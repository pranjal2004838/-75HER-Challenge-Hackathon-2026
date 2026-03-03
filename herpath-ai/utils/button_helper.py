"""
Button helper to ensure proper styling across the app.
"""
import streamlit as st


def styled_button(label, key=None, help=None, use_container_width=False, type="primary", disabled=False):
    """
    Create a button with guaranteed white text on blue background.
    
    Args:
        label: Button text
        key: Unique key for the button
        help: Tooltip text
        use_container_width: Whether to use full container width
        type: Button type ("primary" or "secondary")
        disabled: Whether button is disabled
        
    Returns:
        bool: True if button was clicked
    """
    # Add CSS to force white text before the button
    if type == "primary":
        st.markdown("""
        <style>
        div[data-testid="stButton"] > button[kind="primary"] {
            color: white !important;
            background-color: rgb(99, 102, 241) !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            color: white !important;
            background-color: rgb(79, 70, 229) !important;
        }
        div[data-testid="stButton"] > button[kind="primary"]:active,
        div[data-testid="stButton"] > button[kind="primary"]:focus {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    return st.button(
        label,
        key=key,
        help=help,
        use_container_width=use_container_width,
        type=type,
        disabled=disabled
    )


def styled_form_submit(label, use_container_width=False, type="primary"):
    """
    Create a form submit button with guaranteed white text on blue background.
    
    Args:
        label: Button text
        use_container_width: Whether to use full container width
        type: Button type ("primary" or "secondary")
        
    Returns:
        bool: True if button was clicked
    """
    # Add CSS to force white text before the button
    if type == "primary":
        st.markdown("""
        <style>
        div[data-testid="stFormSubmitButton"] > button {
            color: white !important;
            background-color: rgb(99, 102, 241) !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            color: white !important;
            background-color: rgb(79, 70, 229) !important;
        }
        div[data-testid="stFormSubmitButton"] > button:active,
        div[data-testid="stFormSubmitButton"] > button:focus {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    return st.form_submit_button(
        label,
        use_container_width=use_container_width,
        type=type
    )
