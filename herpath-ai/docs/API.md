# API Documentation

## Overview

HERPath AI exposes its core functionality through a set of Python agent classes. These agents are orchestrated using the Goose framework with automatic retries, fallback responses, and error handling.

---

## Core Agents

### 1. **SkillGapAgent**

**Purpose:** Analyzes user skill gaps based on target role and background.

**Input:**
```python
agent.analyze(
    role: str,                    # "AI Engineer", "Web Developer", "Data Analyst", "Career Re-entry"
    current_level: str,           # "Beginner", "Intermediate", "Advanced"
    weekly_hours: int,            # Available hours per week
    background_text: str,         # User's background and experience
    situation: str                # "Student", "Working", "Career Break"
)
```

**Output:**
```python
{
    "required_skills": ["skill1", "skill2", ...],
    "current_skills": ["skill1", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "priority_order": ["highest_priority", ...],
    "confidence_assessment": "string",
    "emotional_signals": {
        "anxiety_level": "low|medium|high",
        "imposter_syndrome_detected": bool,
        "career_break_concerns": bool,
        "financial_stress": bool,
        "support_notes": "string"
    },
    "recommended_focus_areas": ["area1", ...],
    "estimated_months_to_job_ready": number
}
```

---

### 2. **RoadmapAgent**

**Purpose:** Generates personalized learning roadmaps with week-by-week tasks.

**Input:**
```python
agent.generate(
    role: str,
    missing_skills: list[str],
    priority_order: list[str],
    deadline_weeks: int | None,  # None = flexible
    weekly_hours: int,
    financial_constraint: str,    # "Free Only", "Mixed", "Paid Allowed"
    situation: str,
    emotional_signals: dict
)
```

**Output:**
```python
{
    "total_weeks": number,
    "phases": [
        {
            "phase_name": "string",
            "phase_description": "string",
            "weeks": [
                {
                    "week_number": number,
                    "focus_skill": "string",
                    "tasks": ["specific task with resources"],
                    "milestone": "string",
                    "success_metric": "string",
                    "interview_relevance": "string",
                    "resources": [...]
                }
            ]
        }
    ],
    "recommended_projects": [...],
    "interview_prep_plan": {...}
}
```

---

### 3. **CoachAgent**

**Purpose:** Provides contextual, emotionally-aware coaching responses.

**Input:**
```python
agent.chat(
    user_state: dict,           # User profile
    roadmap_state: dict,        # Active roadmap
    progress_state: dict,       # User progress
    chat_message: str,          # User's message
    mode: str,                  # "clarify_plan", "feeling_stuck", "interview_guidance", "general"
    chat_history: list[dict]    # Recent conversation
)
```

**Output:**
```
"String response with specific, personalized coaching advice"
```

**Modes:**
- `clarify_plan`: Explain roadmap decisions
- `feeling_stuck`: Emotional support + actionable next steps
- `interview_guidance`: Interview prep and confidence building
- `general`: General Q&A

---

### 4. **RebalanceAgent**

**Purpose:** Adjusts existing roadmaps when user constraints change.

**Input:**
```python
agent.rebalance(
    current_roadmap: dict,                    # Current active roadmap
    progress_data: dict,                      # User progress
    user_data: dict,                          # Updated user profile
    rebalance_reason: str,                    # Why rebalancing triggered
    new_weekly_hours: int = None,
    new_deadline_weeks: int = None
)
```

**Output:**
```python
{
    "total_weeks": number,
    "current_week": number,
    "phases": [...],  # Redistributed phases
    "rebalance_summary": {
        "weeks_added_or_removed": number,
        "tasks_redistributed": number,
        "key_changes": ["change1", ...],
        "user_message": "Encouraging message"
    },
    "recommended_actions": ["action1", ...]
}
```

---

## Goose Framework Integration

All agents inherit from `BaseAgent` and use the Goose-style orchestration:

```python
from agents.base_agent import BaseAgent
from agents.goose import GooseAgent, Toolkit

# Pattern: Plan → Execute → Verify
agent = GooseAgent(
    name="CoachAgent",
    toolkit=toolkit,
    max_steps=3,
    timeout_seconds=45.0,
    retry_on_failure=True,
    max_retries=2
)

result = agent.execute(goal="...", context={...})
# Returns: AgentResult with success, response, is_fallback, steps, metadata
```

---

## Error Handling & Fallback

**Automatic Fallback Triggers:**
- Gemini API timeouts (>45 seconds)
- Invalid JSON responses
- Transient HTTP errors

**Fallback Strategy:**
- Hardcoded responses for each agent mode
- Exponential backoff (1s, 2s, 4s waits)
- Graceful degradation (demo mode if Firebase unavailable)

---

## Rate Limiting

- **Gemini API:** 60 calls/minute (handled transparently)
- **Firebase Firestore:** Unlimited on free tier

---

## Data Schemas

All data is validated with Pydantic:

```python
from database.schema import UserSchema, RoadmapSchema, TaskSchema, ProgressSchema

user = UserSchema(
    uid="user123",
    name="Sarah",
    goal="AI Engineer",
    weekly_hours=15,
    situation="Career Break"
)
```

See [schema.py](../database/schema.py) for all models.

---

## Example Usage

```python
from agents.coach_agent import CoachAgent

coach = CoachAgent()

response = coach.chat(
    user_state={
        "name": "Sarah",
        "goal": "AI Engineer",
        "weekly_hours": 15
    },
    roadmap_state={...},
    progress_state={...},
    chat_message="I'm feeling imposter syndrome",
    mode="feeling_stuck"
)

print(response)
# Output: "I notice you're experiencing imposter syndrome..."
```

---

## Testing

Run tests with:
```bash
python -m pytest tests/ -v
```

---

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for API server setup (FastAPI).
