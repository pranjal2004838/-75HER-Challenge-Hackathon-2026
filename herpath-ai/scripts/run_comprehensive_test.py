#!/usr/bin/env python3
"""
Start Streamlit app and run comprehensive tests.
"""
import subprocess
import sys
import time
import requests
import os
import signal

def wait_for_streamlit(url="http://localhost:8501", timeout=40, check_interval=0.5):
    """Wait for Streamlit to be ready."""
    print(f"\n⏳ Waiting for Streamlit to start on {url}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✓ Streamlit is ready!")
                return True
        except:
            pass
        time.sleep(check_interval)
    
    print(f"✗ Streamlit failed to start within {timeout} seconds")
    return False

def main():
    print("\n" + "="*80)
    print("STARTING HERPATH AI - COMPREHENSIVE MANUAL TEST")
    print("="*80)
    
    print("\n1. Starting Streamlit server...")
    
    # Kill any existing processes
    os.system('taskkill /F /IM python.exe /T 2>nul || echo "Cleaned up"')
    time.sleep(2)
    
    # Start Streamlit
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--logger.level=error"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.path.join(os.path.dirname(__file__), "..")
    )
    
    print(f"✓ Streamlit process started (PID: {streamlit_process.pid})")
    
    # Wait for Streamlit to be ready
    if not wait_for_streamlit():
        print("✗ Streamlit failed to start - aborting tests")
        streamlit_process.terminate()
        return 1
    
    time.sleep(2)
    
    print("\n2. Running comprehensive test suite...")
    print("-" * 80)
    
    try:
        # Run test
        test_process = subprocess.run(
            [sys.executable, "scripts/comprehensive_manual_test.py"],
            cwd=os.path.dirname(__file__),
            capture_output=False
        )
        
        test_exit_code = test_process.returncode
        
    except Exception as e:
        print(f"✗ Test failed to run: {e}")
        test_exit_code = 1
    
    finally:
        print("\n3. Shutting down Streamlit...")
        try:
            streamlit_process.terminate()
            streamlit_process.wait(timeout=5)
        except:
            streamlit_process.kill()
        print("✓ Streamlit stopped")
    
    return test_exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
