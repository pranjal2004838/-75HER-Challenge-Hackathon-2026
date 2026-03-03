"""
Agents module for HERPath AI.

This module provides AI agents powered by the Goose-style agentic framework.
All agents integrate with the Gemini API and include automatic fallback responses.

Architecture:
- BaseAgent: Core agent class with Goose integration
- CoachAgent: Contextual career coaching
- RoadmapAgent: Learning roadmap generation
- SkillGapAgent: Skill gap analysis
- RebalanceAgent: Progress optimization

Goose Framework:
- GooseAgent: Main orchestrator
- Toolkit: Tool collection management
- Tools: GeminiTool, VerifyTool
- FallbackManager: Graceful degradation
"""

from .base_agent import BaseAgent, get_gemini_api_key
from .skill_gap_agent import SkillGapAgent, get_fallback_skills
from .roadmap_agent import RoadmapAgent, get_fallback_roadmap
from .rebalance_agent import RebalanceAgent, simple_rebalance
from .coach_agent import CoachAgent, get_fallback_response

# Export Goose components
try:
    from .goose import GooseAgent, Toolkit, Tool, ToolResult, AgentResult
    from .goose import FallbackManager, FallbackResponse
    from .goose.tools import GeminiTool, VerifyTool
    GOOSE_AVAILABLE = True
except ImportError:
    GOOSE_AVAILABLE = False
    GooseAgent = None
    Toolkit = None

__all__ = [
    'BaseAgent',
    'get_gemini_api_key',
    'SkillGapAgent',
    'get_fallback_skills',
    'RoadmapAgent',
    'get_fallback_roadmap',
    'RebalanceAgent',
    'simple_rebalance',
    'CoachAgent',
    'get_fallback_response',
    'GOOSE_AVAILABLE',
]

# Add Goose exports if available
if GOOSE_AVAILABLE:
    __all__.extend([
        'GooseAgent',
        'Toolkit',
        'Tool',
        'ToolResult',
        'AgentResult',
        'FallbackManager',
        'FallbackResponse',
        'GeminiTool',
        'VerifyTool',
    ])
