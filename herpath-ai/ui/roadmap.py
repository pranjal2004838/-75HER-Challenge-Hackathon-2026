"""
Roadmap page UI component.
Displays the full roadmap with collapsible weekly blocks.
"""

import streamlit as st
from typing import Dict, Any, List


def render_roadmap(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Render the roadmap page with collapsible phases and weeks.
    
    Args:
        db_client: FirestoreClient instance
        user_data: User profile data
        roadmap_data: Active roadmap data
        progress_data: Progress summary data
    """
    try:
        st.title("🗺️ Your Learning Roadmap")
        
        # Summary stats
        _render_roadmap_summary(roadmap_data, progress_data)
        
        st.markdown("---")
        
        # Render phases
        phases = roadmap_data.get('phases', [])
        current_week = roadmap_data.get('current_week', 1)
        uid = user_data.get('uid')
        
        if not phases:
            st.warning("No roadmap found. Please complete onboarding or regenerate your roadmap.")
            return
        
        for phase in phases:
            _render_phase(phase, current_week, db_client, uid)
        
        st.markdown("---")
        
        # Roadmap actions
        _render_roadmap_actions(db_client, uid, roadmap_data)
    
    except Exception as e:
        st.error("😕 We couldn't display your roadmap.")
        st.markdown("Your data is safe. Try refreshing or check Settings to regenerate.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"{type(e).__name__}: {e}", language="text")
        if st.button("🔄 Retry", type="primary"):
            st.rerun()


def _render_roadmap_summary(roadmap_data: Dict, progress_data: Dict):
    """Render roadmap summary statistics."""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_weeks = roadmap_data.get('total_weeks', 0)
        st.metric("Total Duration", f"{total_weeks} weeks")
    
    with col2:
        current_week = roadmap_data.get('current_week', 1)
        remaining = max(0, total_weeks - current_week)
        st.metric("Weeks Remaining", remaining)
    
    with col3:
        num_phases = len(roadmap_data.get('phases', []))
        st.metric("Phases", num_phases)
    
    with col4:
        completion = progress_data.get('completion_percentage', 0)
        st.metric("Completion", f"{completion:.0f}%")


def _render_phase(phase: Dict, current_week: int, db_client, uid: str):
    """Render a single phase with its weeks."""
    
    phase_name = phase.get('phase_name', 'Unnamed Phase')
    phase_desc = phase.get('phase_description', '')
    weeks = phase.get('weeks', [])
    
    # Determine phase status
    week_numbers = [w.get('week_number', 0) for w in weeks]
    min_week = min(week_numbers) if week_numbers else 0
    max_week = max(week_numbers) if week_numbers else 0
    
    if current_week > max_week:
        phase_status = "completed"
        status_icon = "✅"
    elif current_week >= min_week:
        phase_status = "current"
        status_icon = "▶️"
    else:
        phase_status = "upcoming"
        status_icon = "⏳"
    
    # Phase header
    with st.expander(f"{status_icon} {phase_name} (Weeks {min_week}-{max_week})", expanded=(phase_status == "current")):
        if phase_desc:
            st.caption(phase_desc)
        
        st.markdown("---")
        
        for week in weeks:
            _render_week(week, current_week, db_client, uid)


def _render_week(week: Dict, current_week: int, db_client, uid: str):
    """Render a single week."""
    
    week_number = week.get('week_number', 0)
    focus_skill = week.get('focus_skill', 'General')
    tasks = week.get('tasks', [])
    milestone = week.get('milestone', '')
    success_metric = week.get('success_metric', '')
    
    # Determine week status
    if week_number < current_week:
        status = "completed"
        status_badge = "✅"
    elif week_number == current_week:
        status = "current"
        status_badge = "▶️"
    else:
        status = "upcoming"
        status_badge = "⏳"
    
    # Week container
    with st.container():
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {status_badge} Week {week_number}: {focus_skill}")
        with col2:
            if status == "current":
                st.markdown("**CURRENT**")
        
        # Tasks
        st.markdown("**Tasks:**")
        
        if status == "current":
            # Interactive tasks for current week
            db_tasks = db_client.get_tasks_for_week(uid, week_number) if db_client else None
            
            if db_tasks:
                for task in db_tasks:
                    task_id = task.get('doc_id')
                    task_status = task.get('status', 'pending')
                    title = task.get('title', '')
                    
                    checked = st.checkbox(
                        title,
                        value=(task_status == 'completed'),
                        key=f"roadmap_task_{task_id}"
                    )
                    
                    # Update if changed
                    new_status = 'completed' if checked else 'pending'
                    if new_status != task_status:
                        if db_client:
                            db_client.update_task_status(task_id, new_status)
                            db_client.update_progress(uid)
                        st.rerun()
            else:
                for task in tasks:
                    st.markdown(f"- {task}")
        else:
            # Static list for other weeks
            for task in tasks:
                if status == "completed":
                    st.markdown(f"- ~~{task}~~")
                else:
                    st.markdown(f"- {task}")
        
        # Milestone
        if milestone:
            st.markdown(f"**🏆 Milestone:** {milestone}")
        
        if success_metric:
            st.caption(f"Success Metric: {success_metric}")
        
        # Resources
        resources = week.get('resources', [])
        if resources:
            with st.expander("📚 Resources"):
                for res in resources:
                    res_name = res.get('name', 'Resource')
                    res_type = res.get('type', '')
                    res_cost = res.get('cost', 'Free')
                    res_url = res.get('url', '')
                    
                    st.markdown(f"**{res_name}** ({res_type})")
                    if res_url:
                        st.markdown(f"[Open]({res_url}) | {res_cost}")
                    else:
                        st.caption(res_cost)
        
        st.markdown("---")


def _render_roadmap_actions(db_client, uid: str, roadmap_data: Dict):
    """Render roadmap action buttons."""
    
    st.subheader("⚡ Actions")
    
    col1, col2, col3 = st.columns(3)
    
    current_week = roadmap_data.get('current_week', 1)
    total_weeks = roadmap_data.get('total_weeks', 1)
    
    with col1:
        if current_week > 1:
            if st.button("← Previous Week", use_container_width=True):
                if db_client:
                    db_client.update_current_week(uid, current_week - 1)
                elif 'demo_roadmap_data' in st.session_state:
                    st.session_state.demo_roadmap_data['current_week'] = current_week - 1
                st.rerun()
    
    with col2:
        if current_week < total_weeks:
            if st.button("Next Week →", use_container_width=True):
                if db_client:
                    db_client.update_current_week(uid, current_week + 1)
                elif 'demo_roadmap_data' in st.session_state:
                    st.session_state.demo_roadmap_data['current_week'] = current_week + 1
                st.rerun()
    
    with col3:
        if st.button("⚖️ Rebalance Plan", use_container_width=True):
            st.session_state.show_rebalance_modal = True
            st.session_state.current_page = 'settings'
            st.rerun()


def render_roadmap_history(db_client, uid: str):
    """Render roadmap version history."""
    
    st.subheader("📜 Roadmap History")
    
    history = db_client.get_roadmap_history(uid) if db_client else None
    
    if not history:
        st.info("No roadmap history found.")
        return
    
    for i, roadmap in enumerate(history):
        is_active = roadmap.get('is_active', False)
        version_date = roadmap.get('roadmap_version')
        reason = roadmap.get('rebalance_reason', 'Initial generation')
        
        status_badge = "✅ Active" if is_active else "📝 Archived"
        
        with st.expander(f"{status_badge} - Version {len(history) - i}"):
            st.markdown(f"**Created:** {version_date}")
            st.markdown(f"**Reason:** {reason}")
            st.markdown(f"**Total Weeks:** {roadmap.get('total_weeks', 'N/A')}")
            
            if not is_active:
                if st.button("Restore this version", key=f"restore_{i}"):
                    # Restore logic would go here
                    st.info("Version restoration feature coming soon.")
