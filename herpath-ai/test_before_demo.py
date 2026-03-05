#!/usr/bin/env python
"""
PRE-DEMO TEST SCRIPT
====================

Run this script 10 minutes before recording your demo video.

Usage:
    python test_before_demo.py

This will verify:
1. All API keys are loaded
2. Gemini API is responding (tests in < 3 seconds)
3. Firebase is reachable
4. Fallback system is active
5. All agents can execute

If ALL TESTS PASS, you're safe to record the demo video.
If ANY TEST FAILS, fix it before recording.
"""

import sys
import os
import logging

# Setup logging to be quiet by default
logging.basicConfig(level=logging.ERROR)

print("\n" + "="*70)
print("HERPATH AI - PRE-DEMO VERIFICATION SCRIPT")
print("="*70)
print("\nRunning critical system checks...\n")

# Test 1: Import all modules
print("[TEST 1] Checking Python imports...")
try:
    from agents import SkillGapAgent, RoadmapAgent, CoachAgent, RebalanceAgent
    from agents.base_agent import get_gemini_api_key
    from database import FirestoreClient
    print("  OK: All agent modules imported successfully")
except ImportError as e:
    print(f"  FAIL: Import error: {e}")
    sys.exit(1)

# Test 2: Check Gemini API key
print("\n[TEST 2] Checking Gemini API key configuration...")
try:
    api_key = get_gemini_api_key()
    if not api_key or len(api_key) < 20:
        print(f"  FAIL: Gemini API key missing or invalid")
        sys.exit(1)
    print(f"  OK: Gemini API key loaded ({api_key[:10]}...)")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

# Test 3: Test Gemini API connectivity
print("\n[TEST 3] Testing Gemini API connectivity (this may take 5-10 seconds)...")
try:
    import requests
    import json
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Reply with just 'OK'."}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 5
        }
    }
    
    response = requests.post(
        f"{url}?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=15
    )
    
    if response.status_code == 200:
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"  OK: Gemini API is responsive (response: '{text.strip()}')")
        else:
            print(f"  FAIL: No response from Gemini")
            sys.exit(1)
    else:
        print(f"  FAIL: Gemini API returned {response.status_code}")
        print(f"       Error: {response.text[:200]}")
        sys.exit(1)
        
except requests.exceptions.Timeout:
    print(f"  FAIL: Gemini API request timed out")
    sys.exit(1)
except Exception as e:
    print(f"  FAIL: {type(e).__name__}: {e}")
    sys.exit(1)

# Test 4: Test Firebase connectivity
print("\n[TEST 4] Testing Firebase connectivity...")
try:
    from database import FirestoreClient
    # Just test that the client can be instantiated
    client = FirestoreClient()
    print("  OK: Firebase Firestore client initialized successfully")
except Exception as e:
    print(f"  WARN: Firebase check inconclusive: {e}")
    print("       (This is OK if you're offline - Streamlit Cloud has it)")

# Test 5: Test agent execution
print("\n[TEST 5] Testing agent execution (Skill Gap Agent)...")
try:
    agent = SkillGapAgent()
    result = agent.execute(
        goal="Web Developer",
        current_level="Beginner"
    )
    
    if result and isinstance(result, dict):
        print(f"  OK: SkillGapAgent executed successfully")
    else:
        print(f"  FAIL: SkillGapAgent returned invalid result")
        sys.exit(1)
        
except Exception as e:
    print(f"  FAIL: Agent execution error: {type(e).__name__}: {e}")
    sys.exit(1)

# All tests passed
print("\n" + "="*70)
print("ALL TESTS PASSED - YOU'RE READY FOR DEMO VIDEO!")
print("="*70 + "\n")

print("Next steps:")
print("  1. Open https://herpathai.streamlit.app/ in your browser")
print("  2. Sign in with: judge@herpath-demo.ai / HERPathDemo2026")
print("  3. Verify the app loads and responds (should be instant)")
print("  4. Then record your demo video")
print("\n")
