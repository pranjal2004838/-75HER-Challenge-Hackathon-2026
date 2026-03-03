"""
HERPath AI Goose-Style Agentic Framework
=========================================

This module implements Block's Goose-inspired agentic AI patterns for
intelligent, multi-step task execution with tool orchestration.

Architecture:
- GooseAgent: Main orchestrator that plans and executes tool chains
- Toolkit: Collection of tools available to agents
- Tool: Individual executable capability
- FallbackManager: Graceful degradation when primary tools fail

Key Features:
- Agentic reasoning with plan-execute-verify loops
- Tool orchestration with dependency resolution
- Comprehensive fallback system for reliability
- Context-aware execution with state management

Usage:
    from agents.goose import GooseAgent, Toolkit
    
    agent = GooseAgent(
        name="Coach",
        toolkit=Toolkit([GeminiTool(), FetchDataTool()]),
        fallback_response="Sorry, I can't help right now."
    )
    
    result = agent.execute(goal="Help user with Python", context={...})

Inspired by Block's Goose Framework:
https://github.com/block/goose
"""

from .agent import GooseAgent, AgentResult
from .toolkit import Toolkit, Tool, ToolResult
from .fallback import FallbackManager, FallbackResponse

__all__ = [
    'GooseAgent',
    'AgentResult',
    'Toolkit',
    'Tool',
    'ToolResult',
    'FallbackManager',
    'FallbackResponse',
]

__version__ = "1.0.0"
__author__ = "HERPath AI Team"
