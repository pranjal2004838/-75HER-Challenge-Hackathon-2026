#!/usr/bin/env python3
"""Simple debug script using Firestore directly."""

import os
import json
from google.cloud import firestore
from google.oauth2 import service_account

# Load Firebase credentials from .streamlit/secrets.toml
import tomllib

secrets_path = ".streamlit/secrets.toml"
if not os.path.exists(secrets_path):
    print("❌ .streamlit/secrets.toml not found")
    exit(1)

with open(secrets_path, 'rb') as f:
    secrets = tomllib.load(f)

# Get Firebase credentials
firebase_creds = secrets.get('firebase_credentials', {})
if not firebase_creds:
    print("❌ firebase_credentials not in secrets.toml")
    exit(1)

# Create Firestore client
try:
    credentials = service_account.Credentials.from_service_account_info(firebase_creds)
    db = firestore.Client(credentials=credentials, project=firebase_creds.get('project_id'))
    print("✅ Connected to Firestore\n")
except Exception as e:
    print(f"❌ Failed to connect to Firestore: {e}")
    exit(1)

print("="*70)
print("🔍 ROADMAP CONTENT DEBUG")
print("="*70)

# Check all roadmaps
print("\n1️⃣ ALL ROADMAPS IN FIRESTORE:")
print("-" * 70)

try:
    roadmaps = db.collection('roadmaps').stream()
    roadmap_list = list(roadmaps)
    print(f"Total roadmaps: {len(roadmap_list)}\n")
    
    for i, doc in enumerate(roadmap_list[:5], 1):  # Show first 5
        data = doc.to_dict()
        uid = data.get('uid', 'UNKNOWN')
        is_active = data.get('is_active', False)
        weeks = data.get('weeks', [])
        
        print(f"Roadmap #{i}:")
        print(f"  UID: {uid}")
        print(f"  Active: {is_active}")
        print(f"  Weeks: {len(weeks)}")
        
        if weeks:
            w1 = weeks[0]
            skill = w1.get('focus_skill', 'NOT SET')
            resources = len(w1.get('resources', []))
            print(f"  Week 1:")
            print(f"    Focus Skill: {skill}")
            print(f"    Resources: {resources}")
            
            # Check for placeholders
            if 'Core Skill' in str(skill) or 'Applied Skill' in str(skill):
                print(f"    ⚠️ PLACEHOLDER DETECTED!")
            else:
                print(f"    ✅ Real content")
        print()
        
except Exception as e:
    print(f"❌ Error: {e}\n")

# Check test user
print("\n2️⃣ TEST USER ROADMAP (test_user_herpath_demo):")
print("-" * 70)

try:
    test_docs = db.collection('roadmaps').where('uid', '==', 'test_user_herpath_demo').stream()
    test_list = list(test_docs)
    
    if test_list:
        print(f"✅ Found {len(test_list)} roadmap(s) for test user\n")
        for doc in test_list:
            data = doc.to_dict()
            weeks = data.get('weeks', [])
            print(f"Weeks: {len(weeks)}")
            print(f"Active: {data.get('is_active', False)}")
            
            if weeks:
                print(f"\nWeek 1:")
                print(f"  Focus: {weeks[0].get('focus_skill', 'NOT SET')}")
                print(f"  Resources: {len(weeks[0].get('resources', []))}")
                for r in weeks[0].get('resources', [])[:2]:
                    print(f"    - {r.get('name', 'Unnamed')}")
                
                if len(weeks) > 1:
                    print(f"\nWeek 2:")
                    print(f"  Focus: {weeks[1].get('focus_skill', 'NOT SET')}")
    else:
        print("❌ No roadmap found for test_user_herpath_demo\n")
        
except Exception as e:
    print(f"❌ Error: {e}\n")

# Check recent user activity
print("\n3️⃣ RECENT USERS:")
print("-" * 70)

try:
    users = db.collection('users').limit(5).stream()
    user_list = list(users)
    print(f"Found {len(user_list)} users\n")
    
    for user_doc in user_list[:3]:
        user_data = user_doc.to_dict()
        uid = user_data.get('uid', 'UNKNOWN')
        email = user_data.get('email', 'UNKNOWN')
        
        print(f"User: {email}")
        print(f"  UID: {uid}")
        
        # Get their active roadmap
        rm_docs = db.collection('roadmaps')\
            .where('uid', '==', uid)\
            .where('is_active', '==', True)\
            .limit(1)\
            .stream()
        
        rm_list = list(rm_docs)
        
        if rm_list:
            rm_data = rm_list[0].to_dict()
            weeks = rm_data.get('weeks', [])
            
            if weeks:
                skill = weeks[0].get('focus_skill', 'NOT SET')
                resources = len(weeks[0].get('resources', []))
                print(f"  Active Roadmap Week 1:")
                print(f"    Skill: {skill}")
                print(f"    Resources: {resources}")
                
                if 'Core Skill' in str(skill):
                    print(f"    🚨 PROBLEM: Showing placeholder!")
                else:
                    print(f"    ✅ Real content")
        else:
            print(f"  ❌ No active roadmap")
        
        print()
        
except Exception as e:
    print(f"❌ Error: {e}\n")

print("="*70)
print("Debug complete.")
print("="*70 + "\n")
