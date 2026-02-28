"""
Progress page UI component.
Shows detailed progress analytics and visualizations.
"""

import streamlit as st
from typing import Dict, Any, List


def render_progress(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Render the progress analytics page.
    
    Args:
        db_client: FirestoreClient instance
        user_data: User profile data
        roadmap_data: Active roadmap data
        progress_data: Progress summary data
    """
    try:
        st.title("📊 Your Progress")
        
        # Refresh progress data
        uid = user_data.get('uid')
        if uid and db_client:
            try:
                fresh_progress = db_client.update_progress(uid)
                if fresh_progress:
                    progress_data = fresh_progress
            except Exception:
                pass  # Use existing progress_data
        
        # Main metrics
        _render_progress_metrics(progress_data, roadmap_data)
        
        st.markdown("---")
        
        # Progress breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            _render_completion_chart(progress_data)
        
        with col2:
            _render_pace_analysis(progress_data, roadmap_data)
        
        st.markdown("---")
        
        # Skill progress (if available)
        _render_skill_progress(roadmap_data, progress_data, db_client, uid)
        
        st.markdown("---")
        
        # Weekly breakdown
        _render_weekly_breakdown(roadmap_data, db_client, uid)
    
    except Exception as e:
        st.error("😕 We couldn't load your progress data.")
        st.markdown("Try refreshing the page. Your progress is still saved.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"{type(e).__name__}: {e}", language="text")
        if st.button("🔄 Retry", type="primary"):
            st.rerun()


def _render_progress_metrics(progress_data: Dict, roadmap_data: Dict):
    """Render main progress metrics."""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completion = progress_data.get('completion_percentage', 0)
        st.metric(
            "Overall Completion",
            f"{completion:.1f}%",
            help="Percentage of all tasks completed"
        )
        st.progress(completion / 100)
    
    with col2:
        completed = progress_data.get('completed_tasks_count', 0)
        total = progress_data.get('total_tasks_count', 0)
        st.metric(
            "Tasks Completed",
            f"{completed}/{total}",
            help="Number of completed tasks out of total"
        )
    
    with col3:
        missed = progress_data.get('missed_tasks_count', 0)
        st.metric(
            "Missed Tasks",
            missed,
            delta=None if missed == 0 else f"-{missed}",
            delta_color="inverse",
            help="Tasks marked as skipped"
        )
    
    with col4:
        current_week = roadmap_data.get('current_week', 1)
        total_weeks = roadmap_data.get('total_weeks', 1)
        remaining = total_weeks - current_week
        st.metric(
            "Weeks Remaining",
            remaining,
            help="Weeks left in your roadmap"
        )


def _render_completion_chart(progress_data: Dict):
    """Render completion breakdown chart."""
    
    st.subheader("📈 Task Breakdown")
    
    completed = progress_data.get('completed_tasks_count', 0)
    missed = progress_data.get('missed_tasks_count', 0)
    total = progress_data.get('total_tasks_count', 0)
    pending = max(0, total - completed - missed)
    
    # Simple bar representation
    if total > 0:
        completed_pct = completed / total * 100
        missed_pct = missed / total * 100
        pending_pct = pending / total * 100
        
        st.markdown(f"""
        <div style="background-color: #e0e0e0; border-radius: 10px; overflow: hidden; height: 30px; display: flex;">
            <div style="background-color: #28a745; width: {completed_pct}%; height: 100%;"></div>
            <div style="background-color: #ffc107; width: {pending_pct}%; height: 100%;"></div>
            <div style="background-color: #dc3545; width: {missed_pct}%; height: 100%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"🟢 **Completed:** {completed}")
        with col2:
            st.markdown(f"🟡 **Pending:** {pending}")
        with col3:
            st.markdown(f"🔴 **Missed:** {missed}")
    else:
        st.info("No tasks found yet.")


def _render_pace_analysis(progress_data: Dict, roadmap_data: Dict):
    """Render pace analysis and projection."""
    
    st.subheader("🏃 Pace Analysis")
    
    pace = progress_data.get('pace_status', 'on_track')
    current_week = roadmap_data.get('current_week', 1)
    total_weeks = roadmap_data.get('total_weeks', 1)
    completion = progress_data.get('completion_percentage', 0)
    
    # Expected vs actual
    expected_pct = (current_week / total_weeks * 100) if total_weeks > 0 else 0
    diff = completion - expected_pct
    
    # Pace indicator
    pace_info = {
        'ahead': ('🚀', 'Ahead of Schedule', 'green'),
        'on_track': ('✅', 'On Track', 'blue'),
        'slightly_behind': ('📊', 'Slightly Behind', 'orange'),
        'behind': ('⚠️', 'Behind Schedule', 'red')
    }
    
    icon, label, color = pace_info.get(pace, ('📊', 'Unknown', 'gray'))
    
    st.markdown(f"### {icon} {label}")
    
    # Comparison
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Expected Progress", f"{expected_pct:.0f}%")
    with col2:
        st.metric(
            "Actual Progress",
            f"{completion:.0f}%",
            delta=f"{diff:+.0f}%",
            delta_color="normal" if diff >= 0 else "inverse"
        )
    
    # Projection
    if completion > 0:
        weeks_per_pct = current_week / completion if completion > 0 else 0
        projected_total = weeks_per_pct * 100
        
        if projected_total < total_weeks * 0.9:
            st.success(f"🎯 At this pace, you'll finish in ~{projected_total:.0f} weeks (early!)")
        elif projected_total > total_weeks * 1.1:
            st.warning(f"⏰ At this pace, completion is projected at ~{projected_total:.0f} weeks")
        else:
            st.info(f"📅 On track to finish in {total_weeks} weeks")


def _render_skill_progress(roadmap_data: Dict, progress_data: Dict, db_client, uid: str):
    """Render skill-by-skill progress."""
    
    st.subheader("🎯 Skill Progress")
    
    # Extract skills from phases
    phases = roadmap_data.get('phases', [])
    skills_progress = {}
    
    current_week = roadmap_data.get('current_week', 1)
    
    for phase in phases:
        for week in phase.get('weeks', []):
            skill = week.get('focus_skill', 'General')
            week_num = week.get('week_number', 0)
            
            if skill not in skills_progress:
                skills_progress[skill] = {'total_weeks': 0, 'completed_weeks': 0}
            
            skills_progress[skill]['total_weeks'] += 1
            if week_num < current_week:
                skills_progress[skill]['completed_weeks'] += 1
    
    if not skills_progress:
        st.info("Skill progress tracking will appear as you progress through your roadmap.")
        return
    
    # Display skill bars
    for skill, data in skills_progress.items():
        completed = data['completed_weeks']
        total = data['total_weeks']
        pct = (completed / total * 100) if total > 0 else 0
        
        st.markdown(f"**{skill}**")
        st.progress(pct / 100)
        st.caption(f"{completed}/{total} weeks completed ({pct:.0f}%)")


def _render_weekly_breakdown(roadmap_data: Dict, db_client, uid: str):
    """Render week-by-week task completion breakdown."""
    
    st.subheader("📅 Weekly Breakdown")
    
    phases = roadmap_data.get('phases', [])
    current_week = roadmap_data.get('current_week', 1)
    
    # Collect all weeks
    all_weeks = []
    for phase in phases:
        for week in phase.get('weeks', []):
            all_weeks.append(week)
    
    # Sort by week number
    all_weeks.sort(key=lambda w: w.get('week_number', 0))
    
    # Display recent weeks
    display_weeks = [w for w in all_weeks if w.get('week_number', 0) <= current_week + 2]
    
    if not display_weeks:
        st.info("Weekly breakdown will appear as you progress.")
        return
    
    for week in display_weeks[-8:]:  # Show last 8 relevant weeks
        week_num = week.get('week_number', 0)
        focus = week.get('focus_skill', 'General')
        tasks = week.get('tasks', [])
        
        # Determine status
        if week_num < current_week:
            status_icon = "✅"
        elif week_num == current_week:
            status_icon = "▶️"
        else:
            status_icon = "⏳"
        
        with st.expander(f"{status_icon} Week {week_num}: {focus}"):
            # Get task status from DB if current or past
            if week_num <= current_week:
                db_tasks = db_client.get_tasks_for_week(uid, week_num) if db_client else None
                
                if db_tasks:
                    completed = sum(1 for t in db_tasks if t.get('status') == 'completed')
                    total = len(db_tasks)
                    st.progress(completed / total if total > 0 else 0)
                    st.caption(f"{completed}/{total} tasks completed")
                    
                    for task in db_tasks:
                        status = task.get('status', 'pending')
                        title = task.get('title', '')
                        if status == 'completed':
                            st.markdown(f"✅ ~~{title}~~")
                        elif status == 'skipped':
                            st.markdown(f"⏭️ ~~{title}~~ (skipped)")
                        else:
                            st.markdown(f"⬜ {title}")
                else:
                    for task in tasks:
                        st.markdown(f"- {task}")
            else:
                for task in tasks:
                    st.markdown(f"- {task}")
