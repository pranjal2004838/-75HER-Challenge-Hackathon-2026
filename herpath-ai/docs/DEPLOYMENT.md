# Deployment Guide

## Overview

HERPath AI is built on **Streamlit** (frontend) + **Firebase** (backend) and is designed for rapid deployment to Streamlit Cloud, Docker, or self-hosted servers.

---

## Quick Deploy: Streamlit Cloud ⚡

The easiest option for judges and demos.

### Steps:

1. **Fork the repository** to your GitHub account
   ```
   https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026
   ```

2. **Go to Streamlit Cloud**
   ```
   https://share.streamlit.io/
   ```

3. **Click "New App" → Deploy from GitHub**
   - Select your fork
   - Select branch: `main`
   - Set main file path: `herpath-ai/app.py`

4. **Configure Secrets**
   - In Streamlit Cloud dashboard, click "⚙️ Settings"
   - Go to "Secrets"
   - Add your `.streamlit/secrets.toml` content:
   ```toml
   GEMINI_API_KEY = "your-key"
   FIREBASE_PROJECT_ID = "your-project-id"
   [firebase_credentials]
   type = "service_account"
   # ... rest of your Firebase service account JSON
   ```

5. **Deploy**
   - Streamlit auto-deploys on every push to main
   - Your app is live at: `https://yourname-herpath-ai.streamlit.app/`

---

## Detailed Setup: Firebase + Gemini API

### Prerequisites:

- Firebase account (free tier works)
- Google Cloud project with Gemini API enabled
- Python 3.9+

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. **Create new project**
3. Use Google Analytics (optional)
4. Wait for project to initialize

### 2. Set Up Firebase Services

#### **Firestore Database:**
1. Go to **Firestore Database**
2. Click **"Create Database"**
3. Select region: `us-central1` (or closest to you)
4. Start in **Test Mode** (for development)
5. Create

#### **Firebase Authentication:**
1. Go to **Authentication** → **Sign-in method**
2. Enable **Email/Password**
3. Optional: Enable Google, GitHub sign-in

#### **Firebase Realtime Database (Optional):**
1. Go to **Realtime Database**
2. Create database in test mode

### 3. Get Credentials

#### **Service Account JSON:**
1. Go to **Project Settings** (⚙️) → **Service Accounts**
2. Click **"Generate New Private Key"**
3. Save the JSON file locally
4. Copy the contents into `secrets.toml`

#### **Web API Key:**
1. Go to **Project Settings** (⚙️) → **General**
2. Find the **Web API Key** (looks like `AIza...`)
3. Add to `secrets.toml` as `FIREBASE_WEB_API_KEY`

### 4. Enable Gemini API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. **Enable API/Service**: Search for "Generative Language API"
3. Click **Enable**
4. Go to **Credentials** → **Create API Key**
5. Copy the key to `secrets.toml` as `GEMINI_API_KEY`

### 5. Configure Secrets

Create `herpath-ai/.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "AIza..."

FIREBASE_WEB_API_KEY = "AIza..."
FIREBASE_AUTH_DOMAIN = "your-project.firebaseapp.com"
FIREBASE_PROJECT_ID = "your-project-id"
FIREBASE_STORAGE_BUCKET = "your-project.firebasestorage.app"
FIREBASE_MESSAGING_SENDER_ID = "123456789"
FIREBASE_APP_ID = "1:123456789:web:abcdef123456"
FIREBASE_MEASUREMENT_ID = "G-XXXXXXXXXX"
FIREBASE_DATABASE_URL = "https://your-project.firebaseio.com"

[firebase_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = """
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
client_email = "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

---

## Option 1: Streamlit Cloud (Recommended)

Already covered above. **Best for:** Public demos, rapid deployment, auto-scaling.

**Cost:** Free tier includes unlimited apps

**Time to deploy:** ~5 minutes

---

## Option 2: Docker Container

For self-hosted or cloud VMs (AWS, Azure, GCP, etc.)

### Build Image:

```bash
cd herpath-ai
docker build -t herpath-ai:latest .
```

### Run Locally:

```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="AIza..." \
  -e FIREBASE_PROJECT_ID="your-project" \
  herpath-ai:latest
```

App will be at `http://localhost:8501`

### Push to Registry (Docker Hub):

```bash
docker tag herpath-ai:latest yourname/herpath-ai:latest
docker push yourname/herpath-ai:latest
```

### Deploy to Cloud VMs:

**AWS EC2:**
```bash
# On EC2 instance:
docker pull yourname/herpath-ai:latest
docker run -d -p 80:8501 yourname/herpath-ai:latest
```

**Google Cloud Run:**
```bash
gcloud run deploy herpath-ai \
  --image yourname/herpath-ai:latest \
  --set-env-vars GEMINI_API_KEY="AIza...",FIREBASE_PROJECT_ID="..."
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group mygroup \
  --name herpath-ai \
  --image yourname/herpath-ai:latest \
  --ports 8501
```

---

## Option 3: Self-Hosted (Linux/macOS/Windows)

### Install Dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Set Environment Variables:

```bash
export GEMINI_API_KEY="AIza..."
export FIREBASE_PROJECT_ID="your-project"
# ... other env vars
```

Or create `.env` file:
```
GEMINI_API_KEY=AIza...
FIREBASE_PROJECT_ID=your-project
```

### Run Server:

```bash
streamlit run app.py \
  --server.port 8501 \
  --server.headless true \
  --logger.level=info
```

### Use Nginx as Reverse Proxy:

```nginx
server {
    listen 80;
    server_name herpath.ai;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Enable HTTPS with Let's Encrypt:

```bash
sudo apt install certbot nginx-certbot
sudo certbot certonly --nginx -d herpath.ai
```

---

## Scaling & Performance

### **For 10-100 users:**
- Streamlit Cloud: ✅ Sufficient
- Firebase free tier: ✅ Sufficient (10k daily reads)
- Gemini API: ✅ Sufficient (60 calls/min)

### **For 1000+ users:**
- Use Docker on Kubernetes (auto-scale)
- Upgrade Firebase plan
- Implement Redis caching
- Use FastAPI instead of Streamlit

---

## Monitoring & Logging

### **Streamlit Cloud:**
View logs in real-time:
1. Go to app settings
2. View logs in dashboard

### **Docker:**
```bash
docker logs -f herpath-ai
```

### **Self-hosted:**
Set log level in `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Security Checklist

- [ ] Secrets stored in environment variables (not in code)
- [ ] Firebase rules set to `test` mode for dev, `production` for prod
- [ ] API rate limiting enabled (Gemini: 60 calls/min)
- [ ] HTTPS enforced (redirect HTTP → HTTPS)
- [ ] User data encrypted at rest (Firebase default)
- [ ] Regular backups of Firestore data
- [ ] Monitor API costs (set billing alerts)

---

## CI/CD Pipeline (Optional)

### **GitHub Actions - Auto Deploy on Push:**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Streamlit Cloud
        uses: streamlit/streamlit-cloud-deploy-action@v1
        with:
          app_path: herpath-ai/app.py
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Troubleshooting

### Problem: "Cannot connect to Firestore"
**Solution:** 
- Check `secrets.toml` has correct Firebase credentials
- Verify Firestore database is in test mode (if development)
- Check Firebase rules allow reads/writes

### Problem: "Gemini API rate limit exceeded"
**Solution:**
- Add exponential backoff (already implemented)
- Upgrade to paid Gemini API tier
- Implement caching for repeated requests

### Problem: "Streamlit app is slow"
**Solution:**
- Use `@st.cache_data` for expensive computations
- Reduce Firebase reads (implement caching)
- Optimize Gemini prompts (fewer tokens)

---

## Future: FastAPI Backend

For production scale, migrate to FastAPI:

```python
# api/main.py
from fastapi import FastAPI
from agents.coach_agent import CoachAgent

app = FastAPI()
coach = CoachAgent()

@app.post("/coach/chat")
async def coach_chat(user_state: dict, message: str):
    response = coach.chat(user_state=user_state, ...)
    return {"response": response}
```

Deploy with:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Then Streamlit frontend calls API:
```python
response = requests.post("https://api.herpath.ai/coach/chat", json={...})
```

---

## Cost Estimates (Monthly)

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| Streamlit Cloud | Unlimited | Public app | $0 |
| Firebase Firestore | 10k reads | 100 users | $0-10 |
| Gemini API | $300 credits | ~1000 calls | $0-1 |
| **Total** | | | **$0-15** |

---

## Support

- Streamlit docs: https://docs.streamlit.io/
- Firebase docs: https://firebase.google.com/docs/
- Gemini API: https://ai.google.dev/
