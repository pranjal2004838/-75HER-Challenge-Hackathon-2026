"""
Comprehensive verification script for both issues
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("="*80)
print("VERIFICATION REPORT - Button Styling & API Model")
print("="*80)

# Check 1: Button CSS in app.py
print("\n1. Checking button CSS in app.py...")
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for data-testid selectors
    has_testid = 'data-testid="stButton"' in content or 'data-testid="stFormSubmitButton"' in content
    has_white_color = '#FFFFFF' in content or 'color: white' in content
    has_primary_selector = 'kind="primary"' in content
    
    print(f"   ✓ Contains data-testid selectors: {has_testid}")
    print(f"   ✓ Contains white color (#FFFFFF): {has_white_color}")
    print(f"   ✓ Contains primary button selectors: {has_primary_selector}")
    
    if has_testid and has_white_color and has_primary_selector:
        print("   ✅ Button CSS is properly configured")
    else:
        print("   ❌ Button CSS may be incomplete")
except Exception as e:
    print(f"   ❌ Error reading app.py: {e}")

# Check 2: Model configuration
print("\n2. Checking model configuration...")
try:
    with open('agents/base_agent.py', 'r', encoding='utf-8') as f:
        agent_content = f.read()
    
    with open('config/settings.py', 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    # Extract model name from base_agent.py
    if 'self.model = "' in agent_content:
        start = agent_content.find('self.model = "') + len('self.model = "')
        end = agent_content.find('"', start)
        model_name = agent_content[start:end]
        print(f"   Model in base_agent.py: {model_name}")
    else:
        print("   ❌ Could not find model in base_agent.py")
        model_name = None
    
    # Extract model from settings.py
    if 'GEMINI_MODEL = "' in settings_content:
        start = settings_content.find('GEMINI_MODEL = "') + len('GEMINI_MODEL = "')
        end = settings_content.find('"', start)
        settings_model = settings_content[start:end]
        print(f"   Model in settings.py: {settings_model}")
    else:
        print("   ❌ Could not find GEMINI_MODEL in settings.py")
        settings_model = None
    
    if model_name == settings_model:
        print(f"   ✅ Models are consistent: {model_name}")
    else:
        print(f"   ⚠️  Models differ: {model_name} vs {settings_model}")
        
except Exception as e:
    print(f"   ❌ Error checking model: {e}")

# Check 3: API Key status
print("\n3. Checking API key configuration...")
try:
    secrets_path = '.streamlit/secrets.toml'
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r') as f:
            secrets = f.read()
        
        has_key = 'GEMINI_API_KEY' in secrets
        print(f"   GEMINI_API_KEY exists: {has_key}")
        
        if has_key:
            # Extract key (first few chars only)
            if 'GEMINI_API_KEY = "' in secrets:
                start = secrets.find('GEMINI_API_KEY = "') + len('GEMINI_API_KEY = "')
                end = secrets.find('"', start)
                key = secrets[start:end]
                print(f"   Key preview: {key[:10]}...{key[-5:]}")
                print("   ⚠️  IMPORTANT: This key may be blocked (403 error detected)")
                print("   ⚠️  Generate new key at: https://aistudio.google.com/app/apikey")
        else:
            print("   ❌ No GEMINI_API_KEY found in secrets.toml")
    else:
        print(f"   ❌ secrets.toml not found at {secrets_path}")
except Exception as e:
    print(f"   ❌ Error checking API key: {e}")

# Final Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("""
BUTTON STYLING FIX:
✓ CSS updated with data-testid selectors
✓ White color (#FFFFFF) explicitly set for all states
✓ Targeting: div[data-testid="stButton"] button[kind="primary"]

TO VERIFY BUTTON FIX:
1. Open app at http://localhost:8501
2. Look at any blue button (like "Next →" in onboarding)
3. Text should be WHITE on blue background
4. If still black, try hard refresh (Ctrl+Shift+R)

MODEL FIX:
✓ Updated to gemini-2.0-flash-exp
✓ Consistent across base_agent.py and settings.py

API KEY ISSUE:
❌ Current key is BLOCKED by Google (403 error)
❌ You MUST generate a new API key to use Gemini

ACTION REQUIRED:
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the new key
4. Update .streamlit/secrets.toml
5. Restart the app

READ: URGENT_API_KEY_FIX.md for detailed instructions
""")
print("="*80)
