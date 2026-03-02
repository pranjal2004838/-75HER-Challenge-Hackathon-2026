#!/usr/bin/env python3
"""Test Firebase credential loading"""

import os
import json
from dotenv import load_dotenv

# Load .env
load_dotenv()

print("=" * 80)
print("Testing Firebase Credential Loading")
print("=" * 80)

# Test 1: Check if .env is loaded
cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON", "")
db_url = os.getenv("FIREBASE_DATABASE_URL", "")

print(f"\n✓ FIREBASE_CREDENTIALS_JSON length: {len(cred_json)} chars")
print(f"✓ FIREBASE_DATABASE_URL: {db_url[:50]}...")

# Test 2: Try to parse JSON
try:
    cred_dict = json.loads(cred_json)
    print(f"\n✓ JSON Parsed Successfully")
    print(f"  - Project ID: {cred_dict.get('project_id')}")
    print(f"  - Client Email: {cred_dict.get('client_email')}")
    print(f"  - Private Key starts with: {str(cred_dict.get('private_key', ''))[:50]}...")
except json.JSONDecodeError as e:
    print(f"\n❌ JSON Parse Error: {e}")
    exit(1)

# Test 3: Try Firebase initialization
try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    
    # Check if app is already initialized
    try:
        app = firebase_admin.get_app()
        print(f"\n✓ Firebase app already initialized")
    except:
        print(f"\n• Initializing Firebase app...")
        cred = credentials.Certificate(cred_dict)
        app = firebase_admin.initialize_app(cred, {
            'databaseURL': db_url
        })
        print(f"✓ Firebase app initialized successfully")
    
    # Test Firestore connection
    db = firestore.client()
    users_ref = db.collection('users')
    docs = list(users_ref.limit(1).stream())
    print(f"✓ Firestore connected - {len(docs)} sample docs read")
    
except Exception as e:
    print(f"\n❌ Firebase initialization error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 80)
print("✓ All tests passed - Firebase is properly configured!")
print("=" * 80)
