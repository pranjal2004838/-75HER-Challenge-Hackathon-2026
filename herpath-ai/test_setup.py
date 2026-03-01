"""
Test script to verify HERPath AI setup and functionality.
Run with: python test_setup.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    errors = []
    
    try:
        # Config
        from config import settings
        print("  ✅ config.settings module")
    except Exception as e:
        errors.append(f"config.settings: {e}")
        print(f"  ❌ config.settings: {e}")
    
    try:
        from config import firebase_config
        print("  ✅ config.firebase_config module")
    except Exception as e:
        errors.append(f"config.firebase_config: {e}")
        print(f"  ⚠️ config.firebase_config: {e} (will use demo mode)")
    
    try:
        # Database
        from database import FirestoreClient, UserSchema, RoadmapSchema
        print("  ✅ database module")
    except Exception as e:
        errors.append(f"database: {e}")
        print(f"  ❌ database: {e}")
    
    try:
        # Agents
        from agents import SkillGapAgent, RoadmapAgent, RebalanceAgent, CoachAgent
        print("  ✅ agents module")
    except Exception as e:
        errors.append(f"agents: {e}")
        print(f"  ❌ agents: {e}")
    
    try:
        # UI
        from ui import render_onboarding, render_dashboard, render_roadmap
        print("  ✅ ui module")
    except Exception as e:
        errors.append(f"ui: {e}")
        print(f"  ❌ ui: {e}")
    
    try:
        # Utils
        from utils import RuleEngine, rule_engine
        print("  ✅ utils module")
    except Exception as e:
        errors.append(f"utils: {e}")
        print(f"  ❌ utils: {e}")
    
    return len(errors) == 0


def test_config():
    """Test configuration."""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config.settings import (
            SUPPORTED_ROLES, 
            SKILL_LEVELS, 
            TIMELINE_OPTIONS,
            get_openai_api_key,
            get_anthropic_api_key
        )
        
        print(f"  ✅ Supported roles: {len(SUPPORTED_ROLES)}")
        print(f"  ✅ Skill levels: {len(SKILL_LEVELS)}")
        print(f"  ✅ Timeline options: {len(TIMELINE_OPTIONS)}")
        
        # Check API keys (won't show actual keys)
        openai_key = get_openai_api_key()
        anthropic_key = get_anthropic_api_key()
        
        if openai_key:
            print(f"  ✅ OpenAI API key configured ({len(openai_key)} chars)")
        else:
            print("  ⚠️  OpenAI API key not set (demo mode will work)")
        
        if anthropic_key:
            print(f"  ✅ Anthropic API key configured ({len(anthropic_key)} chars)")
        else:
            print("  ⚠️  Anthropic API key not set")
        
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False


def test_agents():
    """Test agent initialization."""
    print("\n🤖 Testing agents...")
    
    try:
        from agents import SkillGapAgent, RoadmapAgent, RebalanceAgent, CoachAgent
        
        # Initialize agents
        skill_agent = SkillGapAgent(provider="openai")
        print("  ✅ SkillGapAgent initialized")
        
        roadmap_agent = RoadmapAgent(provider="openai")
        print("  ✅ RoadmapAgent initialized")
        
        rebalance_agent = RebalanceAgent(provider="openai")
        print("  ✅ RebalanceAgent initialized")
        
        coach_agent = CoachAgent(provider="openai")
        print("  ✅ CoachAgent initialized")
        
        return True
    except Exception as e:
        print(f"  ❌ Agent error: {e}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n📋 Testing data schemas...")
    
    try:
        from database.schema import UserSchema, RoadmapSchema, TaskSchema
        from datetime import datetime
        
        # Test user schema
        user = UserSchema(
            uid="test123",
            name="Test User",
            email="test@test.com",
            goal="AI Engineer",
            current_level="Beginner",
            weekly_hours=10,
            deadline_type="6 months",
            financial_constraint="Free Only",
            situation="Student",
            background_text="Test",
            onboarding_completed=False,
            created_at=datetime.utcnow()
        )
        print("  ✅ UserSchema validation works")
        
        # Test task schema
        task = TaskSchema(
            uid="test123",
            roadmap_version=datetime.utcnow(),
            week_number=1,
            task_id="w1_t1",
            title="Test task",
            task_type="learning",
            status="pending",
            created_at=datetime.utcnow()
        )
        print("  ✅ TaskSchema validation works")
        
        return True
    except Exception as e:
        print(f"  ❌ Schema error: {e}")
        return False


def test_rule_engine():
    """Test rule engine."""
    print("\n⚖️  Testing rule engine...")
    
    try:
        from utils import rule_engine
        
        # Mock data
        progress_data = {
            'completion_percentage': 50,
            'missed_tasks_count': 5,
            'total_tasks_count': 20,
            'pace_status': 'on_track',
            'current_week': 5
        }
        
        roadmap_data = {
            'total_weeks': 12,
            'current_week': 5,
            'phases': []
        }
        
        user_data = {
            'weekly_hours': 10,
            'deadline_type': '3 months'
        }
        
        # Evaluate
        recommendation = rule_engine.evaluate(
            progress_data=progress_data,
            user_data=user_data,
            roadmap_data=roadmap_data
        )
        
        print(f"  ✅ Rule engine evaluation: {recommendation.message[:50]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Rule engine error: {e}")
        return False


def test_dependencies():
    """Test that all required packages are installed."""
    print("\n📦 Testing dependencies...")
    
    # Required packages
    required = [
        ('streamlit', True),
        ('pydantic', True),
        ('openai', True),
    ]
    
    # Optional packages (for full features)
    optional = [
        ('firebase_admin', False),
        ('google.cloud.firestore', False),
        ('anthropic', False),
    ]
    
    all_required_installed = True
    
    for package, is_required in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED (required)")
            all_required_installed = False
    
    for package, _ in optional:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ⚠️ {package} - not installed (optional, demo mode available)")
    
    return all_required_installed


def main():
    """Run all tests."""
    print("=" * 60)
    print("HERPath AI - Setup Verification")
    print("=" * 60)
    
    results = {
        'Dependencies': test_dependencies(),
        'Imports': test_imports(),
        'Configuration': test_config(),
        'Agents': test_agents(),
        'Schemas': test_schemas(),
        'Rule Engine': test_rule_engine()
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Ready to run: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        print("   Tip: Run 'pip install -r requirements.txt' to install dependencies")
    
    print("\nNext steps:")
    print("1. Add API keys to .streamlit/secrets.toml")
    print("2. Run: streamlit run app.py")
    print("3. Click 'Enter Demo Mode' to test without Firebase")
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
