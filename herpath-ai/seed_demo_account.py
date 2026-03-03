#!/usr/bin/env python3
"""
Demo Account Seeder - HERPath AI
=================================

Creates a pre-populated demo account for judges and evaluators.
The demo account includes:
- User profile with realistic data
- In-progress roadmap with mixed completion
- Progress tracking
- Sample chat history

Usage:
    python seed_demo_account.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from config.constants import DemoAccountConfig


def seed_demo_account():
    """Seed demo account with realistic data."""
    print("=" * 70)
    print("DEMO ACCOUNT SEEDER - HERPath AI")
    print("=" * 70)
    print()
    
    try:
        # Initialize Firebase
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        # Check if already initialized
        try:
            app = firebase_admin.get_app()
            print("✅ Using existing Firebase app")
        except ValueError:
            # Load credentials
            import streamlit as st
            if "firebase_credentials" in st.secrets:
                cred_dict = dict(st.secrets["firebase_credentials"])
                cred = credentials.Certificate(cred_dict)
                app = firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized")
            else:
                print("❌ Firebase credentials not found")
                return
        
        db = firestore.client()
        
        # Generate demo user ID
        demo_uid = hashlib.sha256(DemoAccountConfig.EMAIL.encode()).hexdigest()[:28]
        
        print(f"\n📝 Creating demo account...")
        print(f"   Email: {DemoAccountConfig.EMAIL}")
        print(f"   Password: {DemoAccountConfig.PASSWORD}")
        print(f"   Name: {DemoAccountConfig.NAME}")
        print(f"   UID: {demo_uid}\n")
        
        # 1. Create user profile
        user_data = {
            'uid': demo_uid,
            'name': DemoAccountConfig.NAME,
            'email': DemoAccountConfig.EMAIL,
            'goal': DemoAccountConfig.GOAL,
            'current_level': DemoAccountConfig.CURRENT_LEVEL,
            'weekly_hours': DemoAccountConfig.WEEKLY_HOURS,
            'deadline_type': f"{DemoAccountConfig.DEADLINE_WEEKS // 4} months",
            'financial_constraint': DemoAccountConfig.FINANCIAL_CONSTRAINT,
            'situation': DemoAccountConfig.SITUATION,
            'background_text': DemoAccountConfig.BACKGROUND,
            'onboarding_completed': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        db.collection('users').document(demo_uid).set(user_data)
        print("✅ User profile created")
        
        # 2. Create roadmap
        roadmap_data = {
            'uid': demo_uid,
            'goal': DemoAccountConfig.GOAL,
            'total_weeks': DemoAccountConfig.DEADLINE_WEEKS,
            'current_week': DemoAccountConfig.CURRENT_WEEK,
            'is_active': True,
            'version': 1,
            'created_at': datetime.utcnow() - timedelta(weeks=DemoAccountConfig.CURRENT_WEEK),
            'updated_at': datetime.utcnow(),
            'phases': [
                {
                    'phase_name': 'Phase 1: Python & Programming Foundations',
                    'phase_description': 'Build core programming skills with Python',
                    'weeks': [
                        {
                            'week_number': 1,
                            'focus_skill': 'Python Basics & Syntax',
                            'tasks': [
                                'Complete Python syntax tutorial on Codecademy (3 hrs)',
                                'Practice variables, data types, operators (2 hrs)',
                                'Write first program: temperature converter (1 hr)',
                                'Read: "Python for Everybody" Ch 1-2 (2 hrs)'
                            ],
                            'milestone': 'Write a program that converts temperatures between C/F/K',
                            'success_metric': 'Program runs without errors and handles edge cases'
                        },
                        {
                            'week_number': 2,
                            'focus_skill': 'Control Flow & Functions',
                            'tasks': [
                                'Learn if/else statements and loops (2 hrs)',
                                'Master functions and parameters (2 hrs)',
                                'Build calculator with basic operations (2 hrs)',
                                'Submit 5 Codewars problems (kyu 8-7) (2 hrs)'
                            ],
                            'milestone': 'Build a functional calculator application',
                            'success_metric': 'Calculator handles +, -, *, / with error handling'
                        },
                        {
                            'week_number': 3,
                            'focus_skill': 'Data Structures (Lists & Dicts)',
                            'tasks': [
                                'Master lists, tuples, dictionaries (3 hrs)',
                                'Practice list comprehensions (2 hrs)',
                                'Build a todo list CLI app (3 hrs)',
                                'Read: Python docs on data structures (1 hr)'
                            ],
                            'milestone': 'Create a working command-line todo app',
                            'success_metric': 'App can add, remove, list, and mark complete'
                        },
                        {
                            'week_number': 4,
                            'focus_skill': 'File I/O & Error Handling',
                            'tasks': [
                                'Learn file reading and writing (2 hrs)',
                                'Master try/except error handling (2 hrs)',
                                'Build contact manager with file saving (3 hrs)',
                                'Submit 5 more Codewars problems (kyu 7-6) (2 hrs)'
                            ],
                            'milestone': 'Contact manager that persists data to files',
                            'success_metric': 'App saves/loads contacts without data loss'
                        }
                    ]
                },
                {
                    'phase_name': 'Phase 2: Data Analysis & NumPy/Pandas',
                    'phase_description': 'Master data manipulation and analysis tools',
                    'weeks': [
                        {
                            'week_number': 5,
                            'focus_skill': 'NumPy Basics',
                            'tasks': [
                                'numpy tutorial on Real Python (3 hrs)',
                                'Practice array operations and indexing (2 hrs)',
                                'Complete 10 NumPy exercises (3 hrs)',
                                'Build matrix calculator project (2 hrs)'
                            ],
                            'milestone': 'Matrix operations calculator',
                            'success_metric': 'Can multiply, transpose, inverse matrices'
                        }
                    ]
                }
            ]
        }
        
        roadmap_ref = db.collection('roadmaps').document()
        roadmap_ref.set(roadmap_data)
        print("✅ Roadmap created")
        
        # 3. Create progress tracking
        progress_data = {
            'uid': demo_uid,
            'roadmap_id': roadmap_ref.id,
            'completion_percentage': DemoAccountConfig.COMPLETION_PERCENTAGE,
            'completed_tasks_count': DemoAccountConfig.COMPLETED_TASKS,
            'total_tasks_count': DemoAccountConfig.TOTAL_TASKS,
            'missed_tasks_count': DemoAccountConfig.MISSED_TASKS,
            'pace_status': 'on_track',
            'current_week': DemoAccountConfig.CURRENT_WEEK,
            'streak_days': 12,
            'last_activity': datetime.utcnow() - timedelta(hours=5),
            'updated_at': datetime.utcnow()
        }
        
        db.collection('progress').document(demo_uid).set(progress_data)
        print("✅ Progress tracking created")
        
        # 4. Create sample chat history
        messages = [
            {
                'uid': demo_uid,
                'role': 'user',
                'content': "I'm feeling stuck on list comprehensions. Can you help?",
                'timestamp': datetime.utcnow() - timedelta(days=2),
                'page': 'coach'
            },
            {
                'uid': demo_uid,
                'role': 'assistant',
                'content': "Absolutely, Sarah! List comprehensions are Python's elegant way to transform lists...",
                'timestamp': datetime.utcnow() - timedelta(days=2, seconds=15),
                'page': 'coach'
            },
            {
                'uid': demo_uid,
                'role': 'user',
                'content': "How do I know if I'm ready to move from Python basics to ML?",
                'timestamp': datetime.utcnow() - timedelta(days=1),
                'page': 'coach'
            },
            {
                'uid': demo_uid,
                'role': 'assistant',
                'content': "Great question! You're ready when you can: 1) Write functions without googling syntax...",
                'timestamp': datetime.utcnow() - timedelta(days=1, seconds=20),
                'page': 'coach'
            }
        ]
        
        for msg in messages:
            db.collection('chat_history').add(msg)
        
        print("✅ Chat history created")
        
        print(f"\n{'=' * 70}")
        print("✅ DEMO ACCOUNT SEEDED SUCCESSFULLY")
        print(f"{'=' * 70}\n")
        print("Demo account details:")
        print(f"  📧 Email: {DemoAccountConfig.EMAIL}")
        print(f"  🔑 Password: {DemoAccountConfig.PASSWORD}")
        print(f"  👤 Name: {DemoAccountConfig.NAME}")
        print(f"  🎯 Goal: {DemoAccountConfig.GOAL}")
        print(f"  📊 Progress: {DemoAccountConfig.COMPLETION_PERCENTAGE}%")
        print(f"  📅 Current Week: {DemoAccountConfig.CURRENT_WEEK}/{DemoAccountConfig.DEADLINE_WEEKS}")
        print()
        print("Judges can now sign in with these credentials to see a realistic demo!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure firebase-admin is installed")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    seed_demo_account()
