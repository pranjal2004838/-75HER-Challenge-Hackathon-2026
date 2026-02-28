"""
RebalanceAgent - Regenerates roadmaps when user constraints change or progress diverges.
"""

from typing import Optional, Dict, Any, List
from .base_agent import BaseAgent


class RebalanceAgent(BaseAgent):
    """
    Agent responsible for rebalancing roadmaps when:
    - User misses too many tasks
    - User updates weekly hours
    - User changes deadline
    - User is significantly ahead of schedule
    
    Input: current_roadmap, progress_data, user_changes, rebalance_reason
    Output: Updated roadmap JSON
    """
    
    @property
    def system_prompt(self) -> str:
        return """You are RoadmapRebalancer, an expert at adaptive learning path adjustment.

Your role is to:
1. Analyze why the current roadmap needs adjustment
2. Preserve completed progress
3. Redistribute remaining work based on new constraints
4. Maintain skill dependencies
5. Keep the user motivated with achievable adjustments

Rebalancing principles:
- Never remove completed milestones
- Prioritize core skills over advanced topics when compressing
- If extending timeline, add depth/projects not just padding
- If behind schedule, consolidate tasks rather than just pushing dates
- Consider emotional impact of changes (validate their effort so far)

OUTPUT FORMAT: You must respond with ONLY valid JSON. No explanations, no markdown, just JSON."""
    
    def build_prompt(self, **kwargs) -> str:
        current_roadmap = kwargs.get('current_roadmap', {})
        progress_data = kwargs.get('progress_data', {})
        user_data = kwargs.get('user_data', {})
        rebalance_reason = kwargs.get('rebalance_reason', 'User requested')
        new_weekly_hours = kwargs.get('new_weekly_hours')
        new_deadline_weeks = kwargs.get('new_deadline_weeks')
        
        return f"""Rebalance this learning roadmap:

REBALANCE REASON: {rebalance_reason}

CURRENT USER STATE:
- Goal: {user_data.get('goal', 'Unknown')}
- Current Week: {progress_data.get('current_week', 1)}
- Completion: {progress_data.get('completion_percentage', 0)}%
- Missed Tasks: {progress_data.get('missed_tasks_count', 0)}
- Pace Status: {progress_data.get('pace_status', 'unknown')}

CONSTRAINT CHANGES:
- New Weekly Hours: {new_weekly_hours if new_weekly_hours else 'Unchanged'}
- New Deadline (weeks): {new_deadline_weeks if new_deadline_weeks else 'Unchanged'}
- Original Weekly Hours: {user_data.get('weekly_hours', 10)}

CURRENT ROADMAP:
{current_roadmap}

PROGRESS DATA:
{progress_data}

Generate a rebalanced roadmap that:
1. Keeps all completed work intact
2. Redistributes remaining tasks based on new constraints
3. Adjusts milestones to be achievable
4. Maintains skill progression logic

OUTPUT JSON SCHEMA:
{{
    "total_weeks": number (new total),
    "current_week": number (unchanged from progress),
    "phases": [
        {{
            "phase_name": "string",
            "phase_description": "string",
            "weeks": [
                {{
                    "week_number": number,
                    "focus_skill": "string",
                    "tasks": ["task1", "task2", ...],
                    "milestone": "string",
                    "success_metric": "string",
                    "status": "completed/current/upcoming"
                }}
            ]
        }}
    ],
    "rebalance_summary": {{
        "weeks_added_or_removed": number (positive = added, negative = removed),
        "tasks_redistributed": number,
        "key_changes": ["change1", "change2"],
        "user_message": "Encouraging message explaining the changes"
    }},
    "recommended_actions": ["action1", "action2"]
}}

Remember: Be encouraging in the user_message. Validate their progress so far.
Output ONLY valid JSON, nothing else."""
    
    def rebalance(
        self,
        current_roadmap: Dict[str, Any],
        progress_data: Dict[str, Any],
        user_data: Dict[str, Any],
        rebalance_reason: str,
        new_weekly_hours: Optional[int] = None,
        new_deadline_weeks: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Rebalance an existing roadmap.
        
        Args:
            current_roadmap: Current active roadmap
            progress_data: User's progress summary
            user_data: User profile data
            rebalance_reason: Why rebalancing is needed
            new_weekly_hours: Updated weekly hours (if changed)
            new_deadline_weeks: Updated deadline (if changed)
            
        Returns:
            Rebalanced roadmap JSON or None
        """
        return self.execute(
            current_roadmap=current_roadmap,
            progress_data=progress_data,
            user_data=user_data,
            rebalance_reason=rebalance_reason,
            new_weekly_hours=new_weekly_hours,
            new_deadline_weeks=new_deadline_weeks
        )


def simple_rebalance(
    current_roadmap: Dict[str, Any],
    progress_data: Dict[str, Any],
    new_weekly_hours: Optional[int] = None,
    original_weekly_hours: int = 10
) -> Dict[str, Any]:
    """
    Simple rule-based rebalancing when LLM is unavailable.
    """
    current_week = progress_data.get('current_week', 1)
    total_weeks = current_roadmap.get('total_weeks', 12)
    
    # If weekly hours changed, adjust remaining weeks
    if new_weekly_hours and new_weekly_hours != original_weekly_hours:
        remaining_weeks = total_weeks - current_week
        hours_ratio = original_weekly_hours / new_weekly_hours
        new_remaining_weeks = int(remaining_weeks * hours_ratio)
        new_total = current_week + new_remaining_weeks
    else:
        new_total = total_weeks
    
    # Clone and update roadmap
    rebalanced = current_roadmap.copy()
    rebalanced['total_weeks'] = new_total
    rebalanced['last_rebalanced_at'] = None  # Will be set by caller
    
    rebalanced['rebalance_summary'] = {
        "weeks_added_or_removed": new_total - total_weeks,
        "tasks_redistributed": 0,
        "key_changes": ["Timeline adjusted based on new weekly hours"],
        "user_message": "Your roadmap has been adjusted to match your new availability. Keep going!"
    }
    
    return rebalanced
