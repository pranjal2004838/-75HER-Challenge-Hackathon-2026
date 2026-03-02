#!/usr/bin/env python3
"""
Test script to verify Firestore chat history and Gemini API fixes.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth as fb_auth
from google.cloud.firestore_v1 import FieldFilter
from agents.base_agent import BaseAgent
import json

print("\n" + "="*70)
print("[TEST] Chat Feature Fixes Verification")
print("="*70 + "\n")

# Test 1: Firestore Chat History Query
print("TEST 1: Firestore Chat History Query (No Index Required)")
print("-" * 70)

try:
    # Initialize Firebase
    if not firebase_admin.get_app():
        from database.firestore_client import db_client
    else:
        db_client = None
    
    from database.firestore_client import db_client
    
    # Try to get chat history for a test user
    test_uid = "test_user_001"
    print(f"  - Testing get_chat_history for user: {test_uid}")
    
    chat_history = db_client.get_chat_history(test_uid, limit=20)
    print(f"  ✓ Chat history query executed without index error")
    print(f"  ✓ Retrieved {len(chat_history)} messages")
    
    if len(chat_history) > 0:
        print(f"  ✓ Sample message: {chat_history[0].get('text', 'N/A')[:50]}...")
    
    test1_passed = True
    print("  [PASS] Firestore query works without composite index\n")
except Exception as e:
    test1_passed = False
    print(f"  [FAIL] Firestore query error: {str(e)}\n")

# Test 2: Gemini API Call
print("TEST 2: Gemini API LLM Call (Fixed Payload)")
print("-" * 70)

try:
    from agents.base_agent import BaseAgent
    from config import settings
    
    # Create an agent
    agent = BaseAgent(
        agent_type="coach",
        model="gemini-2.0-flash",
        system_prompt="You are a helpful career coach. Respond in 1-2 sentences."
    )
    
    # Test the LLM call
    print("  - Testing Gemini API with fixed payload format")
    print("  - Prompt: 'What are the top 3 skills for AI engineers?'")
    
    response = agent._call_gemini("What are the top 3 skills for AI engineers?", temperature=0.7)
    
    if response and len(response) > 0:
        print(f"  ✓ Gemini API call successful (Status 200)")
        print(f"  ✓ Response length: {len(response)} characters")
        print(f"  ✓ Sample response: {response[:80]}..." if len(response) > 80 else f"  ✓ Response: {response}")
        test2_passed = True
        print("  [PASS] Gemini API payload format is correct\n")
    else:
        test2_passed = False
        print(f"  [FAIL] Empty response from Gemini\n")
        
except Exception as e:
    test2_passed = False
    error_msg = str(e)
    print(f"  [FAIL] Gemini API error: {error_msg}\n")
    
    # Check if it's the old 400 error
    if "400" in error_msg or "Bad Request" in error_msg:
        print("  ⚠ Still getting 400 Bad Request error - payload format may need adjustment\n")

# Summary
print("="*70)
print("[SUMMARY] Chat Feature Fixes Test Results")
print("="*70)
print(f"Firestore Query (No Index):  {'✓ PASS' if test1_passed else '✗ FAIL'}")
print(f"Gemini API (Fixed Payload):  {'✓ PASS' if test2_passed else '✗ FAIL'}")
print("="*70)

if test1_passed and test2_passed:
    print("\n✓ ALL CHAT FEATURES WORKING - Both fixes verified!\n")
    sys.exit(0)
else:
    print("\n✗ Some tests failed - review errors above\n")
    sys.exit(1)
