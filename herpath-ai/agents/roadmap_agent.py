"""
RoadmapAgent - Generates structured learning roadmaps based on skill gaps.
"""

from typing import Optional, Dict, Any, List
from .base_agent import BaseAgent


class RoadmapAgent(BaseAgent):
    """
    Agent responsible for generating structured learning roadmaps.
    
    Input: missing_skills, deadline, weekly_hours, financial_constraint, situation, emotional_signals
    Output: JSON with total_weeks, phases (each with weeks containing tasks and milestones)
    """
    
    @property
    def system_prompt(self) -> str:
        return """You are RoadmapArchitect, an expert learning path designer specializing in tech career transitions for women.

Your role is to:
1. Create structured, week-by-week learning roadmaps
2. Balance skill acquisition with practical projects
3. Set realistic milestones with measurable success metrics
4. Adapt pacing based on user constraints and emotional state
5. Recommend appropriate resources (free and paid alternatives)

Design principles:
- Each week should have a clear focus skill
- Tasks should be specific and actionable (not "learn Python" but "complete Python basics: variables, loops, functions")
- Include mini-projects every 2-3 weeks to build portfolio
- Milestones should be demonstrable achievements
- Consider emotional pacing (don't overwhelm anxious learners)

OUTPUT FORMAT: You must respond with ONLY valid JSON. No explanations, no markdown, just JSON."""
    
    def build_prompt(self, **kwargs) -> str:
        missing_skills = kwargs.get('missing_skills', [])
        priority_order = kwargs.get('priority_order', [])
        deadline_weeks = kwargs.get('deadline_weeks')  # None means flexible
        weekly_hours = kwargs.get('weekly_hours', 10)
        financial_constraint = kwargs.get('financial_constraint', 'Mixed')
        situation = kwargs.get('situation', '')
        emotional_signals = kwargs.get('emotional_signals', {})
        role = kwargs.get('role', '')
        
        deadline_str = f"{deadline_weeks} weeks" if deadline_weeks else "Flexible (recommend optimal timeline)"
        
        return f"""Generate a structured learning roadmap for this user:

TARGET ROLE: {role}
SKILLS TO ACQUIRE (in priority order): {priority_order}
ALL MISSING SKILLS: {missing_skills}
DEADLINE: {deadline_str}
WEEKLY HOURS AVAILABLE: {weekly_hours}
FINANCIAL CONSTRAINT: {financial_constraint}
CURRENT SITUATION: {situation}
EMOTIONAL SIGNALS: {emotional_signals}

Generate a comprehensive roadmap.

OUTPUT JSON SCHEMA:
{{
    "total_weeks": number,
    "phases": [
        {{
            "phase_name": "Phase 1: Foundation",
            "phase_description": "Brief description of phase goals",
            "weeks": [
                {{
                    "week_number": 1,
                    "focus_skill": "Primary skill for this week",
                    "tasks": [
                        "Specific task 1 (2-3 hours)",
                        "Specific task 2 (1-2 hours)",
                        "Specific task 3 (2 hours)",
                        "Practice exercise (1-2 hours)"
                    ],
                    "milestone": "Demonstrable achievement by end of week",
                    "success_metric": "How to verify milestone completion",
                    "resources": [
                        {{
                            "name": "Resource name",
                            "type": "course/tutorial/documentation/project",
                            "url": "URL if applicable",
                            "cost": "Free / $X",
                            "time_estimate": "X hours"
                        }}
                    ]
                }}
            ]
        }}
    ],
    "recommended_projects": [
        {{
            "name": "Project name",
            "week_range": "Weeks X-Y",
            "skills_demonstrated": ["skill1", "skill2"],
            "portfolio_value": "high/medium/low"
        }}
    ],
    "interview_prep_weeks": [list of week numbers dedicated to interview prep],
    "buffer_weeks": number (weeks reserved for catch-up/review)
}}

Guidelines:
- If deadline is flexible, recommend optimal timeline based on weekly hours
- Estimate ~20-30 hours per core skill for beginners, 10-15 for intermediate
- Include 1 project every 3-4 weeks
- Add interview prep in final 2-3 weeks
- If high anxiety, start with 80% of normal pace
- Tasks should sum to approximately the weekly_hours available
- Be specific with resources - name actual courses, tutorials, or platforms
- Output ONLY valid JSON, nothing else."""
    
    def generate(
        self,
        role: str,
        missing_skills: List[str],
        priority_order: List[str],
        deadline_weeks: Optional[int],
        weekly_hours: int,
        financial_constraint: str,
        situation: str,
        emotional_signals: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a learning roadmap.
        
        Args:
            role: Target career role
            missing_skills: List of skills to acquire
            priority_order: Prioritized skill list
            deadline_weeks: Target weeks (None for flexible)
            weekly_hours: Available hours per week
            financial_constraint: "Free Only" / "Mixed" / "Paid Allowed"
            situation: Current situation
            emotional_signals: Emotional context from SkillGapAgent
            
        Returns:
            Roadmap JSON or None
        """
        return self.execute(
            role=role,
            missing_skills=missing_skills,
            priority_order=priority_order,
            deadline_weeks=deadline_weeks,
            weekly_hours=weekly_hours,
            financial_constraint=financial_constraint,
            situation=situation,
            emotional_signals=emotional_signals
        )


def get_fallback_roadmap(
    role: str,
    weekly_hours: int,
    deadline_weeks: Optional[int]
) -> Dict[str, Any]:
    """Generate a basic fallback roadmap if LLM fails."""
    
    # Calculate weeks based on hours
    if deadline_weeks:
        total_weeks = deadline_weeks
    else:
        # Estimate: ~200 hours total for career readiness, distributed by weekly hours
        total_hours_needed = 200
        total_weeks = max(8, min(52, total_hours_needed // weekly_hours))
    
    # Basic phase structure
    foundation_weeks = total_weeks // 3
    building_weeks = total_weeks // 3
    mastery_weeks = total_weeks - foundation_weeks - building_weeks
    
    phases = [
        {
            "phase_name": "Phase 1: Foundation",
            "phase_description": "Build core fundamentals",
            "weeks": [
                {
                    "week_number": i + 1,
                    "focus_skill": f"Core Skill {i + 1}",
                    "tasks": [
                        "Study core concepts (3 hours)",
                        "Practice exercises (2 hours)",
                        "Mini project work (2 hours)"
                    ],
                    "milestone": f"Foundation milestone {i + 1}",
                    "success_metric": "Complete all tasks and exercises",
                    "resources": []
                }
                for i in range(foundation_weeks)
            ]
        },
        {
            "phase_name": "Phase 2: Building",
            "phase_description": "Apply skills through projects",
            "weeks": [
                {
                    "week_number": foundation_weeks + i + 1,
                    "focus_skill": f"Applied Skill {i + 1}",
                    "tasks": [
                        "Advanced concepts (2 hours)",
                        "Project development (3 hours)",
                        "Code review/debugging (2 hours)"
                    ],
                    "milestone": f"Building milestone {i + 1}",
                    "success_metric": "Working project component",
                    "resources": []
                }
                for i in range(building_weeks)
            ]
        },
        {
            "phase_name": "Phase 3: Mastery & Interview Prep",
            "phase_description": "Polish skills and prepare for interviews",
            "weeks": [
                {
                    "week_number": foundation_weeks + building_weeks + i + 1,
                    "focus_skill": "Interview Preparation" if i >= mastery_weeks - 2 else f"Advanced Topic {i + 1}",
                    "tasks": [
                        "Portfolio refinement (2 hours)",
                        "Interview practice (2 hours)",
                        "Networking/applications (2 hours)"
                    ],
                    "milestone": f"Mastery milestone {i + 1}",
                    "success_metric": "Ready for interviews",
                    "resources": []
                }
                for i in range(mastery_weeks)
            ]
        }
    ]
    
    return {
        "total_weeks": total_weeks,
        "phases": phases,
        "recommended_projects": [],
        "interview_prep_weeks": list(range(total_weeks - 2, total_weeks + 1)),
        "buffer_weeks": 1
    }
