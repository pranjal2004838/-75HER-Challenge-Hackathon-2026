"""
Toolkit Module - Tool Definitions and Management
================================================

Implements Goose-style tool patterns for defining executable
capabilities that agents can invoke during task execution.

A Toolkit is a collection of Tools. Each Tool:
- Has a name, description, and parameters schema
- Can be executed with validated inputs
- Returns structured ToolResult objects
- Supports both sync and async execution
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
from enum import Enum

logger = logging.getLogger(__name__)


class ToolStatus(Enum):
    """Status codes for tool execution."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"


@dataclass
class ToolResult:
    """
    Structured result from tool execution.
    
    Attributes:
        status: Execution status (success/failure/partial/timeout)
        data: The actual result data (any type)
        error: Error message if failed
        metadata: Additional execution metadata
        execution_time_ms: Time taken to execute in milliseconds
    """
    status: ToolStatus
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    
    @property
    def is_success(self) -> bool:
        return self.status == ToolStatus.SUCCESS
    
    @property
    def is_failure(self) -> bool:
        return self.status in (ToolStatus.FAILURE, ToolStatus.TIMEOUT)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "execution_time_ms": self.execution_time_ms
        }
    
    @classmethod
    def success(cls, data: Any, **metadata) -> "ToolResult":
        """Create a successful result."""
        return cls(status=ToolStatus.SUCCESS, data=data, metadata=metadata)
    
    @classmethod
    def failure(cls, error: str, **metadata) -> "ToolResult":
        """Create a failure result."""
        return cls(status=ToolStatus.FAILURE, error=error, metadata=metadata)
    
    @classmethod
    def timeout(cls, error: str = "Tool execution timed out") -> "ToolResult":
        """Create a timeout result."""
        return cls(status=ToolStatus.TIMEOUT, error=error)


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""
    name: str
    description: str
    param_type: str = "string"  # string, number, boolean, object, array
    required: bool = True
    default: Any = None
    enum: Optional[List[Any]] = None


class Tool(ABC):
    """
    Abstract base class for all tools.
    
    Tools are the building blocks of agentic AI - they represent
    discrete capabilities that an agent can invoke to complete tasks.
    
    Example:
        class MyTool(Tool):
            @property
            def name(self) -> str:
                return "my_tool"
            
            @property
            def description(self) -> str:
                return "Does something useful"
            
            def execute(self, **kwargs) -> ToolResult:
                result = do_something(kwargs.get("input"))
                return ToolResult.success(result)
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the tool does."""
        pass
    
    @property
    def parameters(self) -> List[ToolParameter]:
        """List of parameters the tool accepts."""
        return []
    
    @property
    def requires_context(self) -> bool:
        """Whether this tool needs agent context to execute."""
        return False
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ToolResult with execution outcome
        """
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> Optional[str]:
        """
        Validate input parameters.
        
        Returns None if valid, error message if invalid.
        """
        for param in self.parameters:
            if param.required and param.name not in params:
                return f"Missing required parameter: {param.name}"
            
            if param.name in params and param.enum:
                if params[param.name] not in param.enum:
                    return f"Invalid value for {param.name}. Must be one of: {param.enum}"
        
        return None
    
    def to_schema(self) -> Dict[str, Any]:
        """
        Convert tool to JSON schema for LLM function calling.
        
        Returns schema compatible with OpenAI/Gemini function calling format.
        """
        properties = {}
        required = []
        
        for param in self.parameters:
            properties[param.name] = {
                "type": param.param_type,
                "description": param.description
            }
            if param.enum:
                properties[param.name]["enum"] = param.enum
            if param.required:
                required.append(param.name)
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }


class Toolkit:
    """
    Collection of tools available to an agent.
    
    A Toolkit manages tool registration, lookup, and execution.
    It acts as the bridge between agent reasoning and tool capabilities.
    
    Example:
        toolkit = Toolkit([
            GeminiTool(),
            FetchDataTool(),
            VerifyTool()
        ])
        
        result = toolkit.execute("gemini_call", prompt="Hello")
    """
    
    def __init__(self, tools: Optional[List[Tool]] = None):
        """
        Initialize toolkit with optional list of tools.
        
        Args:
            tools: List of Tool instances to register
        """
        self._tools: Dict[str, Tool] = {}
        
        if tools:
            for tool in tools:
                self.register(tool)
    
    def register(self, tool: Tool) -> None:
        """Register a tool in the toolkit."""
        if tool.name in self._tools:
            logger.warning(f"Overwriting existing tool: {tool.name}")
        self._tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")
    
    def unregister(self, name: str) -> bool:
        """Remove a tool from the toolkit."""
        if name in self._tools:
            del self._tools[name]
            return True
        return False
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """Get list of registered tool names."""
        return list(self._tools.keys())
    
    def get_schemas(self) -> List[Dict[str, Any]]:
        """Get JSON schemas for all tools (for LLM function calling)."""
        return [tool.to_schema() for tool in self._tools.values()]
    
    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a tool by name with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Parameters to pass to the tool
            
        Returns:
            ToolResult from tool execution
        """
        import time
        
        tool = self.get(tool_name)
        if not tool:
            return ToolResult.failure(f"Tool not found: {tool_name}")
        
        # Validate parameters
        validation_error = tool.validate_params(kwargs)
        if validation_error:
            return ToolResult.failure(validation_error)
        
        # Execute with timing
        start_time = time.time()
        try:
            result = tool.execute(**kwargs)
            result.execution_time_ms = (time.time() - start_time) * 1000
            return result
        except Exception as e:
            logger.exception(f"Tool execution failed: {tool_name}")
            return ToolResult.failure(
                f"Tool execution error: {str(e)}",
                tool_name=tool_name,
                exception_type=type(e).__name__
            )
    
    def __len__(self) -> int:
        return len(self._tools)
    
    def __contains__(self, name: str) -> bool:
        return name in self._tools
    
    def __iter__(self):
        return iter(self._tools.values())
