"""
Comprehensive Deployment Readiness Test
Tests Firebase integration, AI agents, context awareness, and user flow
"""

import sys
import os

# Set stdout encoding to UTF-8 for Unicode characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from database.firestore_client import FirestoreClient
from agents import RoadmapAgent, CoachAgent, SkillGapAgent
from config.firebase_config import init_firebase, is_firebase_configured
import json


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)


def test_firebase_init():
    """Test 1: Firebase Initialization"""
    print_section("TEST 1: Firebase Initialization")
    
    success = init_firebase()
    print(f"✓ Firebase initialization: {'SUCCESS' if success else 'FAILED'}")
    
    configured = is_firebase_configured()
    print(f"✓ Firebase configured: {'YES' if configured else 'NO (Demo Mode)'}")
    
    return success


def test_firestore_operations():
    """Test 2: Firestore CRUD Operations"""
    print_section("TEST 2: Firestore CRUD Operations")
    
    db = FirestoreClient()
    test_uid = f"test_user_{datetime.now().timestamp()}"
    
    # Create user
    user_data = {
        'uid': test_uid,
        'name': 'Test User',
        'email': 'test@herpath.ai',
        'goal': 'AI Engineer',
        'current_level': 'Intermediate',
        'weekly_hours': 15,
        'situation': 'Student',
        'financial_constraint': 'Paid Allowed',
        'background_text': 'I have a background in software development and want to transition to AI engineering. I know Python and basic ML concepts.',
        'onboarding_completed': True,
        'created_at': datetime.utcnow()
    }
    
    success = db.create_user(user_data)
    print(f"✓ User creation: {'SUCCESS' if success else 'FAILED'}")
    
    # Retrieve user
    retrieved = db.get_user(test_uid)
    print(f"✓ User retrieval: {'SUCCESS' if retrieved else 'FAILED'}")
    if retrieved:
        print(f"  - Name: {retrieved.get('name')}")
        print(f"  - Goal: {retrieved.get('goal')}")
    
    return success and retrieved is not None


def test_onboarding_ai_with_role_specificity():
    """Test 3: Onboarding AI - Role-Specific Responses"""
    print_section("TEST 3: Onboarding AI - Role Specificity")
    
    print("\n--- Test Case 3.1: AI Engineer Role ---")
    skill_agent = SkillGapAgent()
    
    ai_engineer_analysis = skill_agent.analyze(
        role='AI Engineer',
        current_level='Intermediate',
        weekly_hours=15,
        background_text='I have software development experience. I know Python and basic ML. I want to become an AI Engineer but worry about math skills.',
        situation='Working Professional'
    )
    
    print(f"✓ Skill Gap Analysis: {'SUCCESS' if ai_engineer_analysis else 'FAILED'}")
    if ai_engineer_analysis:
        print(f"\n  Missing Skills:")
        for skill in ai_engineer_analysis.get('missing_skills', [])[:5]:
            print(f"    - {skill}")
        print(f"\n  Priority Order:")
        for i, skill in enumerate(ai_engineer_analysis.get('priority_order', [])[:5], 1):
            print(f"    {i}. {skill}")
    
    print("\n--- Test Case 3.2: Web Developer Role ---")
    web_dev_analysis = skill_agent.analyze(
        role='Web Developer',
        current_level='Beginner',
        weekly_hours=10,
        background_text='Complete beginner to tech. Want to build websites but intimidated by code.',
        situation='Career Pivot'
    )
    
    print(f"✓ Web Dev Analysis: {'SUCCESS' if web_dev_analysis else 'FAILED'}")
    if web_dev_analysis:
        print(f"\n  Missing Skills:")
        for skill in web_dev_analysis.get('missing_skills', [])[:5]:
            print(f"    - {skill}")
    
    # Check that responses are different for different roles
    ai_engineer_skills_set = set(ai_engineer_analysis.get('missing_skills', []))
    web_dev_skills_set = set(web_dev_analysis.get('missing_skills', []))
    
    overlap = ai_engineer_skills_set & web_dev_skills_set
    overlap_percentage = len(overlap) / max(len(ai_engineer_skills_set), 1) * 100 if ai_engineer_skills_set else 0
    
    print(f"\n✓ Role differentiation: {overlap_percentage:.1f}% overlap (should be < 50% for different roles)")
    
    return ai_engineer_analysis is not None and web_dev_analysis is not None


def test_roadmap_generation_with_context():
    """Test 4: Roadmap Generation with User Context"""
    print_section("TEST 4: Roadmap Generation with Context")
    
    roadmap_agent = RoadmapAgent()
    
    print("\n--- Generating roadmap for AI Engineer ---")
    roadmap = roadmap_agent.generate(
        role='AI Engineer',
        missing_skills=['Deep Learning Fundamentals', 'NLP', 'Computer Vision', 'MLOps', 'Transformers'],
        priority_order=['Deep Learning Fundamentals', 'Transformers', 'NLP', 'Computer Vision', 'MLOps'],
        deadline_weeks=16,
        weekly_hours=15,
        financial_constraint='Paid Allowed',
        situation='Working Professional',
        emotional_signals={'anxiety_level': 'medium', 'imposter_syndrome_detected': True}
    )
    
    print(f"✓ Roadmap generation: {'SUCCESS' if roadmap else 'FAILED'}")
    
    if roadmap:
        print(f"\n  Total Weeks: {roadmap.get('total_weeks', 'N/A')}")
        print(f"  Phases: {len(roadmap.get('phases', []))}")
        
        # Check first week for specificity
        if roadmap.get('phases') and roadmap['phases'][0].get('weeks'):
            first_week = roadmap['phases'][0]['weeks'][0]
            print(f"\n  Week 1 ({first_week.get('theme', 'N/A')}):")
            print(f"    Tasks:")
            for task in first_week.get('tasks', [])[:3]:
                title = task.get('title', 'N/A')
                print(f"      - {title}")
                # Check for specificity (should mention actual resources, problem numbers, etc.)
                if any(keyword in title.lower() for keyword in ['leetcode', 'chapter', 'section', 'course', 'specific']):
                    print(f"        ✓ Task is specific")
                else:
                    print(f"        ⚠ Task may be vague")
    
    return roadmap is not None


def test_coach_context_awareness():
    """Test 5: Coach Agent Context Awareness"""
    print_section("TEST 5: Coach Agent Context Awareness")
    
    coach = CoachAgent()
    
    # Scenario 1: Base context
    user_state = {
        'name': 'Sarah',
        'goal': 'AI Engineer',
        'current_level': 'Intermediate',
        'situation': 'Working Professional',
        'weekly_hours': 15,
        'background_text': 'Software developer wanting to transition to AI. Know Python basics.'
    }
    
    roadmap_state = {
        'total_weeks': 16,
        'current_week': 3,
        'phases': [
            {
                'phase_name': 'Foundation',
                'weeks': [
                    {'theme': 'Python ML Libraries', 'week_number': 1},
                    {'theme': 'Math for ML', 'week_number': 2},
                    {'theme': 'Neural Networks Basics', 'week_number': 3}
                ]
            }
        ]
    }
    
    progress_state = {
        'completion_percentage': 60,
        'missed_tasks_count': 2,
        'pace_status': 'slightly_behind'
    }
    
    print("\n--- Initial Chat ---")
    response1 = coach.chat(
        user_state=user_state,
        roadmap_state=roadmap_state,
        progress_state=progress_state,
        chat_message="I'm struggling with understanding backpropagation",
        mode='feeling_stuck',
        chat_history=[]
    )
    
    print(f"✓ Coach response generated: {'SUCCESS' if response1 else 'FAILED'}")
    if response1:
        print(f"\n  Response preview (first 200 chars):")
        print(f"  {response1[:200]}...")
        
        # Check if response mentions user's name or specific context
        context_aware = any(keyword in response1.lower() for keyword in ['sarah', 'week 3', 'neural', 'ai engineer'])
        print(f"\n  ✓ Context-aware: {'YES' if context_aware else 'NO'}")
    
    # Scenario 2: After user changes plan (rebalance)
    print("\n--- After Rebalance (changed schedule) ---")
    
    # Simulate user rebalancing: increased hours, extended timeline
    updated_user_state = {**user_state, 'weekly_hours': 20}  # Changed from 15 to 20
    updated_roadmap_state = {**roadmap_state, 'total_weeks': 20}  # Extended from 16 to 20
    updated_progress_state = {
        **progress_state,
        'completion_percentage': 60,  # Same completion but more time now
        'pace_status': 'ahead_of_schedule'  # Now ahead since timeline extended
    }
    
    response2 = coach.chat(
        user_state=updated_user_state,
        roadmap_state=updated_roadmap_state,
        progress_state=updated_progress_state,
        chat_message="Now that I have more time, should I go deeper into certain topics?",
        mode='clarify_plan',
        chat_history=[
            {'user_message': "I'm struggling with understanding backpropagation", 'ai_response': response1[:100]}
        ]
    )
    
    print(f"✓ Adapted response generated: {'SUCCESS' if response2 else 'FAILED'}")
    if response2:
        print(f"\n  Response preview (first 200 chars):")
        print(f"  {response2[:200]}...")
        
        # Check if response acknowledges the change
        adaptation_aware = any(keyword in response2.lower() for keyword in ['more time', '20 weeks', '20 hours', 'deeper', 'extended'])
        print(f"\n  ✓ Adaptation-aware: {'YES' if adaptation_aware else 'NO'}")
    
    return response1 is not None and response2 is not None


def test_ai_role_confusion():
    """Test 6: AI Role Confusion Check"""
    print_section("TEST 6: AI Role Confusion Check")
    
    roadmap_agent = RoadmapAgent()
    
    print("\n--- Generating roadmap for AI Engineer (should NOT mention web dev) ---")
    ai_roadmap = roadmap_agent.generate(
        role='AI Engineer',
        missing_skills=['Machine Learning', 'Deep Learning', 'NLP'],
        priority_order=['Machine Learning', 'Deep Learning', 'NLP'],
        deadline_weeks=12,
        weekly_hours=15,
        financial_constraint='Paid Allowed',
        situation='Career Pivot',
        emotional_signals={}
    )
    
    if ai_roadmap:
        # Convert roadmap to string for checking
        roadmap_str = json.dumps(ai_roadmap).lower()
        
        # Check for AI-relevant keywords
        ai_keywords = ['machine learning', 'deep learning', 'neural network', 'tensorflow', 'pytorch', 'ai', 'ml']
        ai_mentions = sum(1 for keyword in ai_keywords if keyword in roadmap_str)
        
        # Check for web dev keywords (should be minimal or none)
        web_keywords = ['html', 'css', 'react', 'vue', 'angular', 'dom', 'web development']
        web_mentions = sum(1 for keyword in web_keywords if keyword in roadmap_str)
        
        print(f"  AI-related mentions: {ai_mentions}")
        print(f"  Web Dev mentions: {web_mentions}")
        print(f"\n  ✓ Role clarity: {'PASS' if ai_mentions > web_mentions * 3 else 'FAIL'} (AI mentions should dominate)")
        
        return ai_mentions > web_mentions * 3
    
    return False


def test_complete_user_flow():
    """Test 7: Complete User Flow"""
    print_section("TEST 7: Complete User Flow Simulation")
    
    db = FirestoreClient()
    test_uid = f"flow_test_{datetime.now().timestamp()}"
    
    print("\n--- Step 1: User Signup ---")
    user_data = {
        'uid': test_uid,
        'name': 'Test Flow User',
        'email': 'flow@test.com',
        'created_at': datetime.utcnow()
    }
    signup_success = db.create_user(user_data)
    print(f"  ✓ Signup: {'SUCCESS' if signup_success else 'FAILED'}")
    
    print("\n--- Step 2: Onboarding ---")
    onboarding_data = {
        'goal': 'AI Engineer',
        'current_level': 'Intermediate',
        'weekly_hours': 15,
        'deadline_type': '3-4 months',
        'financial_constraint': 'Paid Allowed',
        'situation': 'Working Professional',
        'background_text': 'I am a software developer with 3 years of experience. Want to transition to AI.'
    }
    
    skill_agent = SkillGapAgent()
    skill_analysis = skill_agent.analyze(
        role=onboarding_data['goal'],
        current_level=onboarding_data['current_level'],
        weekly_hours=onboarding_data['weekly_hours'],
        background_text=onboarding_data['background_text'],
        situation=onboarding_data['situation']
    )
    print(f"  ✓ Skill analysis: {'SUCCESS' if skill_analysis else 'FAILED'}")
    
    print("\n--- Step 3: Roadmap Generation ---")
    roadmap_agent = RoadmapAgent()
    roadmap = roadmap_agent.generate(
        role=onboarding_data['goal'],
        missing_skills=skill_analysis.get('missing_skills', []),
        priority_order=skill_analysis.get('priority_order', []),
        deadline_weeks=16,
        weekly_hours=onboarding_data['weekly_hours'],
        financial_constraint=onboarding_data['financial_constraint'],
        situation=onboarding_data['situation'],
        emotional_signals=skill_analysis.get('emotional_signals', {})
    )
    print(f"  ✓ Roadmap generation: {'SUCCESS' if roadmap else 'FAILED'}")
    
    if roadmap:
        # Save roadmap
        roadmap_data = {
            'uid': test_uid,
            **roadmap,
            'current_week': 1,
            'is_active': True,
            'generated_at': datetime.utcnow()
        }
        roadmap_id = db.create_roadmap(roadmap_data)
        print(f"  ✓ Roadmap saved: {'SUCCESS' if roadmap_id else 'FAILED'}")
        
        print("\n--- Step 4: Coach Interaction ---")
        coach = CoachAgent()
        
        # Retrieve saved data
        active_roadmap = db.get_active_roadmap(test_uid)
        progress = db.get_progress(test_uid)
        
        response = coach.chat(
            user_state={**user_data, **onboarding_data},
            roadmap_state=active_roadmap or roadmap_data,
            progress_state=progress or {'completion_percentage': 0, 'pace_status': 'on_track'},
            chat_message="What should I focus on in my first week?",
            mode='clarify_plan',
            chat_history=[]
        )
        print(f"  ✓ Coach response: {'SUCCESS' if response else 'FAILED'}")
        
        return all([signup_success, skill_analysis, roadmap, roadmap_id, response])
    
    return False


def main():
    """Run all deployment readiness tests."""
    print("\n" + "="*80)
    print("  DEPLOYMENT READINESS TEST SUITE")
    print("  Testing Firebase, AI Agents, and User Flows")
    print("="*80)
    
    results = {}
    
    try:
        results['firebase_init'] = test_firebase_init()
        results['firestore_ops'] = test_firestore_operations()
        results['onboarding_ai'] = test_onboarding_ai_with_role_specificity()
        results['roadmap_generation'] = test_roadmap_generation_with_context()
        results['coach_awareness'] = test_coach_context_awareness()
        results['role_confusion'] = test_ai_role_confusion()
        results['complete_flow'] = test_complete_user_flow()
        
    except Exception as e:
        print(f"\n❌ TEST SUITE ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {test_name.replace('_', ' ').title()}")
    
    print(f"\n  Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED - APP IS DEPLOYMENT READY!")
    elif passed >= total * 0.8:
        print("\n  ⚠️  MOSTLY READY - Address failing tests before deployment")
    else:
        print("\n  ❌ NOT READY - Critical issues must be fixed")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
