"""
Firebase configuration and initialization.
Leave credentials empty - will be loaded from Streamlit secrets.
"""

import streamlit as st
import json
import os

# Track initialization state
_firebase_initialized = False
_firebase_app = None

def _check_firebase_apps():
    """Check if Firebase has any initialized apps."""
    try:
        import firebase_admin
        # Try both ways for compatibility
        if hasattr(firebase_admin, '_apps'):
            return len(firebase_admin._apps) > 0
        elif hasattr(firebase_admin, 'apps'):
            return len(firebase_admin.apps) > 0
        return False
    except Exception:
        return False

def init_firebase():
    """Initialize Firebase app with credentials from Streamlit secrets."""
    global _firebase_initialized, _firebase_app
    
    if _firebase_initialized:
        return True
    
    try:
        import firebase_admin
        from firebase_admin import credentials
    except ImportError as e:
        st.warning(f"Firebase not installed: {e}. Running in demo mode.")
        return False
    
    if _check_firebase_apps():
        # Try to load from Streamlit secrets first
        try:
            if "firebase_credentials" in st.secrets:
                cred_dict = st.secrets["firebase_credentials"]
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': st.secrets.get("firebase_database_url", "")
                })
            else:
                # Fallback to environment variable or .env file
                cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON", "{}")
                if cred_json and cred_json != "{}":
                    cred_dict = json.loads(cred_json)
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': os.getenv("FIREBASE_DATABASE_URL", "")
                    })
                else:
                    st.warning("⚠️ Firebase credentials not configured. Running in demo mode.")
                    return False
        except Exception as e:
            st.error(f"Firebase initialization error: {str(e)}")
            return False
    
    _firebase_initialized = True
    return True

def get_firebase_app():
    """Get or initialize Firebase app."""
    global _firebase_app
    
    if not _check_firebase_apps():
        if not init_firebase():
            return None
    
    try:
        import firebase_admin
        return firebase_admin.get_app()
    except Exception:
        return None

def is_firebase_configured():
    """Check if Firebase is properly configured."""
    return _firebase_initialized and _check_firebase_apps()
