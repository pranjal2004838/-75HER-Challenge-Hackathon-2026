"""
Application settings and configuration.
All API keys and credentials should be added to Streamlit secrets or .env.
"""

import os
import streamlit as st

# =============================================================================
# LLM CONFIGURATION (Gemini-only)
# =============================================================================

# NOTE: Gemini API key should be added to .env as "GEMINI_API_KEY" or Streamlit secrets

def get_gemini_api_key():
    """Get Gemini API key from secrets or environment."""
    try:
        return st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    except:
        return os.getenv("GEMINI_API_KEY", "")

# =============================================================================
# LLM PROVIDER SELECTION
# =============================================================================

# NOTE: Only Gemini is supported now
LLM_PROVIDER = "gemini"

# Model configurations
GEMINI_MODEL = "gemini-3-flash-preview"

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

APP_NAME = "HERPath AI"
APP_TAGLINE = "Transform vague goals into structured, trackable career roadmaps"

# Supported roles (V1 only)
SUPPORTED_ROLES = [
    "AI Engineer",
    "Web Developer",
    "Data Analyst",
    "Career Re-entry into Tech"
]

# Skill levels
SKILL_LEVELS = ["Beginner", "Intermediate", "Advanced"]

# Timeline options
TIMELINE_OPTIONS = {
    "Flexible": None,
    "3 months": 12,
    "6 months": 26,
    "1 year": 52
}

# Financial constraints
FINANCIAL_OPTIONS = [
    "Free Only",
    "Mixed (Free preferred, paid okay)",
    "Paid Allowed"
]

# Current situation options
SITUATION_OPTIONS = [
    "Student",
    "Working Professional",
    "Career Break",
    "Transitioning from another field"
]

# =============================================================================
# ADAPTIVE RULE ENGINE THRESHOLDS
# =============================================================================

# If missed tasks exceed this percentage in 2 weeks, trigger rebalance suggestion
MISSED_TASK_THRESHOLD_PERCENT = 30

# Minimum weekly hours (below this, extend timeline significantly)
MIN_WEEKLY_HOURS = 3

# Maximum weekly hours (reasonable cap)
MAX_WEEKLY_HOURS = 40

# =============================================================================
# UI CONFIGURATION
# =============================================================================

# Sidebar navigation items
NAV_ITEMS = {
    "dashboard": {"icon": "🏠", "label": "Dashboard"},
    "roadmap": {"icon": "🗺️", "label": "Roadmap"},
    "progress": {"icon": "📊", "label": "Progress"},
    "coach": {"icon": "🤖", "label": "AI Coach"},
    "settings": {"icon": "⚙️", "label": "Settings"}
}

# Coach mode toggles
COACH_MODES = [
    "Clarify Plan",
    "I'm Feeling Stuck",
    "Interview Guidance"
]

# =============================================================================
# FIREBASE & GEMINI CONFIGURATION
# =============================================================================

"""
Required environment configuration:

.env file should contain:
- GEMINI_API_KEY = "your-gemini-api-key"
- FIREBASE_CREDENTIALS_JSON = {...service account JSON...}
- FIREBASE_DATABASE_URL = "https://your-project.firebaseio.com"

Or use .streamlit/secrets.toml with same keys.
"""


