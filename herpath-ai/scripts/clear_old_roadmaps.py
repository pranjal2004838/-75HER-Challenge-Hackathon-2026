#!/usr/bin/env python3
"""Clear old placeholder roadmaps from Firestore."""

import os
import tomllib
from google.cloud import firestore
from google.oauth2 import service_account

secrets_path = ".streamlit/secrets.toml"
with open(secrets_path, 'rb') as f:
    secrets = tomllib.load(f)

firebase_creds = secrets.get('firebase_credentials', {})
credentials = service_account.Credentials.from_service_account_info(firebase_creds)
db = firestore.Client(credentials=credentials, project=firebase_creds.get('project_id'))

print("\n" + "="*70)
print("🧹 CLEARING OLD PLACEHOLDER ROADMAPS")
print("="*70 + "\n")

# Get all roadmaps
roadmaps = db.collection('roadmaps').stream()
deleted_count = 0

for doc in roadmaps:
    data = doc.to_dict()
    uid = data.get('uid', '')
    phases = data.get('phases', [])
    
    # Check if this is an old placeholder roadmap
    is_placeholder = False
    if phases:
        for phase in phases:
            for week in phase.get('weeks', []):
                if 'Core Skill' in str(week.get('focus_skill', '')) or 'Applied Skill' in str(week.get('focus_skill', '')):
                    is_placeholder = True
                    break
    
    if is_placeholder:
        db.collection('roadmaps').document(doc.id).delete()
        deleted_count += 1
        print(f"🗑️  Deleted old placeholder roadmap for user {uid[:8]}...")

print(f"\n✅ Deleted {deleted_count} old placeholder roadmaps")
print("   Users will now get fresh roadmaps with real skills when they log in")
print("\n" + "="*70 + "\n")
