"""
Firestore data schemas using Pydantic for validation.
Option B: Versioned roadmap history - each rebalance creates new document.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class TaskType(str, Enum):
    LEARNING = "learning"
    PROJECT = "project"
    MILESTONE = "milestone"


class PaceStatus(str, Enum):
    ON_TRACK = "on_track"
    BEHIND = "behind"
    AHEAD = "ahead"


# =============================================================================
# USER SCHEMA
# =============================================================================

class UserSchema(BaseModel):
    """Schema for users collection."""
    uid: str
    name: str
    email: str
    goal: str
    current_level: str
    weekly_hours: int
    deadline_type: str  # "Flexible", "3 months", etc.
    financial_constraint: str
    situation: str
    background_text: str = ""
    onboarding_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


# =============================================================================
# ROADMAP SCHEMA (Versioned - Option B)
# =============================================================================

class WeekSchema(BaseModel):
    """Schema for individual week within a phase."""
    week_number: int
    focus_skill: str
    tasks: List[str]
    milestone: str
    success_metric: str


class PhaseSchema(BaseModel):
    """Schema for roadmap phases."""
    phase_name: str
    weeks: List[WeekSchema]


class RoadmapSchema(BaseModel):
    """
    Schema for roadmaps collection.
    Option B: Each rebalance creates a new document with version timestamp.
    Document ID: auto-generated
    """
    uid: str
    roadmap_version: datetime = Field(default_factory=datetime.utcnow)
    total_weeks: int
    current_week: int = 1
    phases: List[PhaseSchema]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    last_rebalanced_at: Optional[datetime] = None
    is_active: bool = True  # Only one active roadmap per user
    rebalance_reason: Optional[str] = None  # Why was this version created
    
    class Config:
        use_enum_values = True


# =============================================================================
# TASK SCHEMA
# =============================================================================

class TaskSchema(BaseModel):
    """Schema for tasks collection."""
    uid: str
    roadmap_version: datetime  # Links to specific roadmap version
    week_number: int
    task_id: str
    title: str
    task_type: TaskType
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True


# =============================================================================
# PROGRESS SUMMARY SCHEMA
# =============================================================================

class ProgressSchema(BaseModel):
    """Schema for progress_summary collection."""
    uid: str
    completion_percentage: float = 0.0
    missed_tasks_count: int = 0
    completed_tasks_count: int = 0
    total_tasks_count: int = 0
    projected_completion_date: Optional[datetime] = None
    pace_status: PaceStatus = PaceStatus.ON_TRACK
    current_week: int = 1
    weeks_behind: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


# =============================================================================
# CHAT HISTORY SCHEMA
# =============================================================================

class ChatSchema(BaseModel):
    """Schema for chat_history collection."""
    uid: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_message: str
    ai_response: str
    mode: str = "general"  # "clarify_plan", "feeling_stuck", "interview_guidance"
    context_snapshot: Optional[dict] = None  # Snapshot of user state at time of chat
    
    class Config:
        use_enum_values = True


# =============================================================================
# SKILL GAP OUTPUT SCHEMA
# =============================================================================

class SkillGapOutput(BaseModel):
    """Schema for SkillGapAgent output."""
    required_skills: List[str]
    missing_skills: List[str]
    priority_order: List[str]
    confidence_assessment: str
    emotional_signals: Optional[dict] = None  # Extracted from background_text


# =============================================================================
# ROADMAP GENERATION OUTPUT SCHEMA
# =============================================================================

class RoadmapGenerationOutput(BaseModel):
    """Schema for RoadmapAgent output."""
    total_weeks: int
    phases: List[PhaseSchema]
    recommended_resources: Optional[List[dict]] = None
