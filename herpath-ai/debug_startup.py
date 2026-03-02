#!/usr/bin/env python
"""Debug script to trace what's blocking Streamlit startup."""

import sys
import time

print("[0s] Starting debug startup trace", flush=True)

# Test 1: Basic imports
try:
    print("[1s] Importing sys, os...", flush=True)
    import os
    time.sleep(0.5)
    print("[1.5s] ✓ sys, os imported", flush=True)
except Exception as e:
    print(f"[ERROR] Failed: {e}", flush=True)

# Test 2: Load dotenv
try:
    print("[2s] Loading dotenv...", flush=True)
    from dotenv import load_dotenv
    load_dotenv()
    time.sleep(0.5)
    print("[2.5s] ✓ dotenv loaded", flush=True)
except Exception as e:
    print(f"[ERROR] dotenv failed: {e}", flush=True)

# Test 3: Import Streamlit
try:
    print("[3s] Importing streamlit...", flush=True)
    import streamlit as st
    time.sleep(0.5)
    print("[3.5s] ✓ streamlit imported", flush=True)
except Exception as e:
    print(f"[ERROR] streamlit failed: {e}", flush=True)
    sys.exit(1)

# Test 4: Try to configure Streamlit
try:
    print("[4s] Configuring streamlit...", flush=True)
    st.set_page_config(page_title="Debug", layout="wide")
    time.sleep(0.5)
    print("[4.5s] ✓ streamlit configured", flush=True)
except Exception as e:
    print(f"[ERROR] config failed: {e}", flush=True)

# Test 5: Import custom modules
try:
    print("[5s] Importing custom config...", flush=True)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config.firebase_config import init_firebase as fb_init
    time.sleep(0.5)
    print("[5.5s] ✓ config imported", flush=True)
except Exception as e:
    print(f"[ERROR] config import failed: {e}", flush=True)

# Test 6: Import UI
try:
    print("[6s] Importing UI modules...", flush=True)
    from ui import render_resources
    time.sleep(0.5)
    print("[6.5s] ✓ UI imported", flush=True)
except Exception as e:
    print(f"[ERROR] UI import failed: {e}", flush=True)

# Test 7: Render simple page
try:
    print("[7s] Rendering page...", flush=True)
    st.write("✓ Debug startup complete!")
    time.sleep(0.5)
    print("[7.5s] ✓ Page rendered", flush=True)
except Exception as e:
    print(f"[ERROR] render failed: {e}", flush=True)

print("[8s] All tests passed!", flush=True)
