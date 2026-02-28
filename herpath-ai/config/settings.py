"""
Application settings and configuration.
All API keys and credentials should be added to Streamlit secrets.
"""

import os
import streamlit as st

# =============================================================================
# LLM CONFIGURATION
# =============================================================================

# TODO: Add your OpenAI API key to Streamlit secrets as "OPENAI_API_KEY"
# TODO: Add your Anthropic API key to Streamlit secrets as "ANTHROPIC_API_KEY"

def get_openai_api_key():
    """Get OpenAI API key from secrets or environment."""
    try:
        return st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    except:
        return os.getenv("OPENAI_API_KEY", "")

def get_anthropic_api_key():
    """Get Anthropic API key from secrets or environment."""
    try:
        return st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))
    except:
        return os.getenv("ANTHROPIC_API_KEY", "")

# =============================================================================
# LLM PROVIDER SELECTION
# =============================================================================

# Options: "openai" or "anthropic"
LLM_PROVIDER = "openai"

# Model configurations
OPENAI_MODEL = "gpt-4-turbo-preview"
ANTHROPIC_MODEL = "claude-3-sonnet-20240229"

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
# FIREBASE CONFIGURATION PLACEHOLDER
# =============================================================================

"""
TODO: Add to .streamlit/secrets.toml:

[firebase_credentials]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = "YOUR_PRIVATE_KEY"
client_email = "YOUR_CLIENT_EMAIL"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL"

FIREBASE_DATABASE_URL = "https://YOUR_PROJECT_ID.firebaseio.com"
FIREBASE_WEB_API_KEY = "YOUR_WEB_API_KEY"

OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
"""
