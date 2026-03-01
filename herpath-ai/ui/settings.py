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
    """Render roadmap rebalancing section with Life Events."""
    
    # =====================================================================
    # UNIQUE DIFFERENTIATOR: LIFE EVENTS QUICK TRIGGERS
    # This is what makes HERPath different from Coursera/LinkedIn Learning
    # =====================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%); 
                border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; color: white;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span class="adaptive-indicator">🔄 ADAPTIVE</span>
        </div>
        <h3 style="margin: 0; color: white;">Life Happens. Your Roadmap Adapts.</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; color: #E0E7FF;">
            Unlike static courses, HERPath automatically adjusts to your real life. 
            Select a life event below and we'll restructure your entire learning path.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🌸 What's happening in your life?")
    st.caption("Select an event and we'll intelligently rebalance your roadmap")
    
    # Life Events Grid - UNIQUE FEATURE
    life_events = {
        "new_job": {
            "icon": "💼",
            "label": "Started New Job",
            "description": "Less time for learning, need to adjust pace",
            "hours_change": -5,
            "message": "Congratulations on your new role! Let's slow down your learning pace while you settle in."
        },
        "more_time": {
            "icon": "⏰",
            "label": "More Free Time",
            "description": "Can dedicate more hours weekly",
            "hours_change": +5,
            "message": "Great! Let's accelerate your learning and get you to your goal faster."
        },
        "family_care": {
            "icon": "👨‍👩‍👧",
            "label": "Family Responsibilities",
            "description": "Need to reduce workload temporarily",
            "hours_change": -3,
            "message": "Family comes first. We'll spread your tasks over more weeks so nothing feels rushed."
        },
        "burnout": {
            "icon": "😮‍💨",
            "label": "Feeling Overwhelmed",
            "description": "Need a lighter pace, self-care focus",
            "hours_change": -4,
            "message": "It's okay to slow down. We're reducing your weekly load and adding buffer time."
        },
        "motivation_high": {
            "icon": "🔥",
            "label": "Highly Motivated",
            "description": "Ready to push harder towards goal",
            "hours_change": +3,
            "message": "Love the energy! Let's channel that motivation into faster progress."
        },
        "health_break": {
            "icon": "🏥",
            "label": "Health/Medical",
            "description": "Need extended recovery time",
            "hours_change": -6,
            "message": "Your health is the priority. Take all the time you need - your roadmap will wait."
        },
        "career_pivot": {
            "icon": "🔄",
            "label": "Career Direction Change",
            "description": "Want to adjust my goal path",
            "hours_change": 0,
            "message": "Let's realign your roadmap with your new direction."
        },
        "celebration": {
            "icon": "🎉",
            "label": "Milestone Achieved",
            "description": "Just got a win worth celebrating!",
            "hours_change": 0,
            "message": "Amazing! Let's celebrate this win and keep the momentum going! 🎊"
        }
    }
    
    # Display as clickable cards
    cols = st.columns(4)
    selected_event = None
    
    for idx, (event_key, event_data) in enumerate(life_events.items()):
        with cols[idx % 4]:
            # Create a card-like button for each event
            if st.button(
                f"{event_data['icon']} {event_data['label']}",
                key=f"life_event_{event_key}",
                use_container_width=True,
                help=event_data['description']
            ):
                selected_event = event_key
                st.session_state.selected_life_event = event_key
    
    # If an event was just selected or is in session state
    if 'selected_life_event' in st.session_state:
        event_key = st.session_state.selected_life_event
        event_data = life_events.get(event_key, {})
        
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #F0FDF4; border-left: 4px solid #10B981; 
                    padding: 1rem 1.5rem; border-radius: 0 12px 12px 0; margin: 1rem 0;">
            <strong>{event_data['icon']} {event_data['message']}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Show impact preview
        hours_change = event_data.get('hours_change', 0)
        current_hours = user_data.get('weekly_hours', 10)
        new_hours = max(3, current_hours + hours_change)
        
        if hours_change != 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Hours", f"{current_hours}/week")
            with col2:
                st.metric("Suggested Hours", f"{new_hours}/week", delta=f"{hours_change:+d}")
            with col3:
                # Calculate new timeline
                current_week = roadmap_data.get('current_week', 1)
                remaining_weeks = roadmap_data.get('total_weeks', 12) - current_week
                if hours_change < 0:
                    new_remaining = int(remaining_weeks * current_hours / new_hours)
                    st.metric("New Timeline", f"+{new_remaining - remaining_weeks} weeks")
                else:
                    new_remaining = int(remaining_weeks * current_hours / new_hours)
                    st.metric("Time Saved", f"{remaining_weeks - new_remaining} weeks")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ Apply This Change", type="primary", use_container_width=True):
                _execute_life_event_rebalance(
                    db_client, uid, user_data, roadmap_data, progress_data,
                    event_key, event_data, new_hours if hours_change != 0 else None
                )
        with col2:
            if st.button("Cancel", use_container_width=True):
                del st.session_state.selected_life_event
                st.rerun()
    
    st.markdown("---")
    
    # Keep manual rebalance as advanced option
    with st.expander("⚙️ Advanced: Custom Rebalance"):
        _render_manual_rebalance(db_client, uid, user_data, roadmap_data, progress_data)


def _execute_life_event_rebalance(db_client, uid, user_data, roadmap_data, progress_data, event_key, event_data, new_hours):
    """Execute rebalance based on life event."""
    
    from agents import RebalanceAgent, simple_rebalance
    from utils import sanitize_roadmap_output, ensure_week_continuity
    from datetime import datetime
    
    with st.spinner(f"Adapting your roadmap for: {event_data['label']}..."):
        rebalance_reason = f"Life Event: {event_data['label']} - {event_data['description']}"
        
        try:
            rebalance_agent = RebalanceAgent()
            new_roadmap = rebalance_agent.rebalance(
                current_roadmap=roadmap_data,
                progress_data=progress_data,
                user_data=user_data,
                rebalance_reason=rebalance_reason,
                new_weekly_hours=new_hours,
                new_deadline_weeks=None
            )
        except Exception:
            new_roadmap = None
        
        if not new_roadmap:
            new_roadmap = simple_rebalance(
                current_roadmap=roadmap_data,
                progress_data=progress_data,
                new_weekly_hours=new_hours,
                original_weekly_hours=user_data.get('weekly_hours', 10)
            )
        
        new_roadmap = sanitize_roadmap_output(new_roadmap)
        new_roadmap['phases'] = ensure_week_continuity(new_roadmap.get('phases', []))
        
        roadmap_data_to_save = {
            'uid': uid,
            **new_roadmap,
            'current_week': progress_data.get('current_week', 1),
            'is_active': True,
            'rebalance_reason': rebalance_reason,
            'life_event': event_key,
            'generated_at': datetime.utcnow()
        }
        
        if db_client:
            db_client.create_roadmap(roadmap_data_to_save)
            if new_hours:
                db_client.update_user(uid, {'weekly_hours': new_hours})
        else:
            st.session_state.demo_roadmap_data = roadmap_data_to_save
            if new_hours and 'demo_user_data' in st.session_state:
                st.session_state.demo_user_data['weekly_hours'] = new_hours
    
    # Clear the selection
    if 'selected_life_event' in st.session_state:
        del st.session_state.selected_life_event
    
    # Success message with celebration
    st.balloons()
    st.success(f"🎉 Your roadmap has been adapted! {event_data['message']}")
    st.rerun()


def _render_manual_rebalance(db_client, uid: str, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """Render manual rebalance form (advanced option)."""
    
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
