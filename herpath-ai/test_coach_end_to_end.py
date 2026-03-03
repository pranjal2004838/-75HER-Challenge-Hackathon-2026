#!/usr/bin/env python3
"""
End-to-end test for AI Coach functionality.
Tests model availability, API key validity, and coach response generation.
"""

import os
import sys
import json
from datetime import datetime

# Set UTF-8 encoding
os.environ['PYTHONUTF8'] = '1'

def test_coach_agent():
    """Test the AI Coach agent with a sample user and message."""
    
    print("=" * 80)
    print("AI COACH END-TO-END TEST")
    print("=" * 80)
    print(f"Time: {datetime.now().isoformat()}\n")
    
    # Step 1: Import and validate environment
    print("STEP 1: Checking environment setup...")
    try:
        from agents.coach_agent import CoachAgent
        print("✓ CoachAgent imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import CoachAgent: {e}")
        return False
    
    # Step 2: Check API key
    print("\nSTEP 2: Verifying API key...")
    try:
        from agents.base_agent import get_gemini_api_key
        api_key = get_gemini_api_key()
        if api_key:
            # Show only preview
            preview = api_key[:10] + "..." + api_key[-10:]
            print(f"✓ API key found: {preview}")
        else:
            print("✗ API key is empty")
            return False
    except Exception as e:
        print(f"✗ Error checking API key: {e}")
        return False
    
    # Step 3: Create coach agent
    print("\nSTEP 3: Initializing CoachAgent...")
    try:
        coach = CoachAgent()
        print(f"✓ Agent initialized with model: {coach.model}")
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")
        return False
    
    # Step 4: Prepare test data
    print("\nSTEP 4: Preparing test user data...")
    test_user_state = {
        "name": "Test User",
        "goal": "Become an AI Engineer",
        "current_level": "Intermediate",
        "situation": "Working Professional",
        "weekly_hours": "15",
        "background_text": "Background in web development, new to AI/ML"
    }
    
    test_roadmap_state = {
        "total_weeks": 26,
        "current_week": 3,
        "phases": [
            {
                "phase_name": "Foundations",
                "weeks": [
                    {"week_number": 1},
                    {"week_number": 2},
                    {"week_number": 3}
                ]
            },
            {
                "phase_name": "Advanced Topics",
                "weeks": [
                    {"week_number": 4},
                    {"week_number": 5}
                ]
            }
        ]
    }
    
    test_progress_state = {
        "completion_percentage": 12,
        "missed_tasks_count": 1,
        "pace_status": "on_track"
    }
    
    test_message = "I'm finding the math concepts really hard. How can I get better at understanding linear algebra?"
    test_mode = "Clarify Plan"
    
    print("✓ Test data prepared")
    print(f"  - User: {test_user_state['name']}")
    print(f"  - Goal: {test_user_state['goal']}")
    print(f"  - Message: {test_message}")
    print(f"  - Mode: {test_mode}")
    
    # Step 5: Build prompt
    print("\nSTEP 5: Building coach prompt...")
    try:
        prompt = coach.build_prompt(
            user_state=test_user_state,
            roadmap_state=test_roadmap_state,
            progress_state=test_progress_state,
            chat_message=test_message,
            mode=test_mode,
            chat_history=[]
        )
        print("✓ Prompt built successfully")
        print(f"  - Prompt length: {len(prompt)} characters")
    except Exception as e:
        print(f"✗ Failed to build prompt: {e}")
        return False
    
    # Step 6: Call LLM
    print("\nSTEP 6: Calling Gemini API...")
    print("  - Endpoint: https://generativelanguage.googleapis.com/v1beta/models")
    print(f"  - Model: {coach.model}")
    print("  - Method: generateContent")
    
    try:
        response = coach.call_llm(prompt, temperature=0.7)
        
        if response:
            print("✅ SUCCESS: Received response from Gemini API")
            print(f"\nRESPONSE (first 500 chars):")
            print("-" * 80)
            print(response[:500])
            if len(response) > 500:
                print(f"... [{len(response) - 500} more characters]")
            print("-" * 80)
            return True
        else:
            print("✗ No response received from API")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"✗ API call failed: {error_msg}")
        
        # Parse common errors
        if "403" in error_msg or "PERMISSION_DENIED" in error_msg:
            print("\n⚠️  ERROR: 403 PERMISSION_DENIED")
            print("  - Your API key may be blocked or invalid")
            print("  - Action: Generate new key at https://aistudio.google.com/app/apikey")
        elif "404" in error_msg or "NOT_FOUND" in error_msg:
            print("\n⚠️  ERROR: 404 NOT_FOUND")
            print(f"  - Model '{coach.model}' not found or endpoint incorrect")
            print("  - Action: Run check_models.py to see available models")
        elif "400" in error_msg or "INVALID_ARGUMENT" in error_msg:
            print("\n⚠️  ERROR: 400 BAD_REQUEST")
            print("  - Invalid request format or parameters")
            print("  - Check: maxOutputTokens, temperature, model name")
        elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("\n⚠️  ERROR: 429 RATE_LIMIT")
            print("  - Too many requests to API")
            print("  - Action: Wait a moment and retry")
        elif "Connection" in error_msg or "timeout" in error_msg.lower():
            print("\n⚠️  ERROR: Network/Connection issue")
            print("  - Cannot reach Gemini API")
            print("  - Action: Check internet connection")
        else:
            print(f"\n⚠️  Unexpected error: {error_msg}")
        
        return False

def main():
    """Run the test."""
    success = test_coach_agent()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ AI COACH TEST PASSED - API is working!")
    else:
        print("❌ AI COACH TEST FAILED - See errors above")
    print("=" * 80)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
