"""
Dashboard UI component.
Main dashboard showing user's current status, progress, and weekly focus.
Premium, psychology-optimized design with emotional intelligence.
"""

import streamlit as st
from typing import Dict, Any, Optional
import random


# ============================================================================
# AFFIRMATIONS SYSTEM - Unique differentiator
# ============================================================================

AFFIRMATIONS = [
    "You're not behind. You're on YOUR timeline. 💜",
    "Every expert was once a beginner. Keep going! 🌱",
    "Progress, not perfection. You've got this! ✨",
    "Your career break is a chapter, not the whole story. 📖",
    "Women in tech need YOU. Your perspective matters. 👩‍💻",
    "Small steps lead to big transformations. 🦋",
    "You belong here. Your journey is valid. 💪",
    "Learning at any pace is still learning. 🎯",
    "It's okay to rest. Your roadmap will wait for you. 🌸",
    "Today's effort is tomorrow's success. 🌟"
]


def get_time_based_greeting(name: str) -> tuple:
    """Get greeting and emoji based on time of day."""
    from datetime import datetime
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return f"Good morning, {name}!", "☀️"
    elif 12 <= hour < 17:
        return f"Good afternoon, {name}!", "🌤️"
    elif 17 <= hour < 21:
        return f"Good evening, {name}!", "🌅"
    else:
        return f"Hey there, {name}!", "🌙"


# ============================================================================
# MOOD CHECK-IN - Emotional Intelligence Feature (UNIQUE DIFFERENTIATOR)
# ============================================================================

def _render_mood_checkin(user_data: Dict):
    """
    Quick mood check-in with adaptive suggestions.
    This is a KEY differentiator - we care about the HUMAN, not just the learning.
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F3E8FF 0%, #EDE9FE 100%); 
                padding: 1rem 1.5rem; border-radius: 12px; margin: 1rem 0;">
        <p style="margin: 0; color: #7C3AED; font-weight: 600; font-size: 0.9rem;">
            💜 Quick Check-in
        </p>
        <p style="margin: 0.25rem 0 0 0; color: #64748B; font-size: 0.85rem;">
            How are you feeling about learning today?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    mood_options = {
        "🔥": ("On fire!", "Amazing energy! Let's tackle something challenging today."),
        "😊": ("Feeling good", "Perfect mindset for steady progress. Keep going!"),
        "😐": ("Okay", "That's completely fine. Small wins count too."),
        "😴": ("Low energy", "Rest is productive too. Try a quick 10-min video today."),
        "😰": ("Overwhelmed", "Deep breath. Let's simplify your week together.")
    }
    
    cols = st.columns(5)
    selected_mood = None
    
    for i, (emoji, (label, _)) in enumerate(mood_options.items()):
        with cols[i]:
            if st.button(emoji, key=f"mood_{emoji}", help=label, use_container_width=True):
                selected_mood = emoji
                st.session_state['user_mood'] = emoji
    
    # Show adaptive suggestion based on mood
    current_mood = st.session_state.get('user_mood', None)
    if current_mood and current_mood in mood_options:
        _, suggestion = mood_options[current_mood]
        st.markdown(f"""
        <div style="background: white; padding: 0.75rem 1rem; border-radius: 8px; 
                    border-left: 4px solid #7C3AED; margin-top: 0.5rem;">
            <p style="margin: 0; color: #1E293B; font-size: 0.9rem;">
                {suggestion}
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PROGRESS CELEBRATION - Positive Reinforcement System
# ============================================================================

def _render_progress_celebration(user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Celebrate progress with visual feedback and encouragement.
    Psychology: Positive reinforcement increases motivation and retention.
    """
    completion = progress_data.get('completion_percentage', 0)
    current_week = roadmap_data.get('current_week', 1)
    total_weeks = roadmap_data.get('total_weeks', 1)
    
    # Celebration milestones
    milestones = [
        (0, "🌱", "Just starting", "Every expert was once a beginner!"),
        (10, "🌿", "Building momentum", "You're finding your rhythm!"),
        (25, "🌳", "Quarter done", "You're 25% closer to your goal!"),
        (50, "🎯", "Halfway there", "Amazing! The summit is in sight!"),
        (75, "🚀", "Almost there", "You're crushing it! Keep going!"),
        (90, "⭐", "Final stretch", "The finish line is right there!"),
        (100, "🎉", "Goal achieved", "YOU DID IT! Celebrate yourself!")
    ]
    
    # Find current milestone
    current_milestone = milestones[0]
    for threshold, emoji, title, message in milestones:
        if completion >= threshold:
            current_milestone = (threshold, emoji, title, message)
    
    _, emoji, title, message = current_milestone
    
    # Premium progress card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
                padding: 1.5rem; border-radius: 16px; margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 2rem;">{emoji}</span>
                <span style="color: white; font-weight: 700; font-size: 1.5rem; margin-left: 0.5rem;">
                    {completion:.0f}% Complete
                </span>
            </div>
            <div style="text-align: right;">
                <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">
                    Week {current_week} of {total_weeks}
                </p>
                <p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.8rem;">
                    {title}
                </p>
            </div>
        </div>
        <p style="color: white; margin-top: 0.75rem; margin-bottom: 0; font-style: italic;">
            "{message}"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visual progress bar
    st.progress(completion / 100)


def render_dashboard(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Render the main dashboard with premium UX and emotional intelligence.
    """
    try:
        name = user_data.get('name', 'there').split()[0]
        greeting, emoji = get_time_based_greeting(name)
        
        # =====================================================================
        # PREMIUM HEADER WITH ADAPTIVE BADGE
        # =====================================================================
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="margin-bottom: 0.5rem;">
                <span style="font-size: 2.5rem; font-weight: 700; color: #1E293B;">
                    {emoji} {greeting}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Daily affirmation - changes daily
            affirmation = AFFIRMATIONS[hash(str(user_data.get('uid', ''))) % len(AFFIRMATIONS)]
            st.markdown(f"""
            <p style="color: #7C3AED; font-style: italic; font-size: 1.1rem; margin-top: 0;">
                "{affirmation}"
            </p>
            """, unsafe_allow_html=True)
        
        with col2:
            # ADAPTIVE INDICATOR - Very visible differentiator
            st.markdown("""
            <div style="text-align: right;">
                <div class="adaptive-indicator">
                    🔄 ADAPTIVE MODE
                </div>
                <p style="font-size: 0.75rem; color: #64748B; margin-top: 0.5rem;">
                    Your roadmap adjusts to your life
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # =====================================================================
        # EMOTIONAL CHECK-IN (Quick Mood Pulse) - UNIQUE FEATURE
        # =====================================================================
        _render_mood_checkin(user_data)
        
        # =====================================================================
        # PROGRESS CELEBRATION CARD
        # =====================================================================
        _render_progress_celebration(user_data, roadmap_data, progress_data)
        
        st.markdown("---")
        
        # Main content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            _render_weekly_focus(roadmap_data, db_client, user_data.get('uid'))
        
        with col2:
            _render_insights_card(progress_data, roadmap_data)
        
        st.markdown("---")
        
        # Quick Actions with premium styling
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
