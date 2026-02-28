"""
Dashboard UI component.
Main dashboard showing user's current status, progress, and weekly focus.
"""

import streamlit as st
from typing import Dict, Any, Optional


def render_dashboard(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Render the main dashboard.
    
    Args:
        db_client: FirestoreClient instance
        user_data: User profile data
        roadmap_data: Active roadmap data
        progress_data: Progress summary data
    """
    try:
        # Header with greeting
        name = user_data.get('name', 'there').split()[0]  # First name only
        st.title(f"Welcome back, {name}! 👋")
        
        # Top Identity Card
        _render_identity_card(user_data, roadmap_data, progress_data)
        
        st.markdown("---")
        
        # Main content in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # This Week's Focus
            _render_weekly_focus(roadmap_data, db_client, user_data.get('uid'))
        
        with col2:
            # Insights and Actions
            _render_insights_card(progress_data, roadmap_data)
        
        st.markdown("---")
        
        # Quick Actions
        _render_quick_actions()
    
    except Exception as e:
        st.error("😕 Something went wrong loading your dashboard.")
        st.markdown("Try refreshing the page or navigating to another section.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"{type(e).__name__}: {e}", language="text")
        if st.button("🔄 Retry", type="primary"):
            st.rerun()


def _render_identity_card(user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """Render the top identity card with key stats."""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Goal",
            value=user_data.get('goal', 'Not set'),
            help="Your career target"
        )
    
    with col2:
        deadline = user_data.get('deadline_type', 'Flexible')
        total_weeks = roadmap_data.get('total_weeks', '-')
        st.metric(
            label="📅 Timeline",
            value=f"{total_weeks} weeks",
            delta=deadline if deadline != 'Flexible' else None,
            help="Total duration of your roadmap"
        )
    
    with col3:
        current_week = roadmap_data.get('current_week', 1)
        total_weeks = roadmap_data.get('total_weeks', 1)
        st.metric(
            label="📆 Current Week",
            value=f"Week {current_week}",
            delta=f"of {total_weeks}",
            help="Your current position in the roadmap"
        )
    
    with col4:
        completion = progress_data.get('completion_percentage', 0)
        st.metric(
            label="📊 Progress",
            value=f"{completion:.0f}%",
            help="Overall completion percentage"
        )
    
    # Progress bar
    st.progress(completion / 100)


def _render_weekly_focus(roadmap_data: Dict, db_client, uid: str):
    """Render this week's focus section."""
    
    st.subheader("📌 This Week's Focus")
    
    current_week = roadmap_data.get('current_week', 1)
    
    # Find current week in phases
    week_data = None
    current_phase = None
    
    for phase in roadmap_data.get('phases', []):
        for week in phase.get('weeks', []):
            if week.get('week_number') == current_week:
                week_data = week
                current_phase = phase.get('phase_name', '')
                break
        if week_data:
            break
    
    if not week_data:
        st.info("No week data found. Your roadmap may need to be regenerated.")
        return
    
    # Phase badge
    st.caption(f"Phase: {current_phase}")
    
    # Focus skill
    st.markdown(f"### 🔍 Focus: {week_data.get('focus_skill', 'General')}")
    
    # Tasks
    st.markdown("#### Tasks")
    
    # Get tasks from database
    tasks = db_client.get_tasks_for_week(uid, current_week) if db_client else None
    
    if tasks:
        for task in tasks:
            task_id = task.get('doc_id')
            status = task.get('status', 'pending')
            title = task.get('title', '')
            
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                checked = st.checkbox(
                    "",
                    value=(status == 'completed'),
                    key=f"task_{task_id}"
                )
            with col2:
                if status == 'completed':
                    st.markdown(f"~~{title}~~")
                else:
                    st.markdown(title)
            
            # Update task status if changed
            new_status = 'completed' if checked else 'pending'
            if new_status != status:
                if db_client:
                    db_client.update_task_status(task_id, new_status)
                    db_client.update_progress(uid)
                st.rerun()
    else:
        # Fallback to roadmap tasks
        for task in week_data.get('tasks', []):
            st.markdown(f"- {task}")
    
    # Milestone
    st.markdown("---")
    st.markdown(f"**🏆 Milestone:** {week_data.get('milestone', 'Complete all tasks')}")
    st.caption(f"Success Metric: {week_data.get('success_metric', 'All tasks done')}")
    
    # Resources (if available)
    resources = week_data.get('resources', [])
    if resources:
        with st.expander("📚 Recommended Resources"):
            for res in resources:
                st.markdown(f"**{res.get('name', 'Resource')}**")
                st.caption(f"{res.get('type', '')} | {res.get('cost', 'Free')} | {res.get('time_estimate', '')}")
                if res.get('url'):
                    st.markdown(f"[Open Resource]({res.get('url')})")
                st.markdown("---")


def _render_insights_card(progress_data: Dict, roadmap_data: Dict):
    """Render the insights and actions card."""
    
    st.subheader("💡 Insights")
    
    # Pace status
    pace = progress_data.get('pace_status', 'on_track')
    pace_icons = {
        'ahead': '🚀',
        'on_track': '✅',
        'behind': '⚠️',
        'slightly_behind': '📊'
    }
    pace_labels = {
        'ahead': 'Ahead of schedule!',
        'on_track': 'On track',
        'behind': 'Behind schedule',
        'slightly_behind': 'Slightly behind'
    }
    
    icon = pace_icons.get(pace, '📊')
    label = pace_labels.get(pace, 'Unknown')
    
    st.info(f"{icon} **Pace:** {label}")
    
    # Missed tasks warning
    missed = progress_data.get('missed_tasks_count', 0)
    if missed > 0:
        st.warning(f"⚠️ {missed} missed task(s)")
    
    # Completion stats
    completed = progress_data.get('completed_tasks_count', 0)
    total = progress_data.get('total_tasks_count', 0)
    
    st.markdown(f"**Tasks:** {completed}/{total} completed")
    
    # Weekly hours
    weekly_hours = progress_data.get('weekly_hours', 10)
    
    # Rebalance suggestion
    if pace == 'behind' or missed >= 3:
        st.markdown("---")
        st.markdown("**Suggested Action:**")
        if st.button("⚖️ Rebalance Roadmap", use_container_width=True):
            st.session_state.show_rebalance_modal = True
            st.session_state.current_page = 'settings'
            st.rerun()


def _render_quick_actions():
    """Render quick action buttons."""
    
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🗺️ View Roadmap", use_container_width=True):
            st.session_state.current_page = 'roadmap'
            st.rerun()
    
    with col2:
        if st.button("📊 See Progress", use_container_width=True):
            st.session_state.current_page = 'progress'
            st.rerun()
    
    with col3:
        if st.button("🤖 Talk to Coach", use_container_width=True):
            st.session_state.current_page = 'coach'
            st.rerun()
    
    with col4:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.current_page = 'settings'
            st.rerun()


def advance_week(db_client, uid: str, roadmap_data: Dict) -> bool:
    """
    Advance to the next week.
    
    Returns:
        True if successful
    """
    current_week = roadmap_data.get('current_week', 1)
    total_weeks = roadmap_data.get('total_weeks', 1)
    
    if current_week < total_weeks:
        new_week = current_week + 1
        if db_client:
            success = db_client.update_current_week(uid, new_week)
            if success:
                db_client.update_progress(uid)
            return success
        else:
            # Demo mode: update session state
            import streamlit as st
            if 'demo_roadmap_data' in st.session_state:
                st.session_state.demo_roadmap_data['current_week'] = new_week
            return True
    
    return False
