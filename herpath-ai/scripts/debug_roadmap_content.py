#!/usr/bin/env python3
"""Debug script to check what roadmap data actually exists in Firestore."""

import sys
import os

# Get the parent directory (herpath-ai root)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

import streamlit as st
from config import firebase_config
from database.firestore_client import FirestoreClient

# Initialize Firebase
firebase_config.init_firebase()
db_client = FirestoreClient()

print("\n" + "="*70)
print("🔍 ROADMAP CONTENT DEBUG")
print("="*70)

# Check all roadmaps in Firestore
print("\n1️⃣ ALL ROADMAPS IN FIRESTORE:")
print("-" * 70)
try:
    roadmaps = db_client.db.collection('roadmaps').stream()
    roadmap_count = 0
    for doc in roadmaps:
        roadmap_count += 1
        data = doc.to_dict()
        uid = data.get('uid', 'UNKNOWN')
        is_active = data.get('is_active', False)
        weeks = data.get('weeks', [])
        week_count = len(weeks)
        
        print(f"\n📋 Roadmap #{roadmap_count}")
        print(f"   UID: {uid}")
        print(f"   Active: {is_active}")
        print(f"   Weeks: {week_count}")
        
        if weeks:
            print(f"   Week 1 Focus Skill: {weeks[0].get('focus_skill', 'NOT SET')}")
            print(f"   Week 1 Resources: {len(weeks[0].get('resources', []))} items")
            
            if len(weeks) > 1:
                print(f"   Week 2 Focus Skill: {weeks[1].get('focus_skill', 'NOT SET')}")
    
    if roadmap_count == 0:
        print("   ❌ NO ROADMAPS FOUND IN FIRESTORE!")
    else:
        print(f"\n✅ Total roadmaps: {roadmap_count}")
        
except Exception as e:
    print(f"❌ Error querying roadmaps: {e}")

# Check test_user_herpath_demo specifically
print("\n\n2️⃣ TEST USER ROADMAP (test_user_herpath_demo):")
print("-" * 70)
try:
    test_roadmaps = db_client.db.collection('roadmaps').where('uid', '==', 'test_user_herpath_demo').stream()
    test_count = 0
    for doc in test_roadmaps:
        test_count += 1
        data = doc.to_dict()
        weeks = data.get('weeks', [])
        
        print(f"\n✅ Found test user roadmap!")
        print(f"   Weeks: {len(weeks)}")
        print(f"   Active: {data.get('is_active', False)}")
        
        if weeks:
            print(f"\n   📌 Week 1:")
            print(f"      Focus Skill: {weeks[0].get('focus_skill', 'NOT SET')}")
            print(f"      Resources: {weeks[0].get('resources', [])[:2]}")  # First 2
            
            print(f"\n   📌 Week 2:")
            print(f"      Focus Skill: {weeks[1].get('focus_skill', 'NOT SET')}")
            print(f"      Milestone: {weeks[1].get('milestone', 'NOT SET')}")
    
    if test_count == 0:
        print("   ❌ No roadmap for test_user_herpath_demo")
        
except Exception as e:
    print(f"Error querying test user: {e}")

# Check if fallback is being triggered
print("\n\n[3] CHECK ROADMAP GENERATION FALLBACK:")
print("-" * 70)
try:
    from agents.roadmap_agent import RoadmapAgent
    from config.settings import get_gemini_api_key
    
    key = get_gemini_api_key()
    if not key:
        print("   Note: No Gemini key detected - fallback will be used")
    else:
        print("   Gemini API key is configured")
    
    # Try to check the fallback function
    from agents.roadmap_agent import get_fallback_roadmap
    fallback = get_fallback_roadmap("Beginner", "AI Engineer")
    
    print(f"\n   Fallback roadmap structure:")
    print(f"   - Weeks: {len(fallback.get('weeks', []))}")
    if fallback.get('weeks'):
        week1 = fallback['weeks'][0]
        print(f"   - Week 1 focus_skill: {week1.get('focus_skill', 'NOT SET')}")
        print(f"   - Week 1 resources count: {len(week1.get('resources', []))}")
        
except Exception as e:
    print(f"   ⚠️ Could not check fallback: {e}")

# Check a real user's roadmap
print("\n\n4️⃣ RECENT USERS AND THEIR ROADMAPS:")
print("-" * 70)
try:
    users = db_client.db.collection('users').limit(3).stream()
    user_count = 0
    for user_doc in users:
        user_count += 1
        user_data = user_doc.to_dict()
        uid = user_data.get('uid', 'UNKNOWN')
        
        print(f"\n   👤 User #{user_count}: {uid[:8]}...")
        
        # Get their active roadmap
        roadmap_docs = db_client.db.collection('roadmaps')\
            .where('uid', '==', uid)\
            .where('is_active', '==', True)\
            .limit(1)\
            .stream()
        
        found_roadmap = False
        for rm_doc in roadmap_docs:
            found_roadmap = True
            rm_data = rm_doc.to_dict()
            weeks = rm_data.get('weeks', [])
            
            if weeks:
                print(f"      Weeks: {len(weeks)}")
                print(f"      Week 1 skill: {weeks[0].get('focus_skill', 'NOT SET')}")
                print(f"      Week 1 resources: {len(weeks[0].get('resources', []))} items")
                
                # Check if using placeholder
                if 'Core Skill' in str(weeks[0].get('focus_skill', '')):
                    print(f"      ⚠️ PLACEHOLDER DETECTED!")
                else:
                    print(f"      ✅ Real skill name detected")
        
        if not found_roadmap:
            print(f"      ❌ No active roadmap")
    
    if user_count == 0:
        print("   ❌ No users found")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("Debug complete. Check output above for issues.")
print("="*70 + "\n")
