"""
Fallback Manager - Graceful Degradation System
==============================================

Provides intelligent fallback responses when primary AI tools fail.
Ensures the application remains functional even when:
- Gemini API is unavailable
- Rate limits are hit
- Network errors occur
- Unexpected exceptions happen

Design Philosophy:
- Users should always get a helpful response
- Fallbacks should be context-aware
- Degradation should be transparent
- Recovery should be automatic
"""

import logging
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class FallbackTier(Enum):
    """Tiers of fallback responses, ordered by preference."""
    CACHED = "cached"           # Use cached/previous responses
    TEMPLATE = "template"       # Use role-specific templates
    GENERIC = "generic"         # Use generic helpful responses
    MINIMAL = "minimal"         # Bare minimum acknowledgment


@dataclass
class FallbackResponse:
    """
    A fallback response with metadata.
    
    Attributes:
        content: The actual response text
        tier: Which fallback tier was used
        context_used: What context was available
        is_fallback: Always True (for detection)
    """
    content: str
    tier: FallbackTier
    context_used: Dict[str, Any] = field(default_factory=dict)
    is_fallback: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "tier": self.tier.value,
            "context_used": self.context_used,
            "is_fallback": self.is_fallback
        }


class FallbackManager:
    """
    Manages fallback responses for when AI services are unavailable.
    
    The manager maintains:
    1. Role-specific template responses
    2. Context-aware response selection
    3. Fallback tier escalation
    4. Response quality tracking
    
    Example:
        manager = FallbackManager()
        
        # Get fallback for coaching
        response = manager.get_fallback(
            agent_type="coach",
            mode="feeling_stuck",
            user_context={"goal": "AI Engineer"}
        )
    """
    
    def __init__(self):
        """Initialize the fallback manager with default responses."""
        self._templates = self._load_default_templates()
        self._cache: Dict[str, str] = {}
    
    def _load_default_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load default fallback templates organized by agent and mode."""
        return {
            "coach": {
                "clarify_plan": [
                    "Your learning plan is designed to build skills progressively. Each phase builds on the previous one, so you're always prepared for what comes next. Could you tell me which specific part you'd like me to explain?",
                    "The roadmap follows a proven learning path for your goal. We start with foundations, then move to practical skills, and finally to interview prep. What aspect would you like to dive deeper into?",
                    "Great question about your plan! Your roadmap is customized based on your current level and timeline. Which phase or skill area interests you most right now?"
                ],
                "feeling_stuck": [
                    "I hear you - feeling stuck is completely normal and happens to every learner. Let's break this down: what's the specific task or concept that's giving you trouble? Once we identify that, we can find a smaller first step to get you moving again.",
                    "It's okay to feel this way. Learning new skills, especially in tech, can be overwhelming. Take a breath. Let's focus on just the next tiny step - what were you working on when you got stuck?",
                    "Being stuck is actually a sign you're pushing your boundaries - that's growth! Let's simplify: what's the ONE thing you're trying to accomplish right now? We'll tackle just that."
                ],
                "interview_guidance": [
                    "Interview prep is crucial, and I'm here to help! For technical interviews, focus on explaining your thought process clearly. For behavioral questions, use the STAR method (Situation, Task, Action, Result). What type of interview are you preparing for?",
                    "Great that you're thinking about interviews! The key is connecting your learning journey to the role requirements. Would you like tips on technical questions, behavioral questions, or how to talk about your career transition?",
                    "Interview success comes from preparation and confidence. Based on your goal, I'd recommend practicing 1-2 coding problems daily and preparing 3-4 strong stories about your projects. What area feels most challenging?"
                ],
                "general": [
                    "I'm here to help you stay on track with your learning journey. What would you like to discuss - your roadmap, specific skills, or getting unstuck on something?",
                    "Thanks for reaching out! How can I support your learning today? I can help with understanding your roadmap, tackling specific challenges, or preparing for interviews.",
                    "Ready to help! Whether you need clarity on your plan, support when stuck, or interview guidance - I'm here. What's on your mind?"
                ]
            },
            "roadmap": {
                "ai_engineer": [
                    {
                        "phase_name": "Foundations",
                        "duration_weeks": 4,
                        "skills": ["Python fundamentals", "Math basics (linear algebra, statistics)", "Git & version control"],
                        "milestone": "Complete 3 Python projects with ML-relevant data structures"
                    },
                    {
                        "phase_name": "Core ML",
                        "duration_weeks": 6,
                        "skills": ["NumPy & Pandas", "Scikit-learn", "Model evaluation"],
                        "milestone": "Build and evaluate 3 supervised learning models"
                    },
                    {
                        "phase_name": "Deep Learning",
                        "duration_weeks": 6,
                        "skills": ["Neural networks", "TensorFlow/PyTorch", "CNNs & RNNs"],
                        "milestone": "Complete a deep learning project with real data"
                    },
                    {
                        "phase_name": "Advanced AI",
                        "duration_weeks": 6,
                        "skills": ["Transformers & LLMs", "MLOps basics", "Model deployment"],
                        "milestone": "Deploy an AI model to production"
                    },
                    {
                        "phase_name": "Interview Prep",
                        "duration_weeks": 4,
                        "skills": ["System design for ML", "Coding interviews", "Portfolio polish"],
                        "milestone": "Complete 5 mock interviews"
                    }
                ],
                "web_developer": [
                    {
                        "phase_name": "Foundations",
                        "duration_weeks": 4,
                        "skills": ["HTML & CSS", "JavaScript basics", "Git & CLI"],
                        "milestone": "Build 3 responsive static websites"
                    },
                    {
                        "phase_name": "Frontend Mastery",
                        "duration_weeks": 6,
                        "skills": ["React/Vue/Angular", "State management", "API integration"],
                        "milestone": "Complete a full frontend project with external APIs"
                    },
                    {
                        "phase_name": "Backend Basics",
                        "duration_weeks": 5,
                        "skills": ["Node.js/Python backend", "REST APIs", "Databases (SQL & NoSQL)"],
                        "milestone": "Build a REST API with authentication"
                    },
                    {
                        "phase_name": "Full Stack",
                        "duration_weeks": 6,
                        "skills": ["Full stack integration", "Deployment (Vercel, AWS)", "Testing"],
                        "milestone": "Deploy a full-stack application"
                    },
                    {
                        "phase_name": "Interview Prep",
                        "duration_weeks": 5,
                        "skills": ["Portfolio projects", "Technical interviews", "System design basics"],
                        "milestone": "Complete 5 mock interviews and portfolio review"
                    }
                ],
                "data_analyst": [
                    {
                        "phase_name": "Foundations",
                        "duration_weeks": 4,
                        "skills": ["Excel/Sheets mastery", "SQL basics", "Statistics fundamentals"],
                        "milestone": "Analyze a real dataset and present insights"
                    },
                    {
                        "phase_name": "Python for Data",
                        "duration_weeks": 5,
                        "skills": ["Python basics", "Pandas & NumPy", "Data cleaning"],
                        "milestone": "Complete 3 data cleaning projects"
                    },
                    {
                        "phase_name": "Visualization",
                        "duration_weeks": 4,
                        "skills": ["Matplotlib & Seaborn", "Tableau/Power BI", "Storytelling with data"],
                        "milestone": "Create a dashboard for a business case"
                    },
                    {
                        "phase_name": "Advanced Analytics",
                        "duration_weeks": 6,
                        "skills": ["Statistical analysis", "A/B testing", "Predictive modeling basics"],
                        "milestone": "Complete an end-to-end analysis project"
                    },
                    {
                        "phase_name": "Interview Prep",
                        "duration_weeks": 4,
                        "skills": ["SQL interviews", "Case studies", "Portfolio presentation"],
                        "milestone": "Complete 5 mock interviews"
                    }
                ],
                "career_reentry": [
                    {
                        "phase_name": "Tech Refresh",
                        "duration_weeks": 4,
                        "skills": ["Current tech landscape", "Chosen stack basics", "Modern tools"],
                        "milestone": "Complete a 'hello world' project in chosen stack"
                    },
                    {
                        "phase_name": "Core Skills",
                        "duration_weeks": 6,
                        "skills": ["Primary technology deep-dive", "Version control", "Collaboration tools"],
                        "milestone": "Contribute to an open-source project"
                    },
                    {
                        "phase_name": "Project Building",
                        "duration_weeks": 6,
                        "skills": ["Portfolio projects", "Real-world applications", "Documentation"],
                        "milestone": "Complete 2 portfolio-worthy projects"
                    },
                    {
                        "phase_name": "Networking & Prep",
                        "duration_weeks": 4,
                        "skills": ["LinkedIn optimization", "Resume gap explanation", "Interview prep"],
                        "milestone": "Apply to 10 relevant positions"
                    }
                ]
            },
            "skill_gap": {
                "default": {
                    "identified_gaps": [
                        "Technical fundamentals for your target role",
                        "Practical project experience",
                        "Portfolio development",
                        "Interview readiness"
                    ],
                    "priorities": [
                        {
                            "skill": "Core technical skills",
                            "priority": "HIGH",
                            "reason": "Foundation for all advanced learning"
                        },
                        {
                            "skill": "Hands-on projects",
                            "priority": "HIGH",
                            "reason": "Employers value demonstrated ability"
                        },
                        {
                            "skill": "Soft skills & communication",
                            "priority": "MEDIUM",
                            "reason": "Critical for interviews and team work"
                        }
                    ]
                }
            },
            "rebalance": {
                "default": {
                    "recommendation": "Based on your current progress, consider adjusting your weekly commitments. Focus on completing current tasks before moving to new ones.",
                    "suggested_actions": [
                        "Review and complete any pending tasks from current week",
                        "If consistently behind, reduce weekly goal by 20%",
                        "If ahead of schedule, consider adding stretch goals",
                        "Schedule dedicated focus time for challenging topics"
                    ]
                }
            }
        }
    
    def get_fallback(
        self,
        agent_type: str,
        mode: str = "general",
        user_context: Optional[Dict[str, Any]] = None
    ) -> FallbackResponse:
        """
        Get an appropriate fallback response.
        
        Args:
            agent_type: Type of agent (coach, roadmap, skill_gap, rebalance)
            mode: Specific mode or context (e.g., "feeling_stuck" for coach)
            user_context: Optional user context for personalization
            
        Returns:
            FallbackResponse with appropriate content
        """
        user_context = user_context or {}
        
        # Try to get cached response first
        cache_key = f"{agent_type}:{mode}"
        if cache_key in self._cache:
            return FallbackResponse(
                content=self._cache[cache_key],
                tier=FallbackTier.CACHED,
                context_used=user_context
            )
        
        # Try template responses
        if agent_type in self._templates:
            agent_templates = self._templates[agent_type]
            
            # Normalize mode key
            mode_key = mode.lower().replace(" ", "_").replace("-", "_")
            
            if mode_key in agent_templates:
                templates = agent_templates[mode_key]
                if isinstance(templates, list) and len(templates) > 0:
                    # Pick a random template for variety
                    if isinstance(templates[0], str):
                        content = random.choice(templates)
                        return self._personalize_response(
                            content, user_context, FallbackTier.TEMPLATE
                        )
                    else:
                        # It's a structured response (like roadmap)
                        return FallbackResponse(
                            content=templates,
                            tier=FallbackTier.TEMPLATE,
                            context_used=user_context
                        )
            
            # Try default mode
            if "default" in agent_templates:
                content = agent_templates["default"]
                if isinstance(content, dict):
                    return FallbackResponse(
                        content=content,
                        tier=FallbackTier.TEMPLATE,
                        context_used=user_context
                    )
            
            # Try general mode
            if "general" in agent_templates:
                templates = agent_templates["general"]
                if isinstance(templates, list) and len(templates) > 0:
                    content = random.choice(templates)
                    return self._personalize_response(
                        content, user_context, FallbackTier.TEMPLATE
                    )
        
        # Generic fallback
        return self._get_generic_fallback(agent_type, user_context)
    
    def _personalize_response(
        self,
        content: str,
        context: Dict[str, Any],
        tier: FallbackTier
    ) -> FallbackResponse:
        """Personalize a template response with user context."""
        # Simple personalization - replace placeholders
        personalized = content
        
        if context.get("name"):
            personalized = f"{context['name']}, " + personalized[0].lower() + personalized[1:]
        
        if context.get("goal"):
            personalized = personalized.replace("your goal", f"becoming a {context['goal']}")
        
        return FallbackResponse(
            content=personalized,
            tier=tier,
            context_used=context
        )
    
    def _get_generic_fallback(
        self,
        agent_type: str,
        context: Dict[str, Any]
    ) -> FallbackResponse:
        """Get a generic fallback when no templates match."""
        generic_responses = {
            "coach": "I'm here to support your learning journey. While I'm having trouble connecting right now, remember: consistent small steps lead to big progress. What specific challenge can I help you think through?",
            "roadmap": "I'm preparing your personalized roadmap. This typically includes foundational skills, core competencies, practical projects, and interview preparation - customized to your goals and timeline.",
            "skill_gap": "Based on typical career transitions, focus areas usually include: technical fundamentals, practical project experience, and interview readiness. I'll provide more specific analysis shortly.",
            "rebalance": "To optimize your learning pace, consider reviewing your current progress and adjusting weekly goals based on your available time. Consistent progress matters more than speed."
        }
        
        content = generic_responses.get(
            agent_type,
            "I'm processing your request. Please try again in a moment."
        )
        
        return FallbackResponse(
            content=content,
            tier=FallbackTier.GENERIC,
            context_used=context
        )
    
    def get_roadmap_fallback(
        self,
        goal: str,
        weeks: int = 26,
        skill_level: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Get a fallback roadmap structure.
        
        Args:
            goal: Target role/goal
            weeks: Total weeks for roadmap
            skill_level: Current skill level
            
        Returns:
            Structured roadmap dictionary
        """
        # Normalize goal to key
        goal_key = goal.lower().replace(" ", "_").replace("-", "_")
        
        # Map common variations
        goal_mapping = {
            "ai_engineer": "ai_engineer",
            "machine_learning": "ai_engineer",
            "ml_engineer": "ai_engineer",
            "artificial_intelligence": "ai_engineer",
            "web_developer": "web_developer",
            "frontend_developer": "web_developer",
            "backend_developer": "web_developer",
            "full_stack": "web_developer",
            "data_analyst": "data_analyst",
            "data_science": "data_analyst",
            "business_analyst": "data_analyst",
            "career_re_entry": "career_reentry",
            "career_reentry": "career_reentry",
            "career_break": "career_reentry",
            "returning_to_tech": "career_reentry"
        }
        
        mapped_goal = goal_mapping.get(goal_key, "ai_engineer")
        templates = self._templates.get("roadmap", {})
        
        if mapped_goal in templates:
            phases = templates[mapped_goal]
            return {
                "success": True,
                "is_fallback": True,
                "roadmap": {
                    "goal": goal,
                    "total_weeks": weeks,
                    "skill_level": skill_level,
                    "phases": phases,
                    "generated_by": "fallback_template"
                }
            }
        
        # Ultimate fallback - generic roadmap structure
        return {
            "success": True,
            "is_fallback": True,
            "roadmap": {
                "goal": goal,
                "total_weeks": weeks,
                "skill_level": skill_level,
                "phases": [
                    {
                        "phase_name": "Foundations",
                        "duration_weeks": max(4, weeks // 6),
                        "skills": ["Core fundamentals", "Basic tools", "Learning habits"],
                        "milestone": "Complete foundational assessment"
                    },
                    {
                        "phase_name": "Core Skills",
                        "duration_weeks": max(6, weeks // 4),
                        "skills": ["Primary skills for role", "Practical application", "Project work"],
                        "milestone": "Complete first project"
                    },
                    {
                        "phase_name": "Advanced Topics",
                        "duration_weeks": max(6, weeks // 4),
                        "skills": ["Advanced techniques", "Specialization", "Portfolio building"],
                        "milestone": "Complete portfolio project"
                    },
                    {
                        "phase_name": "Interview Prep",
                        "duration_weeks": max(4, weeks // 6),
                        "skills": ["Technical interviews", "Behavioral prep", "Networking"],
                        "milestone": "Complete 5 mock interviews"
                    }
                ],
                "generated_by": "generic_fallback"
            }
        }
    
    def cache_response(self, key: str, response: str) -> None:
        """Cache a response for future use."""
        self._cache[key] = response
    
    def clear_cache(self) -> None:
        """Clear all cached responses."""
        self._cache.clear()


# Global fallback manager instance
_fallback_manager: Optional[FallbackManager] = None


def get_fallback_manager() -> FallbackManager:
    """Get or create the global fallback manager."""
    global _fallback_manager
    if _fallback_manager is None:
        _fallback_manager = FallbackManager()
    return _fallback_manager
