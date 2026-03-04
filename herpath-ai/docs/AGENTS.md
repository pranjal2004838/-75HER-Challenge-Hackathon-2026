# Agent Architecture

## Multi-Agent System Design

HERPath AI uses a specialized multi-agent system with role-specific agents orchestrated through the Goose framework.

---

## Agent Hierarchy

```
BaseAgent (Abstract)
├── SkillGapAgent
├── RoadmapAgent
├── CoachAgent
├── RebalanceAgent
└── [Future: SkillGapAgent, InterviewCoachAgent, etc.]
```

---

## Agent Responsibilities

### **SkillGapAgent**
**Role:** Skill gap analyzer and assessor

**Responsibilities:**
- Analyze user's skill gaps based on target role
- Identify missing skills vs. current skills
- Prioritize skills by importance
- Detect emotional signals (imposter syndrome, anxiety)
- Estimate time to job readiness

**System Prompt:** Focuses on specificity and honest assessment without sugarcoating timelines.

**Fallback:** Returns default skill mapping for the selected role if Gemini unavailable.

---

### **RoadmapAgent**
**Role:** Curriculum architect and learning path designer

**Responsibilities:**
- Generate week-by-week learning roadmaps
- Include specific resources (LeetCode #s, course names, URLs)
- Adapt task density to available hours
- Respect financial constraints (free vs. paid)
- Build in interview prep weeks
- Include projects and milestones

**System Prompt:** Enforces hyper-specificity in tasks (never "Learn Python", always "Python: list comprehensions, decorators, async/await").

**Output Format:** Structured JSON with 3+ phases, week-by-week breakdown, resources, and interview prep timeline.

**Fallback:** Rule-based roadmap generation using skill-to-weeks mappings.

---

### **CoachAgent**
**Role:** Contextual execution coach and emotional support

**Responsibilities:**
- Provide mode-specific coaching responses
- Remember full user journey (roadmap + progress + chat history)
- Detect and respond to emotional signals
- Give specific, actionable next steps
- Connect abstract goals to concrete tasks
- Celebrate progress and build confidence

**Modes:**
1. **Clarify Plan:** Explain roadmap decisions and big picture
2. **Feeling Stuck:** Emotional validation + smallest next step
3. **Interview Guidance:** Case prep, behavioral questions, storytelling
4. **General:** On-demand Q&A

**System Prompt:** Emphasizes specificity and knowledge of user context.

**Fallback:** Mode-specific generic responses without personalization.

---

### **RebalanceAgent**
**Role:** Adaptive pathway adjustor

**Responsibilities:**
- Monitor progress and detect divergence
- Trigger rebalancing when rules are met
- Redistribute remaining tasks
- Preserve completed progress
- Adjust deadlines intelligently
- Update user with encouraging messages

**Rebalance Triggers:**
- >30% task miss rate in 2-week window
- >20% ahead of schedule
- >25% change in weekly hours
- Deadline or situation change
- User-requested adjustment

**Output:** Updated roadmap with version history and rebalance summary.

**Fallback:** Simple timeline extension based on hours ratio.

---

## Goose Framework Integration

### **Plan-Execute-Verify Loop**

Each agent execution follows this pattern:

```
1. PLAN
   ├─ Read user context
   ├─ Identify required tools
   └─ Construct prompt

2. EXECUTE
   ├─ Call GeminiTool (if available)
   ├─ Parse JSON response
   ├─ Validate against schema
   └─ Retry if invalid (max 2 retries)

3. VERIFY
   ├─ Check response quality
   ├─ Trigger fallback if low quality
   └─ Return AgentResult with metadata
```

### **Toolkit Components**

```python
Toolkit([
    GeminiTool(model="gemini-3-flash-preview"),
    VerifyTool()  # Validates LLM outputs
])
```

**GeminiTool:**
- Calls Gemini REST API with system + user prompts
- Handles authentication and rate limiting
- Timeout: 45 seconds
- Retries: up to 2 with exponential backoff (1s, 2s)

**VerifyTool:**
- Validates JSON parsing
- Checks required fields
- Confirms response schema compliance
- Triggers fallback if validation fails

**FallbackManager:**
- Stores hardcoded responses for all agent modes
- Activates on API errors or timeouts
- Provides graceful degradation

---

## State Management

### **User State**
```python
{
    "uid": "user123",
    "name": "Sarah",
    "goal": "AI Engineer",
    "current_level": "Beginner",
    "weekly_hours": 15,
    "deadline_type": "6 months",
    "financial_constraint": "Mixed",
    "situation": "Career Break",
    "background_text": "..."
}
```

### **Roadmap State**
```python
{
    "total_weeks": 26,
    "current_week": 4,
    "phases": [...],
    "generated_at": "2026-03-04T10:00:00Z",
    "last_rebalanced_at": "2026-03-02T10:00:00Z",
    "is_active": True
}
```

### **Progress State**
```python
{
    "completion_percentage": 16.5,
    "missed_tasks_count": 7,
    "completed_tasks_count": 5,
    "total_tasks_count": 42,
    "pace_status": "ON_TRACK",
    "current_week": 4,
    "weeks_behind": 0
}
```

---

## Control Flow

```
User Onboarding
     ↓
SkillGapAgent (analyze gaps)
     ↓
RoadmapAgent (generate roadmap)
     ↓
Store in Firebase
     ↓
Dashboard Display
     ↓
               ┌─ CoachAgent (chat)
               ├─ RebalanceAgent (if rules triggered)
               └─ Progress Tracking
```

---

## Extensibility

To add a new agent:

1. Inherit from `BaseAgent`
2. Implement `system_prompt` property
3. Implement `build_prompt()` method
4. Call `self.call_llm(prompt)` for executions
5. Register in Toolkit if needed

Example:

```python
from agents.base_agent import BaseAgent

class InterviewCoachAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return """You are an elite interview coach..."""
    
    def build_prompt(self, **kwargs) -> str:
        return f"..."
    
    def coach_interview(self, question: str) -> str:
        prompt = self.build_prompt(question=question)
        return self.call_llm(prompt)
```

---

## Error Handling Strategy

| Error Type | Fallback | Retry |
|-----------|----------|-------|
| Gemini API timeout | Mode-specific hardcoded response | Yes (max 2) |
| Invalid JSON | Return closest valid response | Yes (max 2) |
| Firebase unavailable | In-memory cache for demo account | No |
| Rate limit (Gemini) | Queue request + exponential backoff | Yes |

---

## Performance Notes

- **SkillGapAgent:** ~2-4 seconds (lightweight analysis)
- **RoadmapAgent:** ~15-25 seconds (complex generation)
- **CoachAgent:** ~2-4 seconds (focused response)
- **RebalanceAgent:** ~10-15 seconds (algorithm + update)

All agents have 45-second timeout with graceful fallback.

---

## Monitoring & Logging

Structured logging at DEBUG, INFO, ERROR levels:

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"RoadmapAgent executing for user {uid}")
logger.debug(f"Prompt: {prompt}")
logger.error(f"API error: {error_msg}")
```

See [utils/logging.py](../utils/logging.py) for centralized configuration.

---

## Testing Agents

```bash
# Test individual agent
python -c "from agents.coach_agent import CoachAgent; agent = CoachAgent(); print(agent.system_prompt)"

# Test with mock LLM
python tests/test_agents.py

# Run full pipeline
python -m pytest tests/ -v
```
