"""
Firebase configuration and initialization.
Leave credentials empty - will be loaded from Streamlit secrets.
"""

import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import json
import os

def init_firebase():
    """Initialize Firebase app with credentials from Streamlit secrets."""
    
    if not firebase_admin.apps:
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
                    st.warning("⚠️ Firebase credentials not configured. Please add to Streamlit secrets.")
                    return False
        except Exception as e:
            st.error(f"❌ Firebase initialization failed: {str(e)}")
            return False
    
    return True

def get_firebase_app():
    """Get or initialize Firebase app."""
    if not firebase_admin.apps:
        if not init_firebase():
            return None
    return firebase_admin.get_app()
