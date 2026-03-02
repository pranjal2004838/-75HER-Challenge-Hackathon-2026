#!/usr/bin/env python3
"""Check actual Firestore document structure."""

import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
import tomllib

secrets_path = ".streamlit/secrets.toml"
with open(secrets_path, 'rb') as f:
    secrets = tomllib.load(f)

firebase_creds = secrets.get('firebase_credentials', {})
credentials = service_account.Credentials.from_service_account_info(firebase_creds)
db = firestore.Client(credentials=credentials, project=firebase_creds.get('project_id'))

print("\n📋 CHECKING FIRESTORE DOCUMENT STRUCTURE\n")

# Get first roadmap
roadmaps = db.collection('roadmaps').limit(1).stream()
for doc in roadmaps:
    print(f"Document ID: {doc.id}")
    data = doc.to_dict()
    
    print(f"\nAll Fields in Document:")
    print("-" * 70)
    for key, value in data.items():
        value_type = type(value).__name__
        
        if isinstance(value, (dict, list)):
            if isinstance(value, dict) and len(value) <= 3:
                print(f"  {key}: {value_type} = {value}")
            elif isinstance(value, list):
                print(f"  {key}: {value_type} - length: {len(value)}")
                if value and isinstance(value[0], dict):
                    print(f"    First item keys: {list(value[0].keys())}")
            else:
                print(f"  {key}: {value_type} (length: {len(str(value))})")
        else:
            print(f"  {key}: {value_type} = {value}")
    
    print(f"\n{'Full JSON Structure:':^70}")
    print("-" * 70)
    print(json.dumps(data, indent=2, default=str)[:1000])  # First 1000 chars

print("\n")
