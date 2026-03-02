"""
SkillGapAgent - Analyzes user's skill gaps based on their goal and background.
"""

from typing import Optional, Dict, Any
from .base_agent import BaseAgent


class SkillGapAgent(BaseAgent):
    """
    Agent responsible for analyzing skill gaps.
    
    Input: role, current_level, weekly_hours, background_text
    Output: JSON with required_skills, missing_skills, priority_order, confidence_assessment
    """
    
    @property
    def system_prompt(self) -> str:
        return """You are SkillGapAssessor, an expert tech career advisor specializing in women re-entering or transitioning into tech. You are known for being THE most specific, honest, and thorough skill gap analyzer — not just listing skills, but explaining WHY each skill matters and HOW long it realistically takes.

SPECIFICITY RULES (never break these):
1. When listing skills, ALWAYS group them into: (a) Must-Have for first job, (b) Nice-to-Have differentiators, (c) Long-term growth skills
2. For each missing skill, estimate realistic hours to competency based on user's weekly hours — not just "2 weeks" but "~40 hours, so ~4 weeks at 10hrs/week"
3. Call out the specific sub-skills that matter — not "learn Python" but "Python: list comprehensions, decorators, async/await, writing clean OOP classes — these come up in every first-round coding interview"
4. Be honest about timeline — don't sugarcoat — if they want to be a senior ML engineer in 2 months with 5 hrs/week, say that's unrealistic and explain why
5. Identify HIDDEN skill gaps — things the user hasn't mentioned but which interviewers ALWAYS ask about for this role (e.g. for Web Dev: "you didn't mention testing — interviewers will ask about Jest/React Testing Library, this is a red flag if absent from your portfolio")
6. For emotional signals: be specific — don't just say "anxiety detected", identify the specific pattern (imposter syndrome from comparing to CS graduates, anxiety about gap in resume, financial pressure shortening timeline)

OUTPUT FORMAT: You must respond with ONLY valid JSON. No explanations, no markdown, just JSON."""
    
    def build_prompt(self, **kwargs) -> str:
        role = kwargs.get('role', '')
        current_level = kwargs.get('current_level', '')
        weekly_hours = kwargs.get('weekly_hours', 10)
        background_text = kwargs.get('background_text', '')
        situation = kwargs.get('situation', '')
        
        return f"""Analyze the skill gaps for this user:

TARGET ROLE: {role}
CURRENT LEVEL: {current_level}
AVAILABLE HOURS/WEEK: {weekly_hours}
CURRENT SITUATION: {situation}

USER BACKGROUND (analyze for skills AND emotional signals):
{background_text}

Based on this information, provide a skill gap analysis.

OUTPUT JSON SCHEMA:
{{
    "required_skills": ["skill1", "skill2", ...],
    "current_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "priority_order": ["highest_priority_skill", "second_priority", ...],
    "confidence_assessment": "Brief assessment of user's readiness and confidence level",
    "emotional_signals": {{
        "anxiety_level": "low/medium/high",
        "imposter_syndrome_detected": true/false,
        "career_break_concerns": true/false,
        "financial_stress": true/false,
        "support_notes": "Brief note on emotional considerations for roadmap pacing"
    }},
    "recommended_focus_areas": ["area1", "area2", "area3"],
    "estimated_months_to_job_ready": number
}}

Remember:
- Be specific to the exact role (e.g., "AI Engineer" needs different skills than "Web Developer")
- Consider the user's weekly hours when estimating timeline
- Extract emotional signals from the background text to inform pacing recommendations
- Output ONLY valid JSON, nothing else."""
    
    def analyze(
        self, 
        role: str, 
        current_level: str, 
        weekly_hours: int,
        background_text: str,
        situation: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze skill gaps for a user.
        
        Args:
            role: Target career role
            current_level: Current skill level (Beginner/Intermediate/Advanced)
            weekly_hours: Available hours per week
            background_text: User's background story and concerns
            situation: Current situation (Student/Working/Career Break)
            
        Returns:
            Skill gap analysis JSON or None
        """
        return self.execute(
            role=role,
            current_level=current_level,
            weekly_hours=weekly_hours,
            background_text=background_text,
            situation=situation
        )


# Role-specific skill mappings for fallback/validation
ROLE_SKILL_MAPS = {
    "AI Engineer": {
        "core": ["Python", "Machine Learning Fundamentals", "Deep Learning", "PyTorch/TensorFlow", "MLOps"],
        "supporting": ["Linear Algebra", "Statistics", "Data Processing", "Git", "Docker"],
        "advanced": ["LLM/Transformers", "Computer Vision", "NLP", "Model Optimization", "Cloud ML Services"]
    },
    "Web Developer": {
        "core": ["HTML/CSS", "JavaScript", "React/Vue/Angular", "Node.js", "REST APIs"],
        "supporting": ["Git", "Responsive Design", "SQL Basics", "Testing", "DevTools"],
        "advanced": ["TypeScript", "Next.js", "GraphQL", "CI/CD", "Cloud Deployment"]
    },
    "Data Analyst": {
        "core": ["Excel/Sheets", "SQL", "Python/R", "Data Visualization", "Statistics"],
        "supporting": ["Pandas", "Tableau/PowerBI", "Data Cleaning", "A/B Testing", "Reporting"],
        "advanced": ["Machine Learning Basics", "Big Data Tools", "ETL Pipelines", "Advanced SQL", "Storytelling with Data"]
    },
    "Career Re-entry into Tech": {
        "core": ["Programming Fundamentals", "Git Basics", "Problem Solving", "Tech Communication", "Modern Tools Overview"],
        "supporting": ["Networking in Tech", "Portfolio Building", "Interview Prep", "Remote Work Skills", "Time Management"],
        "advanced": ["Specialization Choice", "Open Source Contribution", "Building Online Presence", "Tech Community Engagement"]
    }
}


def get_fallback_skills(role: str) -> Dict[str, Any]:
    """Get fallback skill analysis if LLM fails."""
    skills = ROLE_SKILL_MAPS.get(role, ROLE_SKILL_MAPS["Career Re-entry into Tech"])
    
    return {
        "required_skills": skills["core"] + skills["supporting"],
        "current_skills": [],
        "missing_skills": skills["core"] + skills["supporting"],
        "priority_order": skills["core"],
        "confidence_assessment": "Unable to assess - using default skill mapping",
        "emotional_signals": {
            "anxiety_level": "medium",
            "imposter_syndrome_detected": False,
            "career_break_concerns": False,
            "financial_stress": False,
            "support_notes": "Default assessment - personalized analysis unavailable"
        },
        "recommended_focus_areas": skills["core"][:3],
        "estimated_months_to_job_ready": 6
    }
