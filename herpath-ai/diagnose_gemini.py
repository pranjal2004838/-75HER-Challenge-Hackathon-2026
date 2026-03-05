"""
Gemini API Diagnostics - Debug tool for Gemini issues
======================================================

This tool helps diagnose why Gemini API calls are failing.
Run when you see API errors to get detailed diagnostics.

Usage:
    python diagnose_gemini.py
"""

import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def diagnose_api_key() -> tuple[bool, str]:
    """Check if API key exists and format is valid."""
    print("\n[DIAGNOSTIC 1] API Key Configuration")
    print("-" * 60)
    
    # Try all sources
    api_key = None
    source = None
    
    # Source 1: Streamlit secrets
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY")
        if key and len(key) > 20:
            api_key = key
            source = "Streamlit secrets"
    except Exception as e:
        logger.debug(f"Streamlit secrets unavailable: {e}")
    
    # Source 2: Environment variable
    if not api_key:
        key = os.getenv("GEMINI_API_KEY")
        if key and len(key) > 20:
            api_key = key
            source = "Environment variable"
    
    # Source 3: .env file
    if not api_key:
        try:
            from dotenv import load_dotenv, find_dotenv
            dotenv_path = find_dotenv()
            if dotenv_path:
                load_dotenv(dotenv_path, override=False)
                key = os.getenv("GEMINI_API_KEY")
                if key and len(key) > 20:
                    api_key = key
                    source = f".env file ({dotenv_path})"
        except Exception as e:
            logger.debug(f"Failed to load .env: {e}")
    
    if not api_key:
        print("❌ FAIL: No API key found in any source")
        print("   Checked: Streamlit secrets, environment vars, .env file")
        return False, "No API key found"
    
    print(f"✓ PASS: API key found from {source}")
    print(f"   Key (hidden): {api_key[:10]}...{api_key[-10:]}")
    
    # Validate format
    if not api_key.startswith("AIzaSy"):
        print("⚠ WARNING: Key does not start with 'AIzaSy' (typical for Gemini)")
        print("   This might be an invalid key")
        return False, "Invalid key format"
    
    return True, api_key


def test_api_key(api_key: str) -> tuple[bool, str]:
    """Test if the API key is valid and not revoked."""
    print("\n[DIAGNOSTIC 2] API Key Validation")
    print("-" * 60)
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Say OK"}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 5
        }
    }
    
    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15
        )
        
        print(f"   HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ PASS: API key is VALID and accepted")
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"   API Response: '{text.strip()}'")
            return True, "API key valid"
        
        elif response.status_code == 403:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown 403 error")
            print(f"❌ FAIL: {response.status_code} - Access Denied")
            print(f"   Error: {error_msg}")
            
            if "leaked" in error_msg.lower():
                print("\n   🚨 CRITICAL: Your API key was reported as LEAKED!")
                print("   You MUST generate a new API key:")
                print("   1. Go to https://ai.google.dev/")
                print("   2. Click 'Get API Key'")
                print("   3. Create a new key (old one is compromised)")
                print("   4. Update .streamlit/secrets.toml")
                return False, error_msg
            
            return False, error_msg
        
        elif response.status_code == 400:
            print(f"❌ FAIL: {response.status_code} - Bad Request")
            print("   API key might be invalid or malformed")
            return False, "Bad request (invalid key?)"
        
        elif response.status_code == 401:
            print(f"❌ FAIL: {response.status_code} - Unauthorized")
            print("   API key authentication failed")
            return False, "Unauthorized (invalid key?)"
        
        else:
            print(f"❌ FAIL: {response.status_code} - {response.text[:200]}")
            return False, f"HTTP {response.status_code}"
        
    except requests.exceptions.Timeout:
        print("❌ FAIL: Request timed out (15 second timeout)")
        print("   Network issue or API server is very slow")
        return False, "Timeout"
    
    except requests.exceptions.ConnectionError as e:
        print(f"❌ FAIL: Cannot connect to Gemini API")
        print(f"   Network error: {str(e)[:100]}")
        return False, "Connection error"
    
    except Exception as e:
        print(f"❌ FAIL: Unexpected error")
        print(f"   {type(e).__name__}: {str(e)[:100]}")
        return False, f"Error: {type(e).__name__}"


def test_endpoint_accessibility() -> tuple[bool, str]:
    """Test if the Gemini API endpoint is reachable."""
    print("\n[DIAGNOSTIC 3] Endpoint Accessibility")
    print("-" * 60)
    
    endpoint = "https://generativelanguage.googleapis.com"
    
    try:
        response = requests.head(endpoint, timeout=5)
        print(f"✓ PASS: Gemini API endpoint is reachable")
        print(f"   Status: {response.status_code}")
        return True, "Endpoint accessible"
    except requests.exceptions.Timeout:
        print("❌ FAIL: Endpoint timeout (network issue)")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ FAIL: Cannot reach endpoint")
        print(f"   {str(e)[:100]}")
        return False, "Unreachable"


def run_all_diagnostics():
    """Run all diagnostic tests."""
    print("\n" + "=" * 60)
    print("GEMINI API DIAGNOSTICS")
    print("=" * 60)
    
    results = {
        "tests_passed": 0,
        "tests_failed": 0,
        "critical_issues": []
    }
    
    # Test 1: API Key Loading
    success, api_key = diagnose_api_key()
    if success:
        results["tests_passed"] += 1
    else:
        results["tests_failed"] += 1
        results["critical_issues"].append(api_key)
        print("\n" + "=" * 60)
        print("CANNOT CONTINUE - API key issue must be fixed first")
        print("=" * 60)
        return results
    
    # Test 2: API Key Validation
    success, message = test_api_key(api_key)
    if success:
        results["tests_passed"] += 1
    else:
        results["tests_failed"] += 1
        results["critical_issues"].append(message)
    
    # Test 3: Endpoint Accessibility
    success, message = test_endpoint_accessibility()
    if success:
        results["tests_passed"] += 1
    else:
        results["tests_failed"] += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {results['tests_passed']}/3 tests passed")
    
    if results["critical_issues"]:
        print(f"CRITICAL ISSUES:")
        for issue in results["critical_issues"]:
            print(f"  - {issue}")
    
    if results["tests_failed"] == 0:
        print("\n✓ ALL DIAGNOSTICS PASSED - API IS WORKING!")
    else:
        print(f"\n❌ {results['tests_failed']} DIAGNOSTIC(S) FAILED")
        print("\nNEXT STEPS:")
        print("1. Verify you have a valid Gemini API key from https://ai.google.dev/")
        print("2. Update .streamlit/secrets.toml with the new key")
        print("3. Run this diagnostic again")
    
    print("=" * 60 + "\n")
    
    return results


if __name__ == "__main__":
    run_all_diagnostics()
