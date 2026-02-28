"""
CoachAgent - Provides context-aware execution guidance through chat.
"""

from typing import Optional, Dict, Any, List
from .base_agent import BaseAgent


class CoachAgent(BaseAgent):
    """
    Agent responsible for providing contextual coaching through chat.
    
    Modes:
    - clarify_plan: Explain roadmap decisions, help understand next steps
    - feeling_stuck: Provide emotional support + actionable unsticking strategies
    - interview_guidance: Interview prep, common questions, confidence building
    
    Input: user_state, roadmap_state, progress_state, chat_message, mode
    Output: Contextual response (not JSON, natural text)
    """
    
    @property
    def system_prompt(self) -> str:
        return """You are HERCoach, an AI execution coach for women in tech careers.

Your role is to:
1. Provide actionable guidance based on the user's current position in their roadmap
2. Help them overcome specific blockers
3. Answer questions about their learning path
4. Provide interview preparation support
5. Offer emotional support while staying execution-focused

Coaching style:
- Be warm but direct
- Always tie advice back to their specific roadmap and progress
- No generic motivational fluff - give actionable steps
- Acknowledge challenges women face in tech
- Celebrate progress, no matter how small
- If they're stuck, break down the next step into smaller pieces

IMPORTANT BOUNDARIES:
- You are NOT a therapist - if serious mental health concerns arise, suggest professional support
- Stay focused on career execution - don't drift into unrelated life coaching
- Reference their actual roadmap data in your responses
- If you don't have context, ask clarifying questions

Response style:
- Keep responses focused and actionable (2-4 paragraphs max)
- Use bullet points for action items
- End with a clear next step when appropriate"""
    
    def build_prompt(self, **kwargs) -> str:
        user_state = kwargs.get('user_state', {})
        roadmap_state = kwargs.get('roadmap_state', {})
        progress_state = kwargs.get('progress_state', {})
        chat_message = kwargs.get('chat_message', '')
        mode = kwargs.get('mode', 'general')
        chat_history = kwargs.get('chat_history', [])
        
        # Build context string
        context = f"""USER CONTEXT:
- Name: {user_state.get('name', 'User')}
- Goal: {user_state.get('goal', 'Unknown')}
- Current Level: {user_state.get('current_level', 'Unknown')}
- Situation: {user_state.get('situation', 'Unknown')}
- Weekly Hours: {user_state.get('weekly_hours', 'Unknown')}
- Background: {user_state.get('background_text', 'Not provided')}

ROADMAP STATE:
- Total Weeks: {roadmap_state.get('total_weeks', 'Unknown')}
- Current Week: {roadmap_state.get('current_week', 1)}
- Active Phase: {self._get_active_phase(roadmap_state)}

PROGRESS STATE:
- Completion: {progress_state.get('completion_percentage', 0)}%
- Missed Tasks: {progress_state.get('missed_tasks_count', 0)}
- Pace Status: {progress_state.get('pace_status', 'unknown')}

CHAT MODE: {mode}
"""
        
        # Add recent chat history for context
        if chat_history:
            recent = chat_history[-5:]  # Last 5 messages
            history_str = "\nRECENT CONVERSATION:\n"
            for msg in recent:
                history_str += f"User: {msg.get('user_message', '')}\n"
                history_str += f"Coach: {msg.get('ai_response', '')[:200]}...\n"
            context += history_str
        
        # Mode-specific instructions
        mode_instructions = self._get_mode_instructions(mode)
        
        return f"""{context}

{mode_instructions}

USER MESSAGE:
{chat_message}

Respond as HERCoach. Be helpful, specific, and action-oriented."""
    
    def _get_active_phase(self, roadmap_state: Dict) -> str:
        """Extract active phase name from roadmap."""
        current_week = roadmap_state.get('current_week', 1)
        phases = roadmap_state.get('phases', [])
        
        for phase in phases:
            weeks = phase.get('weeks', [])
            week_numbers = [w.get('week_number', 0) for w in weeks]
            if current_week in week_numbers:
                return phase.get('phase_name', 'Unknown Phase')
        
        return 'Unknown Phase'
    
    def _get_mode_instructions(self, mode: str) -> str:
        """Get mode-specific coaching instructions."""
        modes = {
            "clarify_plan": """CLARIFY PLAN MODE:
- Explain why specific skills/tasks are in their roadmap
- Help them understand the big picture
- Connect current tasks to end goal
- If they're questioning the plan, validate concerns and explain reasoning""",
            
            "feeling_stuck": """FEELING STUCK MODE:
- Acknowledge their feelings first
- Identify the specific blocker
- Break down the stuck point into smaller steps
- Suggest a "smallest viable action" they can take right now
- Remind them of progress they've made
- Normalize the struggle - this is part of learning""",
            
            "interview_guidance": """INTERVIEW GUIDANCE MODE:
- Provide role-specific interview tips
- Help with common technical and behavioral questions
- Build confidence by connecting their learning to interview readiness
- Suggest mock interview practice approaches
- Help them articulate their career transition story positively""",
            
            "general": """GENERAL COACHING MODE:
- Answer their question directly
- Tie advice to their roadmap when relevant
- Be helpful and concise"""
        }
        
        return modes.get(mode, modes["general"])
    
    def chat(
        self,
        user_state: Dict[str, Any],
        roadmap_state: Dict[str, Any],
        progress_state: Dict[str, Any],
        chat_message: str,
        mode: str = "general",
        chat_history: List[Dict] = None
    ) -> Optional[str]:
        """
        Get coaching response for user message.
        
        Args:
            user_state: User profile data
            roadmap_state: Active roadmap data
            progress_state: Progress summary
            chat_message: User's message
            mode: Coaching mode
            chat_history: Recent chat history
            
        Returns:
            Coach response text or None
        """
        prompt = self.build_prompt(
            user_state=user_state,
            roadmap_state=roadmap_state,
            progress_state=progress_state,
            chat_message=chat_message,
            mode=mode,
            chat_history=chat_history or []
        )
        
        # For coach, we want text response not JSON
        response = self.call_llm(prompt, temperature=0.8)
        return response


def get_fallback_response(mode: str, message: str) -> str:
    """Provide basic response if LLM is unavailable."""
    
    responses = {
        "clarify_plan": "I'd love to help clarify your plan! Your roadmap is designed to build skills progressively. Could you tell me specifically which part you'd like me to explain?",
        
        "feeling_stuck": "It's completely normal to feel stuck sometimes - every learner goes through this. Let's break this down: What specific task or concept is giving you trouble? Once we identify that, we can find a smaller first step.",
        
        "interview_guidance": "Great that you're thinking about interviews! The key is connecting your learning journey to the role requirements. Would you like tips on technical questions, behavioral questions, or how to talk about your career transition?",
        
        "general": "Thanks for reaching out! I'm here to help you stay on track with your learning journey. What would you like to discuss?"
    }
    
    return responses.get(mode, responses["general"])
