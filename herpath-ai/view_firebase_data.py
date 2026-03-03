#!/usr/bin/env python3
"""
Script to view Firebase Firestore data for debugging.
Shows all collections and documents in your HERPath AI Firebase database.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment forcefully
os.environ['FIREBASE_CONFIGURED'] = 'true'

def main():
    """View all Firebase data."""
    print("=" * 70)
    print("FIREBASE DATA VIEWER - HERPath AI")
    print("=" * 70)
    print()
    
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        # Initialize Firebase directly
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        # Check if already initialized
        try:
            app = firebase_admin.get_app()
            print("✅ Using existing Firebase app")
        except ValueError:
            # Load credentials from secrets
            import streamlit as st
            if "firebase_credentials" in st.secrets:
                cred_dict = dict(st.secrets["firebase_credentials"])
                cred = credentials.Certificate(cred_dict)
                app = firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized from secrets")
            else:
                print("❌ Firebase credentials not found in secrets.toml")
                return
        
        db = firestore.client()
        
        # List all collections
        collections = ['users', 'roadmaps', 'tasks', 'progress', 'chat_history']
        
        for collection_name in collections:
            print(f"\n📁 Collection: {collection_name}")
            print("-" * 70)
            
            docs = db.collection(collection_name).stream()
            doc_count = 0
            
            for doc in docs:
                doc_count += 1
                data = doc.to_dict()
                print(f"\n  Document ID: {doc.id}")
                print(f"  Data: {data}")
            
            if doc_count == 0:
                print("  (No documents found)")
            else:
                print(f"\n  Total documents: {doc_count}")
        
        print("\n" + "=" * 70)
        print("✅ Firebase data scan complete")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure firebase-admin is installed: pip install firebase-admin")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
