# Goose Framework Guide

## What is Goose?

Goose is Block's agentic AI framework that implements the **Plan-Execute-Verify** pattern for intelligent, multi-step task execution.

**Reference:** https://block.github.io/goose

---

## Why Custom Goose Implementation?

HERPath AI uses a **custom Goose-style** implementation (not the published `goose-ai` package) because:

1. **Compatibility:** `goose-ai` requires Node.js and has Python 3.14 conflicts with pydantic v1
2. **Control:** Custom implementation gives full control over retry logic and fallback behavior
3. **Simplicity:** Lighter weight for hackathon MVP (no unnecessary dependencies)
4. **Learning:** Demonstrates deep understanding of agentic AI patterns

---

## Goose Pattern: Plan-Execute-Verify

```
┌─────────────────────────────────────────────┐
│             User Request                    │
└────────────────┬────────────────────────────┘
                 ↓
        ┌────────────────┐
        │      PLAN      │ Analyze request, choose tools
        └────────┬───────┘
                 ↓
        ┌────────────────┐
        │   EXECUTE      │ Run tools, handle errors
        └────────┬───────┘
                 ↓
        ┌────────────────┐
        │    VERIFY      │ Check quality, retry if needed
        └────────┬───────┘
                 ↓
        ┌────────────────┐
        │  Final Result  │ Success or Fallback
        └────────────────┘
```

---

## Implementation Details

### **GooseAgent** (`agents/goose/agent.py`)

Main orchestrator class:

```python
class GooseAgent:
    def __init__(
        self,
        name: str,
        toolkit: Toolkit,
        fallback_manager: FallbackManager,
        max_steps: int = 5,           # Max iterations
        timeout_seconds: float = 45.0, # Global timeout
        retry_on_failure: bool = True,
        max_retries: int = 2          # Per-tool retries
    ):
        pass
    
    def execute(
        self,
        goal: str,
        context: dict
    ) -> AgentResult:
        """
        Execute goal using Plan-Execute-Verify loop.
        
        Returns: AgentResult with success flag, response, and metadata.
        """
        pass
```

**AgentResult:**
```python
@dataclass
class AgentResult:
    success: bool
    response: Any
    is_fallback: bool = False
    steps: List[ExecutionStep] = []  # Audit trail
    metadata: Dict[str, Any] = {}
    execution_time_ms: float = 0.0
```

---

### **Toolkit** (`agents/goose/toolkit.py`)

Tool registry and orchestration:

```python
class Toolkit:
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
    
    def get(self, tool_name: str) -> Tool:
        return self.tools.get(tool_name)
    
    def execute(self, tool_name: str, inputs: dict) -> ToolResult:
        tool = self.get(tool_name)
        return tool.execute(**inputs)
```

**Built-in Tools:**

1. **GeminiTool** - Call Google Gemini API
   ```python
   tool.execute(
       prompt="User message",
       system_prompt="Role definition",
       temperature=0.7
   )
   ```

2. **VerifyTool** - Validate LLM outputs
   ```python
   tool.execute(
       response="LLM output",
       schema=ExpectedSchema
   )
   ```

---

### **FallbackManager** (`agents/goose/fallback.py`)

Handles graceful degradation:

```python
class FallbackManager:
    def get_fallback(self, agent_name: str, mode: str) -> str:
        """Return hardcoded response for unavailable LLM."""
        pass
    
    def detect_api_failure(self, error: Exception) -> bool:
        """Check if error is transient (retry) vs. permanent (fallback)."""
        pass
```

**Fallback Triggers:**
- API timeout (>45s)
- Connection error
- Invalid JSON response
- Rate limit (429)

---

## Execution Flow Example

### **Coach Agent Execution:**

```python
# 1. PLAN
coach = CoachAgent()
prompt = coach.build_prompt(
    user_state={...},
    roadmap_state={...},
    chat_message="I'm stuck"
)

# 2. EXECUTE
toolkit = Toolkit([GeminiTool(), VerifyTool()])
result = toolkit.execute(
    "gemini_generate",
    {"prompt": prompt, "system_prompt": coach.system_prompt}
)

# 3. VERIFY
if result.status == ToolStatus.SUCCESS:
    response = result.output
    verified = toolkit.execute("verify", {"response": response})
    if verified.status == ToolStatus.SUCCESS:
        return AgentResult.success_result(response)

# 4. FALLBACK
fallback = fallback_manager.get_fallback("CoachAgent", "feeling_stuck")
return AgentResult.fallback_result(fallback)
```

---

## Retry Strategy

All agents use **exponential backoff**:

```
Attempt 1: Immediate
↓ Error
Attempt 2: Wait 1 second
↓ Error
Attempt 3: Wait 2 seconds
↓ Error (timeout or 3 retries reached)
→ Fallback Response
```

**Configuration:**
```python
agent = GooseAgent(
    max_retries=2,           # 3 attempts total
    timeout_seconds=45.0,    # Global timeout
    retry_on_failure=True    # Retry on error
)
```

---

## Response Validation

All LLM responses are validated:

```python
# Invalid JSON response
response = "{ broken json"
verified = verify_tool.execute(response=response, schema=RoadmapSchema)
# Result: ToolStatus.INVALID_FORMAT → Retry or Fallback

# Valid response
response = '{"total_weeks": 26, "phases": [...]}'
verified = verify_tool.execute(response=response, schema=RoadmapSchema)
# Result: ToolStatus.SUCCESS → Return response
```

---

## Custom Tool Example

To add a **new tool** to the toolkit:

```python
from agents.goose.toolkit import Tool, ToolResult, ToolStatus

class MyCustomTool(Tool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    def execute(self, input_param: str) -> ToolResult:
        try:
            result = do_something(input_param)
            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=result
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                error=str(e)
            )

# Register in toolkit
toolkit.add_tool(MyCustomTool())

# Use in agent
result = toolkit.execute("my_tool", {"input_param": "value"})
```

---

## Monitoring & Debugging

### **Audit Trail**

Each agent execution returns `steps`:

```python
result = agent.execute(goal="...", context={...})

for step in result.steps:
    print(f"Tool: {step.tool_name}")
    print(f"Input: {step.inputs}")
    print(f"Status: {step.result.status}")
    print(f"Output: {step.result.output}")
    print(f"Time: {step.timestamp}")
```

### **Logging**

```python
import logging
logger = logging.getLogger("agents.goose")

# DEBUG: Detailed execution flow
# INFO: Agent start/success/fallback
# ERROR: Exceptions and timeouts

logger.debug(f"Planning execution for {goal}")
logger.info(f"CoachAgent completed in 2.4s")
logger.error(f"Gemini API timeout after 45s")
```

---

## Performance Notes

- **Plan step:** <100ms
- **Execute step:** 3-25s (depends on LLM call)
- **Verify step:** <500ms
- **Fallback generation:** <50ms

**Total execution:** 3-45 seconds (with timeout)

---

## Comparison to Official Goose

| Aspect | Custom | Official goose-ai |
|--------|--------|------------------|
| **Dependency** | None (pure Python) | Node.js required |
| **Python 3.14 compat** | ✅ Yes | ❌ has issues |
| **Customization** | ✅ Full control | ⚠️ Limited |
| **Size** | ~400 LOC | ~2000 LOC |
| **Learning curve** | Quick | Steeper |
| **Community** | None (custom) | Active |

---

## Future Enhancements

- [ ] Parallel tool execution (execute multiple tools in parallel)
- [ ] Support for chained agents (agent outputs → next agent)
- [ ] Tool result caching (avoid repeated calls)
- [ ] User-defined tools (let users add custom logic)
- [ ] Cost tracking (monitor Gemini API spend)

---

## References

- **Official Goose:** https://block.github.io/goose
- **Plan-Execute-Verify Pattern:** https://arxiv.org/abs/2305.04364
- **Agentic AI Trends:** https://www.anthropic.com/news/introducing-claude
