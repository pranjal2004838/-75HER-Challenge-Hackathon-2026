"""
Rule Engine for adaptive roadmap adjustments.
Monitors progress and triggers rebalancing when needed.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class RebalanceTrigger(Enum):
    """Types of rebalance triggers."""
    MISSED_TASKS = "missed_tasks"
    HOURS_CHANGED = "hours_changed"
    DEADLINE_CHANGED = "deadline_changed"
    AHEAD_OF_SCHEDULE = "ahead_of_schedule"
    USER_REQUESTED = "user_requested"
    SITUATION_CHANGED = "situation_changed"


@dataclass
class RebalanceRecommendation:
    """Recommendation from rule engine."""
    should_rebalance: bool
    trigger: Optional[RebalanceTrigger]
    severity: str  # "low", "medium", "high"
    message: str
    suggested_actions: List[str]


class RuleEngine:
    """
    Adaptive rule engine for roadmap management.
    
    Monitors user progress and user state changes,
    determines when rebalancing is needed.
    """
    
    # Thresholds (can be overridden)
    MISSED_TASK_THRESHOLD_PERCENT = 30
    MISSED_TASK_WINDOW_WEEKS = 2
    AHEAD_THRESHOLD_PERCENT = 20
    HOURS_CHANGE_THRESHOLD_PERCENT = 25
    
    def __init__(
        self,
        missed_threshold: float = None,
        ahead_threshold: float = None
    ):
        """
        Initialize rule engine.
        
        Args:
            missed_threshold: Custom missed task threshold (0-100)
            ahead_threshold: Custom ahead of schedule threshold (0-100)
        """
        if missed_threshold:
            self.MISSED_TASK_THRESHOLD_PERCENT = missed_threshold
        if ahead_threshold:
            self.AHEAD_THRESHOLD_PERCENT = ahead_threshold
    
    def evaluate(
        self,
        progress_data: Dict[str, Any],
        user_data: Dict[str, Any],
        roadmap_data: Dict[str, Any],
        previous_user_data: Optional[Dict[str, Any]] = None
    ) -> RebalanceRecommendation:
        """
        Evaluate if rebalancing is needed based on current state.
        
        Args:
            progress_data: Current progress summary
            user_data: Current user profile
            roadmap_data: Active roadmap
            previous_user_data: Previous user profile (for change detection)
            
        Returns:
            RebalanceRecommendation with decision and reasoning
        """
        recommendations = []
        
        # Check missed tasks
        missed_result = self._check_missed_tasks(progress_data, roadmap_data)
        if missed_result:
            recommendations.append(missed_result)
        
        # Check if ahead of schedule
        ahead_result = self._check_ahead_of_schedule(progress_data, roadmap_data)
        if ahead_result:
            recommendations.append(ahead_result)
        
        # Check for hours change
        if previous_user_data:
            hours_result = self._check_hours_change(user_data, previous_user_data)
            if hours_result:
                recommendations.append(hours_result)
            
            # Check for deadline change
            deadline_result = self._check_deadline_change(user_data, previous_user_data)
            if deadline_result:
                recommendations.append(deadline_result)
            
            # Check for situation change
            situation_result = self._check_situation_change(user_data, previous_user_data)
            if situation_result:
                recommendations.append(situation_result)
        
        # Return highest priority recommendation
        if recommendations:
            # Sort by severity
            severity_order = {"high": 0, "medium": 1, "low": 2}
            recommendations.sort(key=lambda r: severity_order.get(r.severity, 3))
            return recommendations[0]
        
        # No rebalancing needed
        return RebalanceRecommendation(
            should_rebalance=False,
            trigger=None,
            severity="none",
            message="You're on track! Keep up the great work.",
            suggested_actions=[]
        )
    
    def _check_missed_tasks(
        self,
        progress_data: Dict[str, Any],
        roadmap_data: Dict[str, Any]
    ) -> Optional[RebalanceRecommendation]:
        """Check if too many tasks have been missed."""
        
        total_tasks = progress_data.get('total_tasks_count', 0)
        missed_tasks = progress_data.get('missed_tasks_count', 0)
        current_week = roadmap_data.get('current_week', 1)
        
        if total_tasks == 0:
            return None
        
        missed_percent = (missed_tasks / total_tasks) * 100
        
        if missed_percent >= self.MISSED_TASK_THRESHOLD_PERCENT:
            severity = "high" if missed_percent >= 50 else "medium"
            
            return RebalanceRecommendation(
                should_rebalance=True,
                trigger=RebalanceTrigger.MISSED_TASKS,
                severity=severity,
                message=f"You've missed {missed_percent:.0f}% of tasks. Let's adjust your roadmap to be more achievable.",
                suggested_actions=[
                    "Extend your timeline to reduce weekly workload",
                    "Focus on the highest priority skills only",
                    "Break tasks into smaller, more manageable pieces",
                    "Consider if your weekly hours estimate is realistic"
                ]
            )
        
        return None
    
    def _check_ahead_of_schedule(
        self,
        progress_data: Dict[str, Any],
        roadmap_data: Dict[str, Any]
    ) -> Optional[RebalanceRecommendation]:
        """Check if user is significantly ahead of schedule."""
        
        completion_pct = progress_data.get('completion_percentage', 0)
        current_week = roadmap_data.get('current_week', 1)
        total_weeks = roadmap_data.get('total_weeks', 1)
        
        expected_pct = (current_week / total_weeks) * 100 if total_weeks > 0 else 0
        
        if completion_pct >= expected_pct + self.AHEAD_THRESHOLD_PERCENT:
            return RebalanceRecommendation(
                should_rebalance=True,
                trigger=RebalanceTrigger.AHEAD_OF_SCHEDULE,
                severity="low",
                message="Amazing progress! You're ahead of schedule. Would you like to add advanced topics?",
                suggested_actions=[
                    "Add an optional advanced mini-project",
                    "Dive deeper into a topic you're interested in",
                    "Start interview prep earlier",
                    "Keep current pace and finish early"
                ]
            )
        
        return None
    
    def _check_hours_change(
        self,
        current_user: Dict[str, Any],
        previous_user: Dict[str, Any]
    ) -> Optional[RebalanceRecommendation]:
        """Check if weekly hours changed significantly."""
        
        current_hours = current_user.get('weekly_hours', 0)
        previous_hours = previous_user.get('weekly_hours', 0)
        
        if previous_hours == 0:
            return None
        
        change_percent = abs(current_hours - previous_hours) / previous_hours * 100
        
        if change_percent >= self.HOURS_CHANGE_THRESHOLD_PERCENT:
            direction = "increased" if current_hours > previous_hours else "decreased"
            
            return RebalanceRecommendation(
                should_rebalance=True,
                trigger=RebalanceTrigger.HOURS_CHANGED,
                severity="medium",
                message=f"Your weekly hours {direction}. Let's adjust your roadmap accordingly.",
                suggested_actions=[
                    f"Recalculate timeline based on {current_hours} hours/week",
                    "Redistribute remaining tasks",
                    "Update milestones and deadlines"
                ]
            )
        
        return None
    
    def _check_deadline_change(
        self,
        current_user: Dict[str, Any],
        previous_user: Dict[str, Any]
    ) -> Optional[RebalanceRecommendation]:
        """Check if deadline setting changed."""
        
        current_deadline = current_user.get('deadline_type')
        previous_deadline = previous_user.get('deadline_type')
        
        if current_deadline != previous_deadline:
            return RebalanceRecommendation(
                should_rebalance=True,
                trigger=RebalanceTrigger.DEADLINE_CHANGED,
                severity="high",
                message="Your timeline has changed. Let's rebuild your roadmap.",
                suggested_actions=[
                    "Regenerate roadmap with new deadline",
                    "Adjust task distribution",
                    "Reprioritize remaining skills"
                ]
            )
        
        return None
    
    def _check_situation_change(
        self,
        current_user: Dict[str, Any],
        previous_user: Dict[str, Any]
    ) -> Optional[RebalanceRecommendation]:
        """Check if life situation changed."""
        
        current_situation = current_user.get('situation')
        previous_situation = previous_user.get('situation')
        
        if current_situation != previous_situation:
            return RebalanceRecommendation(
                should_rebalance=True,
                trigger=RebalanceTrigger.SITUATION_CHANGED,
                severity="medium",
                message="Your situation has changed. Let's adjust your plan to fit your new circumstances.",
                suggested_actions=[
                    "Review and adjust weekly hours",
                    "Consider new time constraints or opportunities",
                    "Update resource recommendations"
                ]
            )
        
        return None
    
    def get_pace_status(
        self,
        progress_data: Dict[str, Any],
        roadmap_data: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Get current pace status with description.
        
        Returns:
            Tuple of (status, description)
        """
        completion_pct = progress_data.get('completion_percentage', 0)
        current_week = roadmap_data.get('current_week', 1)
        total_weeks = roadmap_data.get('total_weeks', 1)
        
        expected_pct = (current_week / total_weeks) * 100 if total_weeks > 0 else 0
        diff = completion_pct - expected_pct
        
        if diff >= 10:
            return ("ahead", f"You're {diff:.0f}% ahead of schedule! 🚀")
        elif diff >= -10:
            return ("on_track", "You're right on track! Keep it up! ✅")
        elif diff >= -25:
            return ("slightly_behind", f"You're {abs(diff):.0f}% behind, but manageable. 📊")
        else:
            return ("behind", f"You're {abs(diff):.0f}% behind schedule. Consider a rebalance. ⚠️")


# Singleton instance
rule_engine = RuleEngine()
