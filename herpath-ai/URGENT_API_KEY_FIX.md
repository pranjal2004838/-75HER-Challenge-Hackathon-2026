# ⚠️ URGENT: API KEY ISSUE DETECTED

## Problem
Your Gemini API key has been flagged as **LEAKED** by Google and has been **BLOCKED**.

### Error Message:
```
{
  "error": {
    "code": 403,
    "message": "Your API key was reported as leaked. Please use another API key.",
    "status": "PERMISSION_DENIED"
  }
}
```

## Solution - Generate New API Key IMMEDIATELY

### Step 1: Go to Google AI Studio
Visit: https://makersuite.google.com/app/apikey
(or https://aistudio.google.com/app/apikey)

### Step 2: Create New API Key
1. Click "Create API Key"
2. Select your Google Cloud project (or create new one)
3. Copy the new API key

### Step 3: Update Your secrets.toml
Open: `herpath-ai/.streamlit/secrets.toml`

Replace the old key with new one:
```toml
GEMINI_API_KEY = "YOUR_NEW_KEY_HERE"
```

### Step 4: Restart the App
```powershell
cd herpath-ai
# Kill any running Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
# Wait a moment
Start-Sleep -Seconds 2
# Restart Streamlit
streamlit run app.py --server.port 8501
```

## Important Security Tips

1. **Never commit API keys to git** - they are in .gitignore already
2. **Don't share screenshots** with visible API keys
3. **Rotate keys regularly** if used in public/shared environments
4. **Set up API key restrictions** in Google Cloud Console:
   - Restrict to specific IPs (your deployment server)
   - Restrict to specific APIs (Generative Language API only)

## Current Status
- Model has been updated to `gemini-2.0-flash-exp`
- Button styling has been fixed with maximum CSS specificity
- App is ready to run once you update the API key

## After Fixing
Once you've updated the API key, test by:
1. Opening the app at http://localhost:8501
2. Going to AI Coach
3. Sending a test message
4. Checking that it responds (no 403 errors)
