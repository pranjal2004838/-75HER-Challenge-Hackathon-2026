"""
Test script to verify Gemini API key loading in Streamlit context
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 70)
print("STREAMLIT GEMINI API TEST")
print("=" * 70)

# Test 1: Check if secrets are available
print("\n[TEST 1] Checking Streamlit secrets availability...")
try:
    if hasattr(st, 'secrets'):
        print("  ✓ st.secrets is available")
        
        # Check if GEMINI_API_KEY exists
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            print(f"  ✓ GEMINI_API_KEY found in secrets")
            print(f"  ✓ Key (hidden): {key[:12]}...{key[-6:]}")
        else:
            print("  ✗ GEMINI_API_KEY not found in st.secrets")
            print("  Available keys:", list(st.secrets.keys())[:5])
    else:
        print("  ✗ st.secrets not available (not running in Streamlit?)")
except Exception as e:
    print(f"  ✗ Error accessing secrets: {e}")

# Test 2: Check agent's key loading
print("\n[TEST 2] Testing agent API key loading...")
try:
    from agents.base_agent import get_gemini_api_key
    
    loaded_key = get_gemini_api_key()
    if loaded_key:
        print(f"  ✓ Agent loaded key: {loaded_key[:12]}...{loaded_key[-6:]}")
        
        # Check if it's the NEW key
        if loaded_key == "AIzaSyC_NiP0jrW9tDtL3AU4XwiO3JnphqTMYmc":
            print("  ✓ KEY IS CORRECT - New key is loaded!")
        elif loaded_key == "AIzaSyAgCHTHi7rOuBm7Jp3o5DFAWgPY1Ah0ar8":
            print("  ✗ KEY IS OLD (BLACKLISTED) - Still loading compromised key!")
        else:
            print("  ? KEY IS UNKNOWN - Neither old nor new key")
    else:
        print("  ✗ Agent returned empty/None key")
except Exception as e:
    print(f"  ✗ Error loading from agent: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Direct API test
print("\n[TEST 3] Testing direct Gemini API call...")
try:
    import requests
    
    from agents.base_agent import get_gemini_api_key
    api_key = get_gemini_api_key()
    
    if not api_key:
        print("  ✗ No API key available to test")
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": "Say OK"}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 5}
        }
        
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            print(f"  ✓ API CALL SUCCESS (200 OK)")
            data = response.json()
            if "candidates" in data:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"  ✓ Response: '{text.strip()}'")
        elif response.status_code == 403:
            print(f"  ✗ API CALL FAILED: 403 PERMISSION DENIED")
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "")
            print(f"  ✗ Error: {error_msg}")
            
            if "leaked" in error_msg.lower():
                print("\n  🚨 CRITICAL: API key is BLACKLISTED/LEAKED!")
                print("  🚨 The key loaded is the OLD compromised key")
                print("  🚨 Streamlit Cloud secrets may not be updated yet")
        else:
            print(f"  ✗ API CALL FAILED: {response.status_code}")
            print(f"  Error: {response.text[:200]}")
            
except Exception as e:
    print(f"  ✗ Error testing API: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70 + "\n")
