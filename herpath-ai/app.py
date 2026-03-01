# -*- coding: utf-8 -*-
"""
HERPath AI - Main Application Entry Point
A stateful, adaptive career execution system for women in tech.

Run with: streamlit run app.py
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="HERPath AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "HERPath AI - Adaptive Career Roadmaps for Women in Tech"
    }
)

# ============================================================================
# CLEAN MINIMAL UI - Premium Professional Design
# ============================================================================

st.markdown("""
<style>
    /* ========== MINIMAL COLOR SYSTEM ========== */
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --primary-light: #818CF8;
        --success: #10B981;
        --surface: #FFFFFF;
        --background: #FAFAFA;
        --text-primary: #0F172A;
        --text-secondary: #64748B;
        --border: #E2E8F0;
        --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    /* ========== GLOBAL ========== */
    .stApp {
        background: var(--background);
    }
    
    .main .block-container {
        padding: 2rem 4rem !important;
        max-width: 1400px !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ========== TYPOGRAPHY ========== */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    p {
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* ========== SIDEBAR - Clean Light ========== */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid var(--border) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: white !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 0.625rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        margin-bottom: 0.25rem !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--background) !important;
        border-color: var(--primary) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: var(--primary) !important;
        border-color: var(--primary) !important;
        color: white !important;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 0.625rem 1.25rem !important;
        transition: all 0.15s ease !important;
        border: 1px solid var(--border) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: var(--primary) !important;
        border-color: var(--primary) !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: var(--primary-dark) !important;
        border-color: var(--primary-dark) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--primary) !important;
        color: var(--primary) !important;
    }
    
    /* ========== CARDS ========== */
    .stExpander {
        background: white !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* ========== PROGRESS BARS ========== */
    .stProgress > div > div > div {
        background: var(--primary) !important;
    }
    
    .stProgress > div {
        background: var(--border) !important;
    }
    
    /* ========== METRICS ========== */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }
    
    /* ========== FORM INPUTS ========== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        padding: 0.625rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        border: none !important;
        background: transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom: 2px solid var(--primary) !important;
    }
    
    /* ========== ALERTS ========== */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
    }
    
    /* ========== CHECKBOXES ========== */
    .stCheckbox {
        margin: 0.5rem 0 !important;
    }
    
    /* ========== ADAPTIVE INDICATOR ========== */
    .adaptive-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--success);
        color: white;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'authenticated': False,
        'uid': None,
        'user_email': None,
        'user_name': None,
        'current_page': 'dashboard',
        'onboarding_completed': False,
        'firebase_initialized': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def init_firebase():
    """Initialize Firebase connection."""
    if st.session_state.get('firebase_initialized'):
        return True
    
    try:
        from config.firebase_config import init_firebase as fb_init
        success = fb_init()
        st.session_state.firebase_initialized = success
        return success
    except Exception as e:
        st.error(f"Firebase initialization error: {e}")
        return False


def get_db_client():
    """Get Firestore client instance."""
    if not st.session_state.get('firebase_initialized'):
        return None
    
    try:
        from database import FirestoreClient
        return FirestoreClient()
    except Exception as e:
        st.error(f"Database client error: {e}")
        return None


# ============================================================================
# AUTHENTICATION (Firebase Email/Password)
# ============================================================================

def render_auth_page():
    """Render login/signup page."""
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem; color: #0F172A;">🚀 HERPath AI</h1>
        <p style="font-size: 1.1rem; color: #64748B;">
            Transform your career goals into structured, trackable roadmaps
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab selection
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        _render_login_form()
    
    with tab2:
        _render_signup_form()


def _render_login_form():
    """Render login form."""
    
    with st.form("login_form"):
        st.markdown("#### Welcome back")
        st.markdown("Sign in to your account")
        st.markdown("")
        
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("")
        submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
        
        if submitted:
            if email and password:
                success, result = _authenticate_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.uid = result['uid']
                    st.session_state.user_email = email
                    st.session_state.user_name = result.get('name', email.split('@')[0])
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter both email and password")


def _render_signup_form():
    """Render signup form."""
    
    with st.form("signup_form"):
        st.markdown("#### Create your account")
        st.markdown("Start your career transformation journey")
        st.markdown("")
        
        name = st.text_input("Full Name", placeholder="Your name")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        st.markdown("")
        submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        
        if submitted:
            if not all([name, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, result = _create_user(name, email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.uid = result['uid']
                    st.session_state.user_email = email
                    st.session_state.user_name = name
                    st.success("✅ Account created successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")


def _authenticate_user(email: str, password: str):
    """
    Authenticate user with Firebase.
    
    TODO: Implement actual Firebase Authentication
    For now, using simplified authentication.
    """
    import hashlib
    
    # Generate a consistent UID from email
    uid = hashlib.sha256(email.encode()).hexdigest()[:28]
    
    # Check if user exists in Firestore
    db = get_db_client()
    if db:
        user = db.get_user(uid)
        if user:
            # In production, verify password with Firebase Auth
            # For demo, we'll accept any password for existing users
            return True, {'uid': uid, 'name': user.get('name', '')}
    
    # If Firebase is not configured, use demo mode
    if not st.session_state.get('firebase_initialized'):
        return True, {'uid': uid, 'name': email.split('@')[0]}
    
    return False, "User not found. Please sign up first."


def _create_user(name: str, email: str, password: str):
    """
    Create new user with Firebase.
    
    TODO: Implement actual Firebase Authentication
    For now, using simplified user creation.
    """
    import hashlib
    
    # Generate a consistent UID from email
    uid = hashlib.sha256(email.encode()).hexdigest()[:28]
    
    # If Firebase is configured, we'd create auth user here
    # For now, just return success
    return True, {'uid': uid, 'name': name}


def _enter_demo_mode():
    """Enter demo mode without authentication."""
    import hashlib
    
    demo_email = "demo@herpath.ai"
    demo_uid = hashlib.sha256(demo_email.encode()).hexdigest()[:28]
    
    st.session_state.authenticated = True
    st.session_state.uid = demo_uid
    st.session_state.user_email = demo_email
    st.session_state.user_name = "Demo User"
    st.session_state.demo_mode = True
    
    st.rerun()


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render the sidebar navigation."""
    
    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 1rem;">
            <h2 style="font-size: 1.5rem; font-weight: 600; color: #0F172A; margin: 0;">🚀 HERPath AI</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        if st.session_state.get('user_name'):
            st.markdown(f"**{st.session_state.user_name}**")
            st.caption(st.session_state.get('user_email', ''))
        
        st.markdown("---")
        
        # Navigation
        nav_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("🗺️", "Roadmap", "roadmap"),
            ("📊", "Progress", "progress"),
            ("🤖", "AI Coach", "coach"),
            ("⚙️", "Settings", "settings")
        ]
        
        for icon, label, page_key in nav_items:
            if st.button(
                f"{icon} {label}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == page_key else "secondary"
            ):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ============================================================================
# MAIN PAGE ROUTER
# ============================================================================

def render_main_content(db_client):
    """Render main content based on current page."""
    
    uid = st.session_state.get('uid')
    
    if not uid:
        st.error("No user ID found. Please log in again.")
        return
    
    # Check if user has completed onboarding
    user_data = db_client.get_user(uid) if db_client else None
    
    # Handle demo mode without Firestore
    if not user_data and st.session_state.get('demo_mode'):
        user_data = _get_demo_user_data()
    
    # Check onboarding status
    onboarding_completed = user_data.get('onboarding_completed', False) if user_data else False
    force_reonboard = st.session_state.get('force_reonboard', False)
    
    if not onboarding_completed or force_reonboard:
        # Show onboarding
        from ui import render_onboarding
        
        def on_onboard_complete():
            st.session_state.onboarding_completed = True
            if 'force_reonboard' in st.session_state:
                del st.session_state.force_reonboard
        
        render_onboarding(db_client, on_onboard_complete)
        return
    
    # Get user data and roadmap
    roadmap_data = db_client.get_active_roadmap(uid) if db_client else _get_demo_roadmap()
    progress_data = db_client.get_progress(uid) if db_client else _get_demo_progress()
    
    # Handle missing data
    if not roadmap_data:
        roadmap_data = _get_demo_roadmap()
    if not progress_data:
        progress_data = _get_demo_progress()
    
    # Router
    page = st.session_state.get('current_page', 'dashboard')
    
    try:
        if page == 'dashboard':
            from ui import render_dashboard
            render_dashboard(db_client, user_data, roadmap_data, progress_data)
        
        elif page == 'roadmap':
            from ui import render_roadmap
            render_roadmap(db_client, user_data, roadmap_data, progress_data)
        
        elif page == 'progress':
            from ui import render_progress
            render_progress(db_client, user_data, roadmap_data, progress_data)
        
        elif page == 'coach':
            from ui import render_coach
            render_coach(db_client, user_data, roadmap_data, progress_data)
        
        elif page == 'settings':
            from ui import render_settings
            render_settings(db_client, user_data, roadmap_data, progress_data)
        
        else:
            st.error(f"Unknown page: {page}")
    
    except Exception as e:
        _page_error(page, e)


def _page_error(page: str, error: Exception):
    """Handle page-level errors gracefully."""
    page_names = {
        'dashboard': 'Dashboard',
        'roadmap': 'Roadmap',
        'progress': 'Progress',
        'coach': 'AI Coach',
        'settings': 'Settings'
    }
    page_name = page_names.get(page, page.title())
    
    st.error(f"😕 Oops! We couldn't load the **{page_name}** page.")
    st.markdown("This might be a temporary issue. Try one of these:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retry", use_container_width=True, type="primary"):
            st.rerun()
    with col2:
        if st.button("🏠 Go to Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with st.expander("🔧 Technical Details", expanded=False):
        st.code(f"{type(error).__name__}: {error}", language="text")


# ============================================================================
# DEMO DATA (When Firestore is not available)
# ============================================================================

def _get_demo_user_data():
    """Get demo user data when Firestore is unavailable."""
    # Check if user completed onboarding in demo mode
    if 'demo_user_data' in st.session_state:
        return st.session_state.demo_user_data
    
    # Check if onboarding was completed this session
    if st.session_state.get('onboarding_completed'):
        return {
            'uid': st.session_state.get('uid', 'demo'),
            'name': st.session_state.get('user_name', 'Demo User'),
            'email': st.session_state.get('user_email', 'demo@herpath.ai'),
            'goal': st.session_state.get('onboarding_data', {}).get('goal', 'AI Engineer'),
            'current_level': st.session_state.get('onboarding_data', {}).get('current_level', 'Beginner'),
            'weekly_hours': st.session_state.get('onboarding_data', {}).get('weekly_hours', 10),
            'deadline_type': st.session_state.get('onboarding_data', {}).get('deadline_type', '6 months'),
            'financial_constraint': st.session_state.get('onboarding_data', {}).get('financial_constraint', 'Mixed (Free preferred, paid okay)'),
            'situation': st.session_state.get('onboarding_data', {}).get('situation', 'Career Break'),
            'background_text': st.session_state.get('onboarding_data', {}).get('background_text', ''),
            'onboarding_completed': True
        }
    
    # Default demo data (onboarding not yet completed)
    return {
        'uid': st.session_state.get('uid', 'demo'),
        'name': st.session_state.get('user_name', 'Demo User'),
        'email': st.session_state.get('user_email', 'demo@herpath.ai'),
        'goal': 'AI Engineer',
        'current_level': 'Beginner',
        'weekly_hours': 10,
        'deadline_type': '6 months',
        'financial_constraint': 'Mixed (Free preferred, paid okay)',
        'situation': 'Career Break',
        'background_text': 'Demo user exploring HERPath AI.',
        'onboarding_completed': False  # Force onboarding for fresh demo mode
    }


def _get_demo_roadmap():
    """Get demo roadmap data when Firestore is unavailable."""
    # Check if user completed onboarding in demo mode
    if 'demo_roadmap_data' in st.session_state:
        return st.session_state.demo_roadmap_data
    
    # Default demo roadmap
    return {
        'total_weeks': 26,
        'current_week': 3,
        'phases': [
            {
                'phase_name': 'Phase 1: Python & Programming Foundations',
                'phase_description': 'Build core programming skills',
                'weeks': [
                    {
                        'week_number': 1,
                        'focus_skill': 'Python Basics',
                        'tasks': [
                            'Complete Python syntax tutorial (3 hrs)',
                            'Practice variables and data types (2 hrs)',
                            'Write first Python program (1 hr)'
                        ],
                        'milestone': 'Write a program that processes user input',
                        'success_metric': 'Program runs without errors'
                    },
                    {
                        'week_number': 2,
                        'focus_skill': 'Control Flow & Functions',
                        'tasks': [
                            'Learn if/else and loops (2 hrs)',
                            'Understand functions (2 hrs)',
                            'Build a calculator program (2 hrs)'
                        ],
                        'milestone': 'Build a functional calculator',
                        'success_metric': 'Calculator handles basic operations'
                    },
                    {
                        'week_number': 3,
                        'focus_skill': 'Data Structures',
                        'tasks': [
                            'Master lists and dictionaries (3 hrs)',
                            'Practice list comprehensions (2 hrs)',
                            'Build a todo list app (2 hrs)'
                        ],
                        'milestone': 'Create a working todo list application',
                        'success_metric': 'App can add, remove, and list items'
                    }
                ]
            },
            {
                'phase_name': 'Phase 2: Machine Learning Basics',
                'phase_description': 'Introduction to ML concepts',
                'weeks': [
                    {
                        'week_number': 4,
                        'focus_skill': 'NumPy & Data Processing',
                        'tasks': [
                            'Learn NumPy arrays (3 hrs)',
                            'Practice data manipulation (2 hrs)',
                            'Complete NumPy exercises (2 hrs)'
                        ],
                        'milestone': 'Process a dataset with NumPy',
                        'success_metric': 'Successfully clean and transform data'
                    }
                ]
            }
        ]
    }


def _get_demo_progress():
    """Get demo progress data when Firestore is unavailable."""
    # Check if user completed onboarding in demo mode
    if 'demo_progress_data' in st.session_state:
        return st.session_state.demo_progress_data
    
    # Default demo progress
    return {
        'uid': st.session_state.get('uid', 'demo'),
        'completion_percentage': 15.5,
        'completed_tasks_count': 6,
        'total_tasks_count': 39,
        'missed_tasks_count': 1,
        'pace_status': 'on_track',
        'current_week': 3
    }


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point."""
    try:
        # Initialize session state
        init_session_state()
        
        # Initialize Firebase
        firebase_ready = init_firebase()
        
        # Check authentication
        if not st.session_state.get('authenticated'):
            render_auth_page()
            return
        
        # Render sidebar
        render_sidebar()
        
        # Get database client
        db_client = get_db_client()
        
        # Show warning if Firebase not configured
        if not firebase_ready or not db_client:
            st.warning("⚠️ Firebase not configured. Running in demo mode with limited functionality.")
        
        # Render main content
        render_main_content(db_client)
    
    except Exception as e:
        _show_error_page(
            "Something went wrong",
            "The app encountered an unexpected error. Please try refreshing the page.",
            e
        )


def _show_error_page(title: str, message: str, error: Exception = None):
    """Display a user-friendly error page instead of raw tracebacks."""
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem;">
        <h2>⚠️ {title}</h2>
        <p style="font-size: 1.1rem; color: #888; margin: 1rem 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show technical details in a collapsed section (useful for debugging)
    if error:
        with st.expander("🔧 Technical Details (for developers)", expanded=False):
            st.code(f"{type(error).__name__}: {error}", language="text")
    
    # Recovery actions
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Refresh App", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
