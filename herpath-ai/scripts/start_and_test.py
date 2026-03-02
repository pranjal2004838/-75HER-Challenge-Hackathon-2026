#!/usr/bin/env python3
"""
Start Streamlit app and verify it's running, then run E2E tests.
"""
import subprocess
import time
import requests
import sys
import os

def wait_for_streamlit(url="http://localhost:8501", timeout=30):
    """Wait for Streamlit to be ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

print("\n" + "="*70)
print("[STARTUP] Starting HERPath AI Streamlit App")
print("="*70 + "\n")

# Start Streamlit in background
print("Starting Streamlit on localhost:8501...")
try:
    # Start Streamlit process
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--logger.level=error"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for it to be ready
    if wait_for_streamlit():
        print("✓ Streamlit is running and ready")
        print("\nRunning E2E tests with both fixes applied...\n")
        
        # Run E2E tests
        result = subprocess.run(
            [sys.executable, "scripts/e2e_test_automation.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        sys.exit(result.returncode)
    else:
        print("✗ Streamlit failed to start within timeout")
        proc.terminate()
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
