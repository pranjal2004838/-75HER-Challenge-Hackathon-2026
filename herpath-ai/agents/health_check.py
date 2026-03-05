"""
Health Check System - Verify all critical services before demo
================================================================

This module provides pre-flight checks to ensure:
- Gemini API is reachable and responding
- Firebase is configured and accessible  
- All API keys are valid
- Fallback systems are working

Use before recording demo video or during demo day.
"""

import logging
import requests
import time
import json
import os
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)


def check_gemini_api() -> Tuple[bool, str]:
    """
    Check if Gemini API is accessible and responding.
    
    Returns:
        (success: bool, message: str)
    """
    try:
        from agents.base_agent import get_gemini_api_key
        
        api_key = get_gemini_api_key()
        if not api_key or len(api_key) < 20:
            return False, "Gemini API key not found or invalid"
        
        # Test with a simple request
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
        
        payload = {
            "contents": [{
                "parts": [{"text": "Say 'OK' briefly."}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 10
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        # Request with timeout
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return True, "Gemini API is responsive and working"
            else:
                return False, f"Unexpected response format: {str(data)[:100]}"
        
        elif response.status_code == 429:
            return False, "Gemini API rate limit exceeded (too many requests)"
        elif response.status_code == 400:
            return False, "Gemini API key is invalid or API not enabled"
        elif response.status_code == 401:
            return False, "Gemini API authentication failed"
        else:
            return False, f"Gemini API error {response.status_code}: {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        return False, "Gemini API request timed out (network issue or server slow)"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to Gemini API (network connectivity issue)"
    except Exception as e:
        return False, f"Gemini check failed: {type(e).__name__}: {str(e)[:100]}"


def check_firebase() -> Tuple[bool, str]:
    """
    Check if Firebase is configured and accessible.
    
    Returns:
        (success: bool, message: str)
    """
    try:
        from config.firebase_config import get_firestore_client
        
        db = get_firestore_client()
        
        # Try a simple read operation
        docs = db.collection("_health_check").limit(1).stream()
        list(docs)  # Consume the iterator
        
        return True, "Firebase Firestore is accessible"
        
    except Exception as e:
        return False, f"Firebase check failed: {type(e).__name__}: {str(e)[:100]}"


def check_fallback_system() -> Tuple[bool, str]:
    """
    Check if fallback responses are available.
    
    Returns:
        (success: bool, message: str)
    """
    try:
        from agents.goose.fallback import get_fallback_manager
        
        manager = get_fallback_manager()
        
        # Test getting fallback for each agent type
        for agent_type in ["coach", "roadmap", "skill_gap", "rebalance"]:
            fallback = manager.get_fallback(agent_type=agent_type, mode="general")
            if not fallback or not fallback.content:
                return False, f"Fallback missing for {agent_type}"
        
        return True, "All fallback responses available"
        
    except Exception as e:
        return False, f"Fallback system check failed: {type(e).__name__}: {str(e)[:100]}"


def run_all_checks() -> Dict[str, Any]:
    """
    Run all health checks and return consolidated report.
    
    Returns:
        dict with checks, results, and overall status
    """
    print("\n" + "="*70)
    print("HERPATH AI - PRE-DEMO HEALTH CHECK")
    print("="*70)
    
    results = {
        "timestamp": time.time(),
        "checks": {},
        "all_passed": True,
        "critical_failures": []
    }
    
    # Check 1: Gemini API
    print("\n[1/3] Checking Gemini API connectivity...")
    success, message = check_gemini_api()
    results["checks"]["gemini_api"] = {"success": success, "message": message}
    print(f"      {'[PASS]' if success else '[FAIL]'} {message}")
    if not success:
        results["all_passed"] = False
        results["critical_failures"].append("Gemini API")
    
    # Check 2: Firebase
    print("\n[2/3] Checking Firebase connectivity...")
    success, message = check_firebase()
    results["checks"]["firebase"] = {"success": success, "message": message}
    print(f"      {'[PASS]' if success else '[FAIL]'} {message}")
    if not success:
        results["all_passed"] = False
        results["critical_failures"].append("Firebase")
    
    # Check 3: Fallback System
    print("\n[3/3] Checking fallback system...")
    success, message = check_fallback_system()
    results["checks"]["fallback_system"] = {"success": success, "message": message}
    print(f"      {'[PASS]' if success else '[FAIL]'} {message}")
    if not success:
        results["all_passed"] = False
        results["critical_failures"].append("Fallback System")
    
    # Summary
    print("\n" + "="*70)
    if results["all_passed"]:
        print("STATUS: ALL CHECKS PASSED - READY FOR DEMO")
    else:
        print(f"STATUS: {len(results['critical_failures'])} CRITICAL FAILURES")
        for failure in results["critical_failures"]:
            print(f"  - {failure}")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    # Run health check when executed directly
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    
    report = run_all_checks()
    
    # Exit with non-zero code if checks failed
    if not report["all_passed"]:
        sys.exit(1)
