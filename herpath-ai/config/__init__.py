"""Config module initialization."""
try:
    from .firebase_config import init_firebase, get_firebase_app, is_firebase_configured
except ImportError:
    # Firebase not available, provide stubs
    def init_firebase():
        return False
    def get_firebase_app():
        return None
    def is_firebase_configured():
        return False

from .settings import (
    get_openai_api_key,
    get_anthropic_api_key,
    LLM_PROVIDER,
    SUPPORTED_ROLES,
    SKILL_LEVELS,
    TIMELINE_OPTIONS,
    FINANCIAL_OPTIONS,
    SITUATION_OPTIONS
)
