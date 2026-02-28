"""
AI Coach page UI component.
Chat interface for contextual coaching and guidance.
"""

import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


def render_coach(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """
    Render the AI Coach chat interface.
    
    Args:
        db_client: FirestoreClient instance
        user_data: User profile data
        roadmap_data: Active roadmap data
        progress_data: Progress summary data
    """
    try:
        st.title("🤖 AI Coach")
        st.markdown("Get personalized guidance for your learning journey.")
        
        uid = user_data.get('uid')
        
        # Context card
        _render_context_card(user_data, roadmap_data, progress_data)
        
        st.markdown("---")
        
        # Mode selector
        _render_mode_selector()
        
        st.markdown("---")
        
        # Chat interface
        _render_chat_interface(db_client, uid, user_data, roadmap_data, progress_data)
    
    except Exception as e:
        st.error("😕 The AI Coach ran into an issue.")
        st.markdown("This is usually a temporary problem. Please try again.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"{type(e).__name__}: {e}", language="text")
        if st.button("🔄 Retry", type="primary"):
            st.session_state.pop('chat_messages', None)
            st.rerun()


def _render_context_card(user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """Render the context summary card."""
    
    with st.expander("📋 Your Current Context", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Goal:** {user_data.get('goal', 'Not set')}")
            st.markdown(f"**Current Week:** {roadmap_data.get('current_week', 1)} of {roadmap_data.get('total_weeks', '-')}")
            
            # Current focus
            current_week = roadmap_data.get('current_week', 1)
            focus_skill = "Unknown"
            for phase in roadmap_data.get('phases', []):
                for week in phase.get('weeks', []):
                    if week.get('week_number') == current_week:
                        focus_skill = week.get('focus_skill', 'General')
                        break
            st.markdown(f"**Current Focus:** {focus_skill}")
        
        with col2:
            st.markdown(f"**Progress:** {progress_data.get('completion_percentage', 0):.0f}%")
            st.markdown(f"**Missed Tasks:** {progress_data.get('missed_tasks_count', 0)}")
            st.markdown(f"**Pace:** {progress_data.get('pace_status', 'unknown').replace('_', ' ').title()}")


def _render_mode_selector():
    """Render the coaching mode selector."""
    
    st.markdown("### 💬 How can I help you today?")
    
    modes = {
        "clarify_plan": ("🔍 Clarify Plan", "Understand your roadmap and next steps"),
        "feeling_stuck": ("😔 I'm Feeling Stuck", "Get help overcoming blockers"),
        "interview_guidance": ("💼 Interview Guidance", "Prepare for tech interviews"),
        "general": ("💭 General Question", "Ask anything about your journey")
    }
    
    # Initialize mode if not set
    if 'coach_mode' not in st.session_state:
        st.session_state.coach_mode = 'general'
    
    cols = st.columns(4)
    
    for i, (mode_key, (label, desc)) in enumerate(modes.items()):
        with cols[i]:
            if st.button(
                label,
                use_container_width=True,
                type="primary" if st.session_state.coach_mode == mode_key else "secondary",
                help=desc
            ):
                st.session_state.coach_mode = mode_key
                st.rerun()


def _render_chat_interface(db_client, uid: str, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """Render the chat interface."""
    
    # Initialize chat history in session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        # Load from database
        if uid and db_client:
            history = db_client.get_chat_history(uid, limit=20)
            for chat in history:
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": chat.get('user_message', '')
                })
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": chat.get('ai_response', '')
                })
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "user":
                with st.chat_message("user"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(content)
    
    # Chat input
    mode = st.session_state.get('coach_mode', 'general')
    
    mode_placeholders = {
        "clarify_plan": "Ask about your roadmap, skills, or learning path...",
        "feeling_stuck": "Tell me where you're stuck or what's challenging you...",
        "interview_guidance": "Ask about interview prep, common questions, or how to present yourself...",
        "general": "Type your message..."
    }
    
    user_input = st.chat_input(mode_placeholders.get(mode, "Type your message..."))
    
    if user_input:
        # Add user message to history
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message immediately
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
        
        # Generate response
        with st.spinner("Thinking..."):
            response = _get_coach_response(
                user_input,
                mode,
                user_data,
                roadmap_data,
                progress_data,
                st.session_state.chat_messages
            )
        
        # Add assistant response to history
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Display assistant response
        with chat_container:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(response)
        
        # Save to database
        if uid and db_client:
            db_client.save_chat_message({
                'uid': uid,
                'user_message': user_input,
                'ai_response': response,
                'mode': mode,
                'timestamp': datetime.utcnow()
            })
        
        st.rerun()
    
    # Clear chat button
    if st.session_state.chat_messages:
        if st.button("🗑️ Clear Chat", use_container_width=False):
            st.session_state.chat_messages = []
            st.rerun()


def _get_coach_response(
    message: str,
    mode: str,
    user_data: Dict,
    roadmap_data: Dict,
    progress_data: Dict,
    chat_history: List[Dict]
) -> str:
    """
    Get response from CoachAgent.
    
    Args:
        message: User's message
        mode: Current coaching mode
        user_data: User profile
        roadmap_data: Active roadmap
        progress_data: Progress summary
        chat_history: Recent chat history
        
    Returns:
        Coach response text
    """
    from agents import CoachAgent, get_fallback_response
    
    try:
        coach = CoachAgent()
        
        # Convert chat history to expected format
        formatted_history = []
        for i in range(0, len(chat_history) - 1, 2):
            if i + 1 < len(chat_history):
                formatted_history.append({
                    'user_message': chat_history[i].get('content', ''),
                    'ai_response': chat_history[i + 1].get('content', '')
                })
        
        response = coach.chat(
            user_state=user_data,
            roadmap_state=roadmap_data,
            progress_state=progress_data,
            chat_message=message,
            mode=mode,
            chat_history=formatted_history
        )
        
        if response:
            return response
        else:
            return get_fallback_response(mode, message)
            
    except Exception as e:
        st.error(f"Error getting response: {e}")
        return get_fallback_response(mode, message)


def render_quick_prompts(mode: str) -> List[str]:
    """Get quick prompt suggestions based on mode."""
    
    prompts = {
        "clarify_plan": [
            "Why is this skill important for my goal?",
            "How does this week connect to the bigger picture?",
            "What should I prioritize this week?",
            "Can you explain this phase in more detail?"
        ],
        "feeling_stuck": [
            "I don't understand this concept",
            "I keep procrastinating on my tasks",
            "I feel like I'm not making progress",
            "I'm overwhelmed by how much I have to learn"
        ],
        "interview_guidance": [
            "What questions should I expect?",
            "How do I explain my career transition?",
            "What projects should I highlight?",
            "How do I handle imposter syndrome in interviews?"
        ],
        "general": [
            "What should I focus on today?",
            "How am I doing overall?",
            "Any tips for staying motivated?",
            "What's the most important thing this week?"
        ]
    }
    
    return prompts.get(mode, prompts["general"])
