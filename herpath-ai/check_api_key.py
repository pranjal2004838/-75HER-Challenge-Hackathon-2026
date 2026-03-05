"""
Stream-Safe Gemini API Check
Shows ONLY what system key is being used (safe for debugging)
"""

import streamlit as st
import sys
import os

st.set_page_config(page_title="API Key Check", layout="wide")

st.title("🔍 Gemini API Key Diagnostic")
st.markdown("This page shows what API key your app is currently using")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1️⃣ Streamlit Secrets")
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            st.success(f"✓ Found")
            st.code(f"{key[:12]}...{key[-8:]}")
        else:
            st.error("✗ Not found in secrets")
    except Exception as e:
        st.error(f"Error: {e}")

with col2:
    st.subheader("2️⃣ Agent Loader")
    try:
        from agents.base_agent import get_gemini_api_key
        key = get_gemini_api_key()
        if key:
            st.success(f"✓ Loaded")
            st.code(f"{key[:12]}...{key[-8:]}")
            
            # Validate key format (never hardcode actual keys!)
            if key.startswith("AIzaSy") and len(key) > 30:
                st.success("✅ **Key format valid**")
            else:
                st.warning("⚠️ Key format looks unusual")
        else:
            st.error("✗ No key loaded")
    except Exception as e:
        st.error(f"Error: {e}")

with col3:
    st.subheader("3️⃣ API Connectivity")
    try:
        import requests
        from agents.base_agent import get_gemini_api_key
        
        key = get_gemini_api_key()
        if not key:
            st.error("No key to test")
        else:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={key}"
            payload = {
                "contents": [{"parts": [{"text": "Say OK"}]}],
                "generationConfig": {"temperature": 0.1, "maxOutputTokens": 5}
            }
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    st.success("✓ API Working (200)")
                    st.code("HTTP 200 OK")
                elif response.status_code == 403:
                    st.error("✗ Access Denied (403)")
                    error_data = response.json()
                    msg = error_data.get("error", {}).get("message", "Unknown")
                    if "leaked" in msg.lower():
                        st.error("🚨 Key is BLACKLISTED")
                    st.code(msg[:100])
                else:
                    st.error(f"✗ Failed ({response.status_code})")
                    st.code(response.text[:100])
            except requests.exceptions.Timeout:
                st.error("✗ Timeout")
            except Exception as e:
                st.error(f"✗ Error: {str(e)[:50]}")
    except Exception as e:
        st.error(f"Setup error: {e}")

st.divider()

st.subheader("📋 What to Check")
st.markdown("""
1. **If all 3 show GREEN** → API is working, demo is ready! 🎉
2. **If 2 shows OLD KEY** → Streamlit Cloud secrets updated but app not restarted
3. **If 3 shows 403** → Key is blacklisted (get new one from https://ai.google.dev/)

**Next Steps:**
- If not all green, reboot the app in Streamlit Cloud Settings
- Hard refresh browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
""")
