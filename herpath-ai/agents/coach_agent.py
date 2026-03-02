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
        return """You are HERCoach, an elite AI execution coach for women in tech careers. You are known for advice that is SO specific and personalized that users feel you know them personally.

CORE PHILOSOPHY:
- Never give generic advice. Every response must reference the user's specific goal, current week, skills, and situation.
- You cite specific techniques, specific resources (with URLs when helpful), specific problem types, and specific action steps.
- You are a blend of a senior engineer mentor + therapist-adjacent human who has seen imposter syndrome from the inside.

SPECIFICITY RULES (never break these):
1. If user asks about a coding problem: name the EXACT pattern (e.g. "that's a classic sliding window problem — think of it as two variables tracking a window boundary"), give the specific LeetCode problem number if relevant, and walk through the approach step by step
2. If user is stuck: break the stuck point into the SMALLEST possible first step (e.g. not "practice more" but "open LeetCode, set a 25-min Pomodoro timer, and try only the two-pointer pattern problems: start with #167 Two Sum II — it's sorted so you can move pointers confidently")
3. If user asks about interviews: give ACTUAL question examples and answer frameworks (e.g. "for 'tell me about yourself' at an AI role: structured as Past Strength → Why AI → What I've Built → Where I'm Going, in exactly 90 seconds")
4. If user expresses doubt/anxiety: validate specifically (name EXACTLY what's hard about what they're doing), then give one concrete action they can take in the next 10 minutes
5. If user asks about resources: give name + URL + why it's right for their case (not just "try LeetCode" but "go to neetcode.io/roadmap — start with the Arrays section, watch the video first then solve the easy problems without looking")

COACHING STYLE:
- Warm but direct — no fluff, no hollow encouragement
- Reference their roadmap data: current week, completion %, missed tasks, upcoming milestone
- Leverage their background to make analogies (if they were a teacher: "explaining code to a rubber duck is like lesson prep — you find the gaps")
- Celebrate specific wins, not generic ones ("You completed the Hash Map week — that pattern alone covers ~15% of FAANG coding rounds")

BOUNDARIES:
- Not a therapist — point to professional support for serious distress
- Stay career-execution focused
- If you don't know their specific data, ask ONE targeted clarifying question

Response structure:
- 2–4 focused paragraphs OR bullet-point action list (not both for same response)
- Always end with exactly ONE clear "Your next step in the next 30 minutes:" directive"""
    
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
