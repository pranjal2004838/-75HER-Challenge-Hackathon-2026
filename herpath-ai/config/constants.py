"""
Configuration Constants - HERPath AI
===================================

Centralized configuration for all application constants.
Prevents hardcoding and makes the app more maintainable.
"""

from typing import Dict, List
import os

# ============================================================================
# API CONFIGURATION
# ============================================================================

class APIConfig:
    """API-related configuration."""
    
    # Gemini API
    GEMINI_MODEL: str = "gemini-3-flash-preview"
    GEMINI_ENDPOINT: str = "https://generativelanguage.googleapis.com/v1beta/models"
    GEMINI_MAX_TOKENS: int = 16384
    GEMINI_DEFAULT_TEMPERATURE: float = 0.7
    
    # Timeout settings
    API_TIMEOUT_SECONDS: int = 30
    MAX_API_RETRIES: int = 3
    EXPONENTIAL_BACKOFF_BASE: int = 2
    MAX_BACKOFF_SECONDS: int = 60
    
    # Rate limiting
    RATE_LIMIT_CALLS_PER_MINUTE: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

class AgentConfig:
    """Agent execution configuration."""
    
    MAX_AGENT_STEPS: int = 3
    AGENT_TIMEOUT_SECONDS: float = 45.0
    AGENT_MAX_RETRIES: int = 2
    
    # Response validation
    MIN_RESPONSE_LENGTH: int = 20
    MAX_RESPONSE_LENGTH: int = 50000
    
    # Fallback behavior
    ENABLE_FALLBACK: bool = True
    FALLBACK_CACHE_DURATION_SECONDS: int = 3600


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

class DatabaseConfig:
    """Database/Firestore configuration."""
    
    # Collection names
    COLLECTION_USERS: str = "users"
    COLLECTION_ROADMAPS: str = "roadmaps"
    COLLECTION_TASKS: str = "tasks"
    COLLECTION_PROGRESS: str = "progress"
    COLLECTION_CHAT_HISTORY: str = "chat_history"
    
    # Demo mode settings
    DEMO_USER_EMAIL: str = "demo@herpath.ai"
    DEMO_USER_NAME: str = "Demo User"
    
    # Query limits
    MAX_ROADMAP_HISTORY: int = 10
    MAX_CHAT_HISTORY: int = 100


# ============================================================================
# UI CONFIGURATION
# ============================================================================

class UIConfig:
    """UI/UX configuration."""
    
    # Colors
    PRIMARY_COLOR: str = "#6366F1"
    PRIMARY_DARK: str = "#4F46E5"
    SUCCESS_COLOR: str = "#10B981"
    ERROR_COLOR: str = "#EF4444"
    WARNING_COLOR: str = "#F59E0B"
    
    # Layout
    MAX_CONTAINER_WIDTH: int = 1400
    SIDEBAR_WIDTH: int = 280
    
    # Pagination
    TASKS_PER_PAGE: int = 10
    RESOURCES_PER_PAGE: int = 12


# ============================================================================
# ROADMAP CONFIGURATION
# ============================================================================

class RoadmapConfig:
    """Roadmap generation configuration."""
    
    # Supported goals
    SUPPORTED_GOALS: List[str] = [
        "AI Engineer",
        "ML Engineer",
        "Data Scientist",
        "Data Analyst",
        "Web Developer",
        "Mobile Developer",
        "DevOps Engineer",
        "Cloud Engineer",
        "Cybersecurity Specialist",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer"
    ]
    
    # Skill levels
    SKILL_LEVELS: List[str] = ["Beginner", "Intermediate", "Advanced"]
    
    # Timeline presets (in weeks)
    TIMELINE_PRESETS: Dict[str, int] = {
        "3 months": 12,
        "6 months": 26,
        "9 months": 39,
        "12 months": 52
    }
    
    # Weekly hours
    MIN_WEEKLY_HOURS: int = 2
    MAX_WEEKLY_HOURS: int = 40
    DEFAULT_WEEKLY_HOURS: int = 10
    
    # Financial constraints
    FINANCIAL_OPTIONS: List[str] = [
        "Free Only",
        "Mixed (Free preferred, paid okay)",
        "Budget ($0-$50/month)",
        "Comfortable ($50-$200/month)"
    ]
    
    # Situations
    SITUATION_OPTIONS: List[str] = [
        "Student",
        "Working Full-time",
        "Career Transition",
        "Career Break",
        "Freelancing"
    ]


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

class LoggingConfig:
    """Logging configuration."""
    
    # Log levels
    DEFAULT_LEVEL: str = "INFO"
    FILE_LEVEL: str = "DEBUG"
    CONSOLE_LEVEL: str = "INFO"
    
    # Log format
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    # Log file
    LOG_FILE: str = "herpath_ai.log"
    MAX_LOG_SIZE_MB: int = 10
    BACKUP_COUNT: int = 5


# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

class SecurityConfig:
    """Security-related configuration."""
    
    # API key validation
    MIN_API_KEY_LENGTH: int = 20
    MASK_API_KEY_CHARS: int = 4  # Show only last N chars
    
    # Session
    SESSION_TIMEOUT_MINUTES: int = 480  # 8 hours
    
    # Input validation
    MAX_INPUT_LENGTH: int = 5000
    PROHIBITED_PATTERNS: List[str] = [
        r"<script",
        r"javascript:",
        r"onclick=",
        r"onerror="
    ]


# ============================================================================
# FEATURE FLAGS
# ============================================================================

class FeatureFlags:
    """Feature toggles for gradual rollout."""
    
    ENABLE_GOOSE_FRAMEWORK: bool = True
    ENABLE_FIREBASE_AUTH: bool = False  # Simplified auth for hackathon MVP
    ENABLE_ANALYTICS: bool = True
    ENABLE_CHAT_HISTORY: bool = True
    ENABLE_ROADMAP_EXPORT: bool = False  # Planned: PDF export
    ENABLE_EMAIL_NOTIFICATIONS: bool = False  # Planned: Email service
    ENABLE_DARK_MODE: bool = False  # Planned: Dark theme


# ============================================================================
# DEMO ACCOUNT CONFIGURATION
# ============================================================================

class DemoAccountConfig:
    """Pre-seeded demo account configuration."""
    
    # Demo user credentials
    EMAIL: str = "demo@herpath.ai"
    PASSWORD: str = "HERPath2026!"  # For demo purposes only
    NAME: str = "Maya Johnson"
    
    # Demo user profile
    GOAL: str = "AI Engineer"
    CURRENT_LEVEL: str = "Intermediate"
    WEEKLY_HOURS: int = 15
    DEADLINE_WEEKS: int = 26
    FINANCIAL_CONSTRAINT: str = "Mixed (Free preferred, paid okay)"
    SITUATION: str = "Career Transition"
    BACKGROUND: str = "Former data analyst with 3 years experience. Comfortable with Python and SQL, looking to transition into AI/ML engineering. Strong analytical skills, need guidance on deep learning frameworks and system design."
    
    # Demo roadmap progress
    CURRENT_WEEK: int = 4
    COMPLETION_PERCENTAGE: float = 16.5
    COMPLETED_TASKS: int = 7
    TOTAL_TASKS: int = 42
    MISSED_TASKS: int = 1


# ============================================================================
# ENVIRONMENT HELPERS
# ============================================================================

def get_env_or_default(key: str, default: str = "") -> str:
    """Get environment variable or return default."""
    return os.getenv(key, default)


def is_production() -> bool:
    """Check if running in production mode."""
    return os.getenv("ENVIRONMENT", "development").lower() == "production"


def is_demo_mode() -> bool:
    """Check if demo mode is enabled."""
    return os.getenv("DEMO_MODE", "false").lower() == "true"
