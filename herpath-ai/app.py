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
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --background-color: #1E1E1E;
        --text-color: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a2e;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Card-like containers */
    .stExpander {
        border-radius: 10px;
        border: 1px solid #333;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #4ECDC4;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        border-radius: 15px;
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
    <div style="text-align: center; padding: 2rem;">
        <h1>🚀 HERPath AI</h1>
        <p style="font-size: 1.2rem; color: #888;">
            Transform your career goals into structured, trackable roadmaps
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab selection
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        _render_login_form()
    
    with tab2:
        _render_signup_form()
    
    # Demo mode option
    st.markdown("---")
    st.markdown("**Or try demo mode:**")
    if st.button("🎮 Enter Demo Mode", use_container_width=True):
        _enter_demo_mode()


def _render_login_form():
    """Render login form."""
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Your password")
        
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
        
        if submitted:
            if email and password:
                success, result = _authenticate_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.uid = result['uid']
                    st.session_state.user_email = email
                    st.session_state.user_name = result.get('name', email.split('@')[0])
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.error("Please enter email and password")


def _render_signup_form():
    """Render signup form."""
    
    with st.form("signup_form"):
        name = st.text_input("Your Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        
        if submitted:
            if not all([name, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords don't match")
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
        <div style="text-align: center; padding: 1rem;">
            <h2>🚀 HERPath AI</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        if st.session_state.get('user_name'):
            st.markdown(f"**👤 {st.session_state.user_name}**")
            if st.session_state.get('demo_mode'):
                st.caption("🎮 Demo Mode")
        
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
