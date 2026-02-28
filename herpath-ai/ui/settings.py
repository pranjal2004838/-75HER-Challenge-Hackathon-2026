"""
Settings page UI component.
Allows users to update profile and trigger roadmap rebalancing.
"""

import streamlit as st
from typing import Dict, Any
from datetime import datetime


def render_settings(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Render the settings page.
    
    Args:
        db_client: FirestoreClient instance
        user_data: User profile data
        roadmap_data: Active roadmap data
        progress_data: Progress summary data
    """
    try:
        st.title("⚙️ Settings")
        
        uid = user_data.get('uid')
        
        # Profile settings
        _render_profile_settings(db_client, uid, user_data)
        
        st.markdown("---")
        
        # Roadmap rebalancing
        _render_rebalance_section(db_client, uid, user_data, roadmap_data, progress_data)
        
        st.markdown("---")
        
        # Account settings
        _render_account_settings(uid)
    
    except Exception as e:
        st.error("😕 Settings couldn't be loaded.")
        st.markdown("Please try refreshing the page.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"{type(e).__name__}: {e}", language="text")
        if st.button("🔄 Retry", type="primary"):
            st.rerun()


def _render_profile_settings(db_client, uid: str, user_data: Dict):
    """Render profile settings section."""
    
    st.subheader("👤 Profile Settings")
    
    # Import settings
    from config.settings import FINANCIAL_OPTIONS, SITUATION_OPTIONS
    
    with st.form("profile_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly hours
            current_hours = user_data.get('weekly_hours', 10)
            new_hours = st.slider(
                "Weekly Hours",
                min_value=3,
                max_value=40,
                value=current_hours,
                help="How many hours can you dedicate per week?"
            )
            
            # Financial constraint
            current_financial = user_data.get('financial_constraint', 'Mixed (Free preferred, paid okay)')
            financial_index = FINANCIAL_OPTIONS.index(current_financial) if current_financial in FINANCIAL_OPTIONS else 1
            new_financial = st.selectbox(
                "Budget Preference",
                options=FINANCIAL_OPTIONS,
                index=financial_index
            )
        
        with col2:
            # Situation
            current_situation = user_data.get('situation', 'Working Professional')
            situation_index = SITUATION_OPTIONS.index(current_situation) if current_situation in SITUATION_OPTIONS else 0
            new_situation = st.selectbox(
                "Current Situation",
                options=SITUATION_OPTIONS,
                index=situation_index
            )
            
            # Display goal (read-only)
            st.text_input(
                "Current Goal",
                value=user_data.get('goal', ''),
                disabled=True,
                help="To change your goal, you'll need to re-onboard."
            )
        
        submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        if submitted:
            updates = {}
            changes = []
            
            if new_hours != current_hours:
                updates['weekly_hours'] = new_hours
                changes.append(f"Weekly hours: {current_hours} → {new_hours}")
            
            if new_financial != current_financial:
                updates['financial_constraint'] = new_financial
                changes.append("Budget preference updated")
            
            if new_situation != current_situation:
                updates['situation'] = new_situation
                changes.append("Situation updated")
            
            if updates:
                if db_client:
                    success = db_client.update_user(uid, updates)
                else:
                    # Demo mode: update session state
                    if 'demo_user_data' in st.session_state:
                        st.session_state.demo_user_data.update(updates)
                    success = True
                
                if success:
                    st.success("✅ Profile updated!")
                    
                    # Store previous data for rule engine
                    st.session_state.previous_user_data = user_data.copy()
                    
                    # Check if rebalance is needed
                    if 'weekly_hours' in updates:
                        st.info("💡 Your availability changed. Consider rebalancing your roadmap below.")
                        st.session_state.suggest_rebalance = True
                    
                    for change in changes:
                        st.caption(f"• {change}")
                    
                    st.rerun()
                else:
                    st.error("Failed to update profile. Please try again.")


def _render_rebalance_section(db_client, uid: str, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """Render roadmap rebalancing section."""
    
    st.subheader("⚖️ Roadmap Rebalancing")
    
    # Check if rebalance is suggested
    suggest = st.session_state.get('suggest_rebalance', False)
    
    # Get rule engine recommendation
    from utils import rule_engine
    
    previous_data = st.session_state.get('previous_user_data')
    recommendation = rule_engine.evaluate(
        progress_data=progress_data,
        user_data=user_data,
        roadmap_data=roadmap_data,
        previous_user_data=previous_data
    )
    
    # Display recommendation
    if recommendation.should_rebalance or suggest:
        st.warning(f"💡 **Recommendation:** {recommendation.message}")
        
        if recommendation.suggested_actions:
            st.markdown("**Suggested Actions:**")
            for action in recommendation.suggested_actions:
                st.markdown(f"• {action}")
    else:
        st.success("✅ Your roadmap is on track! No rebalancing needed.")
    
    st.markdown("---")
    
    # Manual rebalance options
    st.markdown("### Manual Rebalance")
    
    with st.form("rebalance_form"):
        reason = st.text_area(
            "Why do you want to rebalance? (optional)",
            placeholder="e.g., I got a new job and have less time, I want to speed up, etc.",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_weekly_hours = st.number_input(
                "New Weekly Hours (optional)",
                min_value=0,
                max_value=40,
                value=0,
                help="Leave at 0 to keep current hours"
            )
        
        with col2:
            timeline_change = st.selectbox(
                "Timeline Adjustment",
                options=[
                    "Keep current",
                    "Extend by 2 weeks",
                    "Extend by 4 weeks",
                    "Compress by 2 weeks",
                    "Compress by 4 weeks"
                ]
            )
        
        rebalance_submitted = st.form_submit_button(
            "🔄 Rebalance Roadmap",
            use_container_width=True,
            type="primary"
        )
        
        if rebalance_submitted:
            _execute_rebalance(
                db_client,
                uid,
                user_data,
                roadmap_data,
                progress_data,
                reason,
                new_weekly_hours if new_weekly_hours > 0 else None,
                timeline_change
            )


def _execute_rebalance(
    db_client,
    uid: str,
    user_data: Dict,
    roadmap_data: Dict,
    progress_data: Dict,
    reason: str,
    new_weekly_hours: int,
    timeline_change: str
):
    """Execute the rebalancing process."""
    
    from agents import RebalanceAgent, simple_rebalance
    from config.settings import TIMELINE_OPTIONS
    from utils import sanitize_roadmap_output, ensure_week_continuity
    
    with st.spinner("Rebalancing your roadmap..."):
        # Calculate new deadline weeks
        current_total = roadmap_data.get('total_weeks', 12)
        
        timeline_adjustments = {
            "Keep current": 0,
            "Extend by 2 weeks": 2,
            "Extend by 4 weeks": 4,
            "Compress by 2 weeks": -2,
            "Compress by 4 weeks": -4
        }
        
        adjustment = timeline_adjustments.get(timeline_change, 0)
        new_deadline_weeks = max(4, current_total + adjustment)  # Minimum 4 weeks
        
        # Build rebalance reason
        rebalance_reason = reason if reason else "User requested rebalance"
        if new_weekly_hours:
            rebalance_reason += f" | Hours: {user_data.get('weekly_hours')} → {new_weekly_hours}"
        if adjustment != 0:
            rebalance_reason += f" | Timeline: {adjustment:+d} weeks"
        
        # Try AI rebalance first
        try:
            rebalance_agent = RebalanceAgent()
            new_roadmap = rebalance_agent.rebalance(
                current_roadmap=roadmap_data,
                progress_data=progress_data,
                user_data=user_data,
                rebalance_reason=rebalance_reason,
                new_weekly_hours=new_weekly_hours,
                new_deadline_weeks=new_deadline_weeks if adjustment != 0 else None
            )
        except Exception as e:
            st.warning(f"AI rebalance unavailable: {e}")
            new_roadmap = None
        
        # Fallback to simple rebalance
        if not new_roadmap:
            new_roadmap = simple_rebalance(
                current_roadmap=roadmap_data,
                progress_data=progress_data,
                new_weekly_hours=new_weekly_hours,
                original_weekly_hours=user_data.get('weekly_hours', 10)
            )
        
        # Sanitize and save
        new_roadmap = sanitize_roadmap_output(new_roadmap)
        new_roadmap['phases'] = ensure_week_continuity(new_roadmap.get('phases', []))
        
        # Prepare roadmap data for saving
        roadmap_data_to_save = {
            'uid': uid,
            **new_roadmap,
            'current_week': progress_data.get('current_week', 1),
            'is_active': True,
            'rebalance_reason': rebalance_reason,
            'generated_at': datetime.utcnow(),
            'last_rebalanced_at': datetime.utcnow()
        }
        
        # Save new roadmap (creates new version)
        if db_client:
            success = db_client.create_roadmap(roadmap_data_to_save)
        else:
            # Demo mode: update session state
            st.session_state.demo_roadmap_data = roadmap_data_to_save
            success = True
        
        if success:
            # Update user hours if changed
            if new_weekly_hours:
                if db_client:
                    db_client.update_user(uid, {'weekly_hours': new_weekly_hours})
                elif 'demo_user_data' in st.session_state:
                    st.session_state.demo_user_data['weekly_hours'] = new_weekly_hours
            
            st.success("✅ Roadmap rebalanced successfully!")
            
            # Show summary if available
            summary = new_roadmap.get('rebalance_summary', {})
            if summary:
                st.info(summary.get('user_message', 'Your roadmap has been updated.'))
                
                key_changes = summary.get('key_changes', [])
                if key_changes:
                    st.markdown("**Changes made:**")
                    for change in key_changes:
                        st.markdown(f"• {change}")
            
            # Clear suggestion flag
            if 'suggest_rebalance' in st.session_state:
                del st.session_state.suggest_rebalance
            
            st.rerun()
        else:
            st.error("Failed to save rebalanced roadmap. Please try again.")


def _render_account_settings(uid: str):
    """Render account settings section."""
    
    st.subheader("🔐 Account")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("🔄 Re-onboard", use_container_width=True, help="Start fresh with new goals"):
            st.session_state.force_reonboard = True
            st.session_state.onboarding_completed = False
            st.rerun()
    
    st.markdown("---")
    
    # Danger zone
    with st.expander("⚠️ Danger Zone"):
        st.warning("These actions cannot be undone!")
        
        if st.button("🗑️ Delete All My Data", type="secondary"):
            st.error("This feature is disabled for safety. Contact support to delete your account.")
