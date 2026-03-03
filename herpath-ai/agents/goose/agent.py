"""
GooseAgent - Main Agentic AI Orchestrator
==========================================

Implements Block's Goose-style agentic AI patterns for intelligent,
multi-step task execution with tool orchestration.

Key Features:
- Plan-Execute-Verify (PEV) loop for robust execution
- Tool orchestration with dependency resolution
- Automatic fallback to cached/template responses
- Comprehensive logging and observability
- Context-aware execution with state management

Architecture:
    User Request
         ↓
    [PLAN] - Agent reasons about what tools/steps needed
         ↓
    [EXECUTE] - Agent runs tools in sequence/parallel
         ↓
    [VERIFY] - Agent checks results and decides next action
         ↓
    Final Response (or loop back to PLAN)

Inspired by Block's Goose Framework.
"""

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum

from .toolkit import Toolkit, Tool, ToolResult, ToolStatus
from .fallback import FallbackManager, FallbackResponse, get_fallback_manager

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """States the agent can be in during execution."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExecutionStep:
    """Record of a single execution step."""
    tool_name: str
    inputs: Dict[str, Any]
    result: ToolResult
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool": self.tool_name,
            "inputs": self.inputs,
            "result": self.result.to_dict(),
            "timestamp": self.timestamp
        }


@dataclass
class AgentResult:
    """
    Final result from agent execution.
    
    Attributes:
        success: Whether the execution succeeded
        response: The main response (text or structured data)
        is_fallback: Whether this is a fallback response
        steps: List of execution steps taken
        metadata: Additional execution metadata
        execution_time_ms: Total execution time
    """
    success: bool
    response: Any
    is_fallback: bool = False
    steps: List[ExecutionStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "response": self.response,
            "is_fallback": self.is_fallback,
            "steps": [s.to_dict() for s in self.steps],
            "metadata": self.metadata,
            "execution_time_ms": self.execution_time_ms
        }
    
    @classmethod
    def success_result(cls, response: Any, **kwargs) -> "AgentResult":
        return cls(success=True, response=response, **kwargs)
    
    @classmethod
    def failure_result(cls, error: str, **kwargs) -> "AgentResult":
        return cls(success=False, response=error, **kwargs)
    
    @classmethod
    def fallback_result(cls, response: Any, **kwargs) -> "AgentResult":
        return cls(success=True, response=response, is_fallback=True, **kwargs)


class GooseAgent:
    """
    Main agentic AI orchestrator following Goose patterns.
    
    A GooseAgent:
    1. Takes a goal and context
    2. Plans which tools to use
    3. Executes tools with error handling
    4. Verifies results and retries if needed
    5. Falls back gracefully on failures
    
    Example:
        agent = GooseAgent(
            name="CoachAgent",
            toolkit=toolkit,
            max_steps=5
        )
        
        result = agent.execute(
            goal="Provide career coaching",
            context={"user": {...}, "mode": "feeling_stuck"}
        )
    """
    
    def __init__(
        self,
        name: str,
        toolkit: Optional[Toolkit] = None,
        fallback_manager: Optional[FallbackManager] = None,
        max_steps: int = 5,
        timeout_seconds: float = 30.0,
        retry_on_failure: bool = True,
        max_retries: int = 2
    ):
        """
        Initialize the GooseAgent.
        
        Args:
            name: Agent identifier
            toolkit: Collection of tools available to the agent
            fallback_manager: Manager for fallback responses
            max_steps: Maximum execution steps before timeout
            timeout_seconds: Maximum execution time
            retry_on_failure: Whether to retry failed steps
            max_retries: Maximum retry attempts per step
        """
        self.name = name
        self.toolkit = toolkit or Toolkit()
        self.fallback_manager = fallback_manager or get_fallback_manager()
        self.max_steps = max_steps
        self.timeout_seconds = timeout_seconds
        self.retry_on_failure = retry_on_failure
        self.max_retries = max_retries
        
        self._state = AgentState.IDLE
        self._steps: List[ExecutionStep] = []
        self._context: Dict[str, Any] = {}
        self._start_time: float = 0.0
    
    @property
    def state(self) -> AgentState:
        """Current agent state."""
        return self._state
    
    def execute(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
        tools_to_use: Optional[List[str]] = None
    ) -> AgentResult:
        """
        Execute the agent with a goal and context.
        
        This is the main entry point for agent execution.
        Implements the Plan-Execute-Verify (PEV) loop.
        
        Args:
            goal: What the agent should accomplish
            context: Additional context for execution
            tools_to_use: Optional list of specific tools to use
            
        Returns:
            AgentResult with execution outcome
        """
        self._start_time = time.time()
        self._steps = []
        self._context = context or {}
        self._context["goal"] = goal
        
        try:
            # Phase 1: Planning
            self._state = AgentState.PLANNING
            plan = self._plan(goal, tools_to_use)
            
            if not plan:
                return self._get_fallback_result(goal)
            
            # Phase 2: Execution
            self._state = AgentState.EXECUTING
            result = self._execute_plan(plan)
            
            # Phase 3: Verification
            self._state = AgentState.VERIFYING
            verified_result = self._verify_result(result)
            
            self._state = AgentState.COMPLETED
            return verified_result
            
        except Exception as e:
            logger.exception(f"Agent {self.name} execution failed: {e}")
            self._state = AgentState.FAILED
            return self._get_fallback_result(goal)
        finally:
            elapsed = (time.time() - self._start_time) * 1000
            logger.info(f"Agent {self.name} completed in {elapsed:.2f}ms")
    
    def _plan(
        self,
        goal: str,
        tools_to_use: Optional[List[str]] = None
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Plan which tools to use and in what order.
        
        For now, this uses a simple deterministic planning.
        Future: Could use LLM-based planning for complex goals.
        
        Returns:
            List of (tool_name, parameters) tuples
        """
        if tools_to_use:
            # Use specified tools in order
            return [(tool, {}) for tool in tools_to_use if tool in self.toolkit]
        
        # Default: Use all available tools
        available = self.toolkit.list_tools()
        
        # Prioritize tools based on common patterns
        priority_order = [
            "fetch_context",
            "fetch_user_data",
            "fetch_roadmap",
            "call_gemini",
            "gemini_generate",
            "verify_response",
            "format_response"
        ]
        
        plan = []
        for tool_name in priority_order:
            if tool_name in available:
                plan.append((tool_name, {}))
        
        # Add remaining tools
        for tool_name in available:
            if tool_name not in [p[0] for p in plan]:
                plan.append((tool_name, {}))
        
        return plan
    
    def _execute_plan(
        self,
        plan: List[Tuple[str, Dict[str, Any]]]
    ) -> Optional[Any]:
        """
        Execute the planned tools in sequence.
        
        Args:
            plan: List of (tool_name, parameters) to execute
            
        Returns:
            Final result from execution or None on failure
        """
        step_count = 0
        last_result = None
        
        for tool_name, params in plan:
            # Check limits
            if step_count >= self.max_steps:
                logger.warning(f"Agent {self.name} hit max steps limit")
                break
            
            elapsed = time.time() - self._start_time
            if elapsed > self.timeout_seconds:
                logger.warning(f"Agent {self.name} hit timeout")
                break
            
            # Merge context into params
            execution_params = {**self._context, **params}
            if last_result is not None:
                execution_params["previous_result"] = last_result
            
            # Execute with retries
            result = self._execute_with_retry(tool_name, execution_params)
            
            # Record step
            step = ExecutionStep(
                tool_name=tool_name,
                inputs=execution_params,
                result=result
            )
            self._steps.append(step)
            step_count += 1
            
            # Handle result
            if result.is_success:
                last_result = result.data
            elif result.is_failure and not self.retry_on_failure:
                # Stop on failure if no retry
                logger.warning(f"Tool {tool_name} failed: {result.error}")
                break
        
        return last_result
    
    def _execute_with_retry(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> ToolResult:
        """
        Execute a tool with retry logic.
        
        Args:
            tool_name: Name of tool to execute
            params: Parameters for the tool
            
        Returns:
            ToolResult from execution
        """
        last_result = None
        
        for attempt in range(self.max_retries + 1):
            result = self.toolkit.execute(tool_name, **params)
            last_result = result
            
            if result.is_success:
                return result
            
            # Check if retryable
            if not self._is_retryable_error(result.error):
                return result
            
            # Backoff before retry
            if attempt < self.max_retries:
                wait_time = 2 ** attempt
                logger.info(f"Retrying {tool_name} in {wait_time}s")
                time.sleep(wait_time)
        
        return last_result or ToolResult.failure("Max retries exceeded")
    
    def _is_retryable_error(self, error: Optional[str]) -> bool:
        """Check if an error is retryable."""
        if not error:
            return False
        
        error_lower = error.lower()
        retryable_patterns = [
            "timeout", "connection", "rate_limit", "429",
            "500", "502", "503", "504", "temporarily"
        ]
        
        return any(pattern in error_lower for pattern in retryable_patterns)
    
    def _verify_result(self, result: Optional[Any]) -> AgentResult:
        """
        Verify and package the execution result.
        
        Args:
            result: Raw result from execution
            
        Returns:
            Verified AgentResult
        """
        elapsed = (time.time() - self._start_time) * 1000
        
        if result is None:
            return self._get_fallback_result(self._context.get("goal", ""))
        
        # Check if result is meaningful
        if isinstance(result, str) and len(result.strip()) < 10:
            return self._get_fallback_result(self._context.get("goal", ""))
        
        if isinstance(result, dict) and not result:
            return self._get_fallback_result(self._context.get("goal", ""))
        
        return AgentResult.success_result(
            response=result,
            steps=self._steps,
            execution_time_ms=elapsed,
            metadata={
                "agent": self.name,
                "steps_taken": len(self._steps),
                "tools_used": [s.tool_name for s in self._steps]
            }
        )
    
    def _get_fallback_result(self, goal: str) -> AgentResult:
        """
        Get a fallback result when execution fails.
        
        Args:
            goal: Original goal for context
            
        Returns:
            Fallback AgentResult
        """
        elapsed = (time.time() - self._start_time) * 1000
        
        # Determine agent type from name
        agent_type = self._infer_agent_type()
        mode = self._context.get("mode", "general")
        
        fallback = self.fallback_manager.get_fallback(
            agent_type=agent_type,
            mode=mode,
            user_context=self._context
        )
        
        return AgentResult.fallback_result(
            response=fallback.content,
            steps=self._steps,
            execution_time_ms=elapsed,
            metadata={
                "agent": self.name,
                "fallback_tier": fallback.tier.value,
                "original_goal": goal
            }
        )
    
    def _infer_agent_type(self) -> str:
        """Infer agent type from name."""
        name_lower = self.name.lower()
        
        if "coach" in name_lower:
            return "coach"
        elif "roadmap" in name_lower:
            return "roadmap"
        elif "skill" in name_lower or "gap" in name_lower:
            return "skill_gap"
        elif "rebalance" in name_lower:
            return "rebalance"
        
        return "coach"  # Default
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent's toolkit."""
        self.toolkit.register(tool)
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get the execution log for debugging."""
        return [step.to_dict() for step in self._steps]
    
    def reset(self) -> None:
        """Reset agent state for new execution."""
        self._state = AgentState.IDLE
        self._steps = []
        self._context = {}
        self._start_time = 0.0
