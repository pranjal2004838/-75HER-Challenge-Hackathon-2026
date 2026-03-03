"""
Quick diagnostic test for Gemini API and Firebase
"""
import sys
import os

# Set UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_api():
    """Test if Gemini API is working."""
    print("\n=== Testing Gemini API ===")
    
    from agents import SkillGapAgent
    
    agent = SkillGapAgent()
    print(f"Agent provider: {agent.provider}")
    print(f"Agent model: {agent.model}")
    
    # Check if API key is available
    from agents.base_agent import get_gemini_api_key
    api_key = get_gemini_api_key()
    print(f"API key configured: {api_key is not None and len(api_key) > 10}")
    
    if not api_key or len(api_key) < 10:
        print("ERROR: Gemini API key not found or invalid")
        return False
    
    # Simple test
    print("\nTesting skill gap analysis...")
    try:
        result = agent.analyze(
            role="Web Developer",
            current_level="Beginner",
            weekly_hours=10,
            background_text="Complete beginner",
            situation="Career Pivot"
        )
        
        print(f"Result: {'SUCCESS' if result else 'FAILED'}")
        if result:
            print(f"Missing skills found: {len(result.get('missing_skills', []))}")
        else:
            print("Agent returned None")
        
        return result is not None
    except Exception as e:
        print(f"ERROR calling agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_firebase_save():
    """Test if Firebase/Firestore is actually saving data."""
    print("\n=== Testing Firebase/Firestore ===")
    
    from config.firebase_config import init_firebase, is_firebase_configured
    from database.firestore_client import FirestoreClient
    from datetime import datetime
    
    # Init Firebase
    firebase_ok = init_firebase()
    firebase_configured = is_firebase_configured()
    
    print(f"Firebase initialized: {firebase_ok}")
    print(f"Firebase configured: {firebase_configured}")
    
    # Try to save data
    db = FirestoreClient()
    print(f"Demo mode: {db._demo_mode}")
    
    test_uid = f"test_{datetime.now().timestamp()}"
    user_data = {
        'uid': test_uid,
        'name': 'Test User',
        'email': 'test@example.com',
        'created_at': datetime.now()
    }
    
    try:
        success = db.create_user(user_data)
        print(f"User creation: {'SUCCESS' if success else 'FAILED'}")
    except Exception as e:
        print(f"User creation: FAILED - {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    try:
        # Try to retrieve
        retrieved = db.get_user(test_uid)
        print(f"User retrieval: {'SUCCESS' if retrieved else 'FAILED'}")
        
        if retrieved:
            print(f"Retrieved user: {retrieved.get('name')}")
    except Exception as e:
        print(f"User retrieval: FAILED - {e}")
        retrieved = None
    
    return success and retrieved is not None


def main():
    print("="*70)
    print("  QUICK DIAGNOSTIC TEST")
    print("="*70)
    
    gemini_ok = test_gemini_api()
    firebase_ok = test_firebase_save()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Gemini API: {' OK' if gemini_ok else 'FAILED'}")
    print(f"Firebase:   {'OK' if firebase_ok else 'FAILED'}")
    
    return gemini_ok and firebase_ok


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
