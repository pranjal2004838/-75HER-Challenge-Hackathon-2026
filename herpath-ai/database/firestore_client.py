"""
Firestore client for all database operations.
Handles CRUD for users, roadmaps, tasks, progress, and chat history.
Option B: Versioned roadmaps - each rebalance creates new document.
"""

import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any
from .schema import (
    UserSchema, RoadmapSchema, TaskSchema, 
    ProgressSchema, ChatSchema, TaskStatus
)
import json
import uuid

# Import FieldFilter for proper Firestore query syntax (avoids deprecation warning)
try:
    from google.cloud.firestore_v1.base_query import FieldFilter
except ImportError:
    FieldFilter = None  # Fallback for demo mode


# Lightweight in-memory Firestore stub for demo mode (uses Streamlit session_state)
class _DemoFirestoreModule:
    class Query:
        DESCENDING = 'DESC'


class _DemoFirestore:
    def __init__(self, client_owner):
        self._owner = client_owner

    def collection(self, name):
        return _DemoCollection(name)

    def batch(self):
        return _DemoBatch()


class _DemoCollection:
    def __init__(self, name):
        self.name = name
        if f'demo_{self.name}' not in st.session_state:
            st.session_state[f'demo_{self.name}'] = {}

    def document(self, doc_id: Optional[str] = None):
        if not doc_id:
            doc_id = str(uuid.uuid4())
        return _DemoDocRef(self.name, doc_id)

    def add(self, data: dict):
        doc_id = str(uuid.uuid4())
        st.session_state[f'demo_{self.name}'][doc_id] = dict(data)
        return (None, _DemoDocRef(self.name, doc_id))

    def where(self, field, op, value):
        return _DemoQuery(self.name).where(field, op, value)

    def order_by(self, *args, **kwargs):
        return _DemoQuery(self.name).order_by(*args, **kwargs)

    def stream(self):
        # return all docs
        docs = []
        for doc_id, data in st.session_state.get(f'demo_{self.name}', {}).items():
            docs.append(_DemoDocSnapshot(self.name, doc_id, data))
        return docs


class _DemoDocRef:
    def __init__(self, collection, doc_id):
        self.id = doc_id
        self._collection = collection

    def set(self, data: dict):
        st.session_state.setdefault(f'demo_{self._collection}', {})[self.id] = dict(data)

    def update(self, updates: dict):
        col = st.session_state.setdefault(f'demo_{self._collection}', {})
        if self.id in col:
            col[self.id].update(updates)
        else:
            col[self.id] = dict(updates)

    def get(self):
        col = st.session_state.get(f'demo_{self._collection}', {})
        data = col.get(self.id)
        return _DemoDocSnapshot(self._collection, self.id, data)


class _DemoDocSnapshot:
    def __init__(self, collection, doc_id, data):
        self.id = doc_id
        self._data = data
        self._collection = collection
        self.reference = _DemoDocRef(self._collection, doc_id)

    @property
    def exists(self):
        return self._data is not None

    def to_dict(self):
        return dict(self._data) if self._data is not None else None


class _DemoQuery:
    def __init__(self, collection):
        self._collection = collection
        self._filters = []
        self._order = None
        self._limit = None

    def where(self, field, op, value):
        self._filters.append((field, op, value))
        return self

    def order_by(self, field, direction=None):
        self._order = (field, direction)
        return self

    def limit(self, n: int):
        self._limit = n
        return self

    def stream(self):
        all_docs = st.session_state.get(f'demo_{self._collection}', {})
        results = []
        for doc_id, data in all_docs.items():
            ok = True
            for field, op, value in self._filters:
                if data.get(field) != value:
                    ok = False
                    break
            if ok:
                results.append(_DemoDocSnapshot(self._collection, doc_id, data))

        if self._order:
            key, direction = self._order
            results.sort(key=lambda d: d.to_dict().get(key))
            if direction == _DemoFirestoreModule.Query.DESCENDING:
                results.reverse()

        if self._limit is not None:
            results = results[: self._limit]

        return results


class _DemoBatch:
    def __init__(self):
        self._ops = []

    def set(self, doc_ref: _DemoDocRef, data: dict):
        self._ops.append(('set', doc_ref, data))

    def commit(self):
        for op, doc_ref, data in self._ops:
            if op == 'set':
                st.session_state.setdefault(f'demo_{doc_ref._collection}', {})[doc_ref.id] = dict(data)
        self._ops = []



class FirestoreClient:
    """Firestore database client for HERPath AI."""
    
    def __init__(self):
        """Initialize Firestore client."""
        self._db = None
        self._demo_mode = False
    
    @property
    def db(self):
        """Lazy load Firestore client."""
        if self._db is None:
            try:
                from firebase_admin import firestore
                self._db = firestore.client()
                # expose real firestore module to module scope for code that references it
                globals()['firestore'] = firestore
            except Exception as e:
                st.warning(f"⚠️ Firestore not available: {e}. Using demo mode.")
                self._demo_mode = True
                # install demo stub both as module-level 'firestore' and as client
                globals()['firestore'] = _DemoFirestoreModule()
                self._db = _DemoFirestore(self)
                return self._db
        return self._db
    
    def _is_demo_mode(self):
        """Check if running in demo mode (no Firebase)."""
        return self._demo_mode or self.db is None
    
    # =========================================================================
    # USER OPERATIONS
    # =========================================================================
    
    def create_user(self, user_data: dict) -> bool:
        """Create a new user document."""
        if self._is_demo_mode():
            # Store in session state for demo
            if 'demo_users' not in st.session_state:
                st.session_state.demo_users = {}
            st.session_state.demo_users[user_data.get('uid')] = user_data
            return True
        try:
            user = UserSchema(**user_data)
            self.db.collection('users').document(user.uid).set(user.model_dump())
            return True
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, uid: str) -> Optional[dict]:
        """Get user document by UID."""
        if self._is_demo_mode():
            return st.session_state.get('demo_users', {}).get(uid)
        try:
            doc = self.db.collection('users').document(uid).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            st.error(f"Error fetching user: {e}")
            return None
    
    def update_user(self, uid: str, updates: dict) -> bool:
        """Update user document."""
        if self._is_demo_mode():
            if 'demo_users' in st.session_state and uid in st.session_state.demo_users:
                st.session_state.demo_users[uid].update(updates)
            return True
        try:
            updates['updated_at'] = datetime.utcnow()
            self.db.collection('users').document(uid).update(updates)
            return True
        except Exception as e:
            st.error(f"Error updating user: {e}")
            return False
    
    def mark_onboarding_complete(self, uid: str) -> bool:
        """Mark user onboarding as complete."""
        return self.update_user(uid, {'onboarding_completed': True})
    
    # =========================================================================
    # ROADMAP OPERATIONS (Versioned - Option B)
    # =========================================================================
    
    def create_roadmap(self, roadmap_data: dict) -> Optional[str]:
        """
        Create a new roadmap version.
        Deactivates previous active roadmap for user.
        """
        if self._is_demo_mode():
            # Store in session state for demo
            if 'demo_roadmaps' not in st.session_state:
                st.session_state.demo_roadmaps = {}
            uid = roadmap_data.get('uid')
            roadmap_data['is_active'] = True
            roadmap_data['doc_id'] = f"demo_roadmap_{uid}"
            st.session_state.demo_roadmaps[uid] = roadmap_data
            return roadmap_data['doc_id']
        try:
            uid = roadmap_data.get('uid')
            
            # SAFEGUARD: Ensure total_weeks is always present (required field)
            if 'total_weeks' not in roadmap_data or roadmap_data.get('total_weeks') is None:
                # Calculate from phases if not provided
                phases = roadmap_data.get('phases', [])
                max_week = 0
                for phase in phases:
                    for week in phase.get('weeks', []):
                        max_week = max(max_week, week.get('week_number', 0))
                roadmap_data['total_weeks'] = max(max_week, 12)  # Min 12 weeks if empty
            
            # Deactivate previous active roadmaps
            self._deactivate_user_roadmaps(uid)
            
            # Create new roadmap
            roadmap = RoadmapSchema(**roadmap_data)
            doc_ref = self.db.collection('roadmaps').add(roadmap.model_dump())
            
            # Also create individual task documents
            self._create_tasks_from_roadmap(uid, roadmap)
            
            return doc_ref[1].id
        except Exception as e:
            st.error(f"Error creating roadmap: {e}")
            return None
    
    def _deactivate_user_roadmaps(self, uid: str):
        """Deactivate all active roadmaps for a user."""
        if self._is_demo_mode():
            return
        try:
            query = self.db.collection('roadmaps')
            if FieldFilter:
                query = query.where(filter=FieldFilter('uid', '==', uid))
                query = query.where(filter=FieldFilter('is_active', '==', True))
            else:
                query = query.where('uid', '==', uid).where('is_active', '==', True)
            docs = query.stream()
            
            for doc in docs:
                doc.reference.update({'is_active': False})
        except Exception as e:
            st.error(f"Error deactivating roadmaps: {e}")
    
    def get_active_roadmap(self, uid: str) -> Optional[dict]:
        """Get the currently active roadmap for a user."""
        if self._is_demo_mode():
            return st.session_state.get('demo_roadmaps', {}).get(uid)
        try:
            query = self.db.collection('roadmaps')
            if FieldFilter:
                query = query.where(filter=FieldFilter('uid', '==', uid))
                query = query.where(filter=FieldFilter('is_active', '==', True))
            else:
                query = query.where('uid', '==', uid).where('is_active', '==', True)
            docs = query.limit(1).stream()
            
            for doc in docs:
                data = doc.to_dict()
                data['doc_id'] = doc.id
                return data
            return None
        except Exception as e:
            st.error(f"Error fetching roadmap: {e}")
            return None
    
    def get_roadmap_history(self, uid: str) -> List[dict]:
        """Get all roadmap versions for a user (for history/undo)."""
        try:
            query = self.db.collection('roadmaps')
            if FieldFilter:
                query = query.where(filter=FieldFilter('uid', '==', uid))
            else:
                query = query.where('uid', '==', uid)
            docs = query.order_by('roadmap_version', direction=firestore.Query.DESCENDING).stream()
            
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            st.error(f"Error fetching roadmap history: {e}")
            return []
    
    def update_current_week(self, uid: str, week: int) -> bool:
        """Update current week in active roadmap."""
        try:
            roadmap = self.get_active_roadmap(uid)
            if roadmap and 'doc_id' in roadmap:
                self.db.collection('roadmaps').document(roadmap['doc_id']).update({
                    'current_week': week
                })
                return True
            return False
        except Exception as e:
            st.error(f"Error updating current week: {e}")
            return False
    
    # =========================================================================
    # TASK OPERATIONS
    # =========================================================================
    
    def _create_tasks_from_roadmap(self, uid: str, roadmap: RoadmapSchema):
        """Create individual task documents from roadmap phases."""
        try:
            batch = self.db.batch()
            task_count = 0
            
            for phase in roadmap.phases:
                for week in phase.weeks:
                    for idx, task_title in enumerate(week.tasks):
                        task_data = TaskSchema(
                            uid=uid,
                            roadmap_version=roadmap.roadmap_version,
                            week_number=week.week_number,
                            task_id=f"w{week.week_number}_t{idx+1}",
                            title=task_title,
                            task_type="learning"  # Default, can be enhanced
                        )
                        doc_ref = self.db.collection('tasks').document()
                        batch.set(doc_ref, task_data.model_dump())
                        task_count += 1
                        
                        # Firestore batch limit is 500
                        if task_count % 400 == 0:
                            batch.commit()
                            batch = self.db.batch()
            
            batch.commit()
        except Exception as e:
            st.error(f"Error creating tasks: {e}")
    
    def get_tasks_for_week(self, uid: str, week_number: int) -> List[dict]:
        """Get all tasks for a specific week."""
        try:
            # Get active roadmap version
            roadmap = self.get_active_roadmap(uid)
            if not roadmap:
                return []
            
            query = self.db.collection('tasks')
            if FieldFilter:
                query = query.where(filter=FieldFilter('uid', '==', uid))
                query = query.where(filter=FieldFilter('week_number', '==', week_number))
            else:
                query = query.where('uid', '==', uid).where('week_number', '==', week_number)
            docs = query.stream()
            
            return [doc.to_dict() | {'doc_id': doc.id} for doc in docs]
        except Exception as e:
            st.error(f"Error fetching tasks: {e}")
            return []
    
    def update_task_status(self, task_doc_id: str, status: str) -> bool:
        """Update task status."""
        try:
            updates = {'status': status}
            if status == TaskStatus.COMPLETED:
                updates['completed_at'] = datetime.utcnow()
            
            self.db.collection('tasks').document(task_doc_id).update(updates)
            return True
        except Exception as e:
            st.error(f"Error updating task: {e}")
            return False
    
    def get_all_user_tasks(self, uid: str) -> List[dict]:
        """Get all tasks for a user from active roadmap."""
        try:
            roadmap = self.get_active_roadmap(uid)
            if not roadmap:
                return []
            
            query = self.db.collection('tasks')
            if FieldFilter:
                query = query.where(filter=FieldFilter('uid', '==', uid))
            else:
                query = query.where('uid', '==', uid)
            docs = query.stream()
            
            return [doc.to_dict() | {'doc_id': doc.id} for doc in docs]
        except Exception as e:
            st.error(f"Error fetching all tasks: {e}")
            return []
    
    # =========================================================================
    # PROGRESS OPERATIONS
    # =========================================================================
    
    def update_progress(self, uid: str) -> Optional[dict]:
        """Calculate and update progress summary."""
        if self._is_demo_mode():
            # Return demo progress data
            progress_data = {
                'uid': uid,
                'completion_percentage': 25.0,
                'missed_tasks_count': 0,
                'completed_tasks_count': 3,
                'total_tasks_count': 12,
                'pace_status': 'on_track',
                'current_week': 1,
                'last_updated': datetime.utcnow()
            }
            if 'demo_progress' not in st.session_state:
                st.session_state.demo_progress = {}
            st.session_state.demo_progress[uid] = progress_data
            return progress_data
        try:
            tasks = self.get_all_user_tasks(uid)
            roadmap = self.get_active_roadmap(uid)
            
            if not tasks or not roadmap:
                return None
            
            total = len(tasks)
            completed = sum(1 for t in tasks if t.get('status') == 'completed')
            missed = sum(1 for t in tasks if t.get('status') == 'skipped')
            
            completion_pct = (completed / total * 100) if total > 0 else 0
            
            # Calculate pace status
            current_week = roadmap.get('current_week', 1)
            total_weeks = roadmap.get('total_weeks', 1)
            expected_pct = (current_week / total_weeks * 100) if total_weeks > 0 else 0
            
            if completion_pct >= expected_pct:
                pace = 'ahead' if completion_pct > expected_pct + 10 else 'on_track'
            else:
                pace = 'behind'
            
            progress_data = {
                'uid': uid,
                'completion_percentage': round(completion_pct, 1),
                'missed_tasks_count': missed,
                'completed_tasks_count': completed,
                'total_tasks_count': total,
                'pace_status': pace,
                'current_week': current_week,
                'last_updated': datetime.utcnow()
            }
            
            self.db.collection('progress_summary').document(uid).set(progress_data)
            return progress_data
            
        except Exception as e:
            st.error(f"Error updating progress: {e}")
            return None
    
    def get_progress(self, uid: str) -> Optional[dict]:
        """Get progress summary for user."""
        if self._is_demo_mode():
            return st.session_state.get('demo_progress', {}).get(uid, self.update_progress(uid))
        try:
            doc = self.db.collection('progress_summary').document(uid).get()
            if doc.exists:
                return doc.to_dict()
            return self.update_progress(uid)
        except Exception as e:
            st.error(f"Error fetching progress: {e}")
            return None
    
    # =========================================================================
    # CHAT HISTORY OPERATIONS
    # =========================================================================
    
    def save_chat_message(self, chat_data: dict) -> bool:
        """Save a chat message to history."""
        try:
            chat = ChatSchema(**chat_data)
            self.db.collection('chat_history').add(chat.model_dump())
            return True
        except Exception as e:
            st.error(f"Error saving chat: {e}")
            return False
    
    def get_chat_history(self, uid: str, limit: int = 50) -> List[dict]:
        """Get chat history for user."""
        try:
            # Simple query without composite index requirement
            query = self.db.collection('chat_history')
            if FieldFilter:
                query = query.where(filter=FieldFilter('uid', '==', uid))
            else:
                query = query.where('uid', '==', uid)
            
            # Fetch all docs and sort locally to avoid index requirement
            docs = query.stream()
            chats = [doc.to_dict() for doc in docs]
            
            # Sort by timestamp locally
            chats.sort(key=lambda x: x.get('timestamp', 0))
            return chats[-limit:] if len(chats) > limit else chats
        except Exception as e:
            st.error(f"Error fetching chat history: {e}")
            return []
    
    # =========================================================================
    # ANALYTICS HELPERS
    # =========================================================================
    
    def get_missed_task_percentage_last_n_weeks(self, uid: str, n_weeks: int = 2) -> float:
        """Calculate missed task percentage for last N weeks."""
        try:
            roadmap = self.get_active_roadmap(uid)
            if not roadmap:
                return 0.0
            
            current_week = roadmap.get('current_week', 1)
            start_week = max(1, current_week - n_weeks + 1)
            
            tasks = self.get_all_user_tasks(uid)
            recent_tasks = [t for t in tasks if start_week <= t.get('week_number', 0) <= current_week]
            
            if not recent_tasks:
                return 0.0
            
            missed = sum(1 for t in recent_tasks if t.get('status') == 'skipped')
            return (missed / len(recent_tasks) * 100)
        except:
            return 0.0
