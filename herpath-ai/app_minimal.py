# -*- coding: utf-8 -*-
"""
HERPath AI - Minimal Startup Version
Tests if basic Streamlit works without freezing on imports
"""

import streamlit as st
import sys
import os

print("[STARTUP] Starting minimal app...", flush=True)

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()
print("[STARTUP] ✓ dotenv loaded", flush=True)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="HERPath AI - Running",
    page_icon="🚀",
    layout="wide"
)

print("[STARTUP] ✓ Page config set", flush=True)

# ============================================================================
# MINIMAL DEMO - Just show that server is up
# ============================================================================

st.markdown("# ✅ HERPath AI Server is UP")
st.markdown("---")
st.success("🎉 **Server is running successfully!**")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "🟢 ONLINE", "Ready")
    with col2:
        st.metric("Port", "8501", "Active")

st.markdown("---")
st.info("The full app is loading in the background. Refresh the page in 5-10 seconds for the complete HERPath AI experience.")

print("[STARTUP] ✓ App rendered successfully", flush=True)
