"""
JSON validation utilities for agent outputs.
"""

import json
from typing import Dict, Any, Optional, List, Tuple
from pydantic import ValidationError


def validate_skill_gap_output(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate SkillGapAgent output.
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    required_fields = ['required_skills', 'missing_skills', 'priority_order']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(data[field], list):
            errors.append(f"Field '{field}' must be a list")
    
    if 'confidence_assessment' not in data:
        errors.append("Missing confidence_assessment")
    
    return (len(errors) == 0, errors)


def validate_roadmap_output(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate RoadmapAgent output.
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    if 'total_weeks' not in data:
        errors.append("Missing total_weeks")
    elif not isinstance(data['total_weeks'], int):
        errors.append("total_weeks must be an integer")
    
    if 'phases' not in data:
        errors.append("Missing phases")
    elif not isinstance(data['phases'], list):
        errors.append("phases must be a list")
    elif len(data['phases']) == 0:
        errors.append("phases cannot be empty")
    else:
        # Validate phase structure
        for i, phase in enumerate(data['phases']):
            phase_errors = validate_phase(phase, i)
            errors.extend(phase_errors)
    
    return (len(errors) == 0, errors)


def validate_phase(phase: Dict[str, Any], phase_index: int) -> List[str]:
    """Validate individual phase structure."""
    errors = []
    prefix = f"Phase {phase_index + 1}"
    
    if 'phase_name' not in phase:
        errors.append(f"{prefix}: Missing phase_name")
    
    if 'weeks' not in phase:
        errors.append(f"{prefix}: Missing weeks")
    elif not isinstance(phase['weeks'], list):
        errors.append(f"{prefix}: weeks must be a list")
    elif len(phase['weeks']) == 0:
        errors.append(f"{prefix}: weeks cannot be empty")
    else:
        for j, week in enumerate(phase['weeks']):
            week_errors = validate_week(week, phase_index, j)
            errors.extend(week_errors)
    
    return errors


def validate_week(week: Dict[str, Any], phase_index: int, week_index: int) -> List[str]:
    """Validate individual week structure."""
    errors = []
    prefix = f"Phase {phase_index + 1}, Week {week_index + 1}"
    
    required_fields = ['week_number', 'focus_skill', 'tasks', 'milestone', 'success_metric']
    
    for field in required_fields:
        if field not in week:
            errors.append(f"{prefix}: Missing {field}")
    
    if 'tasks' in week and not isinstance(week['tasks'], list):
        errors.append(f"{prefix}: tasks must be a list")
    
    if 'week_number' in week and not isinstance(week['week_number'], int):
        errors.append(f"{prefix}: week_number must be an integer")
    
    return errors


def sanitize_roadmap_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize and fix common issues in roadmap output.
    """
    sanitized = data.copy()
    
    # Ensure total_weeks is int
    if 'total_weeks' in sanitized:
        sanitized['total_weeks'] = int(sanitized['total_weeks'])
    
    # Ensure phases exist
    if 'phases' not in sanitized:
        sanitized['phases'] = []
    
    # Ensure each phase has required structure
    for phase in sanitized.get('phases', []):
        if 'phase_name' not in phase:
            phase['phase_name'] = 'Unnamed Phase'
        if 'weeks' not in phase:
            phase['weeks'] = []
        
        # Ensure each week has required structure
        for week in phase.get('weeks', []):
            if 'week_number' not in week:
                week['week_number'] = 1
            if 'focus_skill' not in week:
                week['focus_skill'] = 'General Learning'
            if 'tasks' not in week:
                week['tasks'] = []
            if 'milestone' not in week:
                week['milestone'] = 'Complete weekly tasks'
            if 'success_metric' not in week:
                week['success_metric'] = 'All tasks completed'
    
    return sanitized


def fix_json_response(response: str) -> Optional[Dict[str, Any]]:
    """
    Attempt to fix common JSON issues in LLM responses.
    """
    if not response:
        return None
    
    # Remove markdown code blocks
    clean = response.strip()
    if clean.startswith('```'):
        lines = clean.split('\n')
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line if it's ```)
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        clean = '\n'.join(lines)
    
    # Try to parse
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON object
    start = clean.find('{')
    end = clean.rfind('}')
    
    if start != -1 and end != -1:
        try:
            return json.loads(clean[start:end + 1])
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON array
    start = clean.find('[')
    end = clean.rfind(']')
    
    if start != -1 and end != -1:
        try:
            return json.loads(clean[start:end + 1])
        except json.JSONDecodeError:
            pass
    
    return None


def ensure_week_continuity(phases: List[Dict]) -> List[Dict]:
    """
    Ensure week numbers are continuous across all phases.
    """
    week_counter = 1
    
    for phase in phases:
        for week in phase.get('weeks', []):
            week['week_number'] = week_counter
            week_counter += 1
    
    return phases
