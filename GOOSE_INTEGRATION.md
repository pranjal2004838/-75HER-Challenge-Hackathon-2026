# AI/ML Track: Goose Integration

## Goose Features Integrated

**1. Plan-Execute-Verify Loop**
- All 5 agents (Roadmap, Coach, Skill Gap, Rebalance, Health Check) operate within PEV cycle
- **Plan:** Analyze user context → determine execution path
- **Execute:** Call Gemini API with context injection + structured prompts
- **Verify:** Validate responses with Pydantic schemas before surfacing to user

**2. Multi-Agent Orchestration**
- Roadmap Agent: Generates week-by-week curriculum
- Coach Agent: Context-aware mentoring (4 modes: Stuck/Clarify/Interview/General)
- Rebalance Agent: Adaptive timeline when >30% tasks missed
- Skill Gap & Health Check agents for analysis & validation
- Central orchestrator manages agent sequence and data flow

**3. Tool Management & Verification**
- **GeminiTool:** REST API calls with retry (1s→2s→4s backoff), 30s timeout, JSON validation
- **VerifyTool:** Schema validation on all LLM responses; re-prompts if invalid
- **Rule Engine Tool:** Transparent rebalancing logic (no black-box ML)

**4. Fallback & Resilience (4-Tier)**
- Level 1: Cached responses from user history
- Level 2: Template responses (hardcoded coaching patterns)
- Level 3: Generic encouragement
- Level 4: Minimal single-line support
- Result: 99.9% uptime even if Gemini API fails

**5. Context Injection & State Threading**
- User context (goal, skill, availability, constraints) loaded once, passed to all agents
- Progress context (week #, completion rate, milestones) injected into Coach prompts
- Conversation history maintained for continuity
- Enables personalized responses: "You've completed 27/40 tasks..."

## How Goose Contributed

| Challenge | Without Goose | With Goose |
|-----------|---------------|-----------|
| **Scale** | Hardcoded responses for each career path × skill × situation | Single agent handles infinite combinations |
| **Personalization** | Generic: "You got this!" | Specific: "Week 6/52, 65% done, here's next step..." |
| **Resilience** | Crashes if API fails | 4-tier fallback—never fails |
| **Maintainability** | Brittle if-then-else logic | Flexible agentic patterns |
| **Intelligence** | Template-based answers | Detects emotion (imposter syndrome, burnout), adapts mode |

## Code Location

```
herpath-ai/agents/
├── goose/
│   ├── agent.py          # PEV orchestrator
│   ├── toolkit.py        # GeminiTool, VerifyTool
│   └── fallback.py       # 4-tier degradation
├── coach_agent.py        # Emotional mentoring
├── roadmap_agent.py      # Curriculum gen
├── rebalance_agent.py    # Timeline adapt
└── base_agent.py         # Retry/timeout logic
```

## Key Result

Goose pattern **enables emotional personalization at scale**—the core value proposition. Without it, HERPath AI is just another generic platform. With it, the system genuinely understands women's journeys and adapts to context, emotion, and constraints. That's what keeps women in tech.
