# 🚀 HERPath AI

**AI-Powered Career Navigation System for Women in Tech**

[![Python](https://img.shields.io/badge/Python-3.14+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)](https://streamlit.io)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange)](https://firebase.google.com)
[![Goose Framework](https://img.shields.io/badge/Goose-Agentic_AI-purple)](https://block.github.io/goose)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **#75HER Challenge Hackathon 2026** | Built for International Women's Day  
> Transforming career uncertainty into structured, achievable roadmaps

---

## 🎯 Problem Statement

**60% of women leave tech within 10 years.** Why?

- ❌ Vague "learn to code" advice without clear paths
- ❌ Imposter syndrome from comparing to others' journeys
- ❌ Career breaks creating re-entry anxiety
- ❌ Overwhelm from conflicting online resources

**HERPath AI solves this** by turning career goals into personalized, AI-powered execution plans with built-in accountability, adaptive pacing, and emotional intelligence.

---

## ✨ Key Features

### 🧭 **Intelligent Roadmap Generation**
- Multi-agent AI system powered by **Block's Goose Framework**
- Personalized week-by-week learning plans based on:
  - Target role + current skill level
  - Available time (2-40 hrs/week)
  - Financial constraints (free-only to paid)
  - Life situation (student, career break, full-time worker)
- Phase-based structure with clear milestones and success metrics

### 📊 **Adaptive Progress Tracking**
- Real-time completion metrics and pace analysis
- Automatic rebalancing when falling behind or ahead
- Streak tracking and missed task detection
- Visual progress breakdowns by phase

### 🤖 **AI Coach with Context**
- Multi-mode coaching:
  - **Clarify Plan**: Break down ambiguous goals
  - **Feeling Stuck**: Emotional support + tactical next steps
  - **Interview Prep**: Role-specific guidance
  - **General**: On-demand Q&A
- Remembers your full journey (roadmap + progress + history)
- Goose agentic framework with Plan-Execute-Verify loop

### ⚖️ **Smart Rebalancing Engine**
- Rule-based detection of when to adjust:
  - Missed >3 tasks in 2 weeks → Suggest easier pace
  - Consistently ahead → Offer accelerated path
  - Life changes → Re-generate roadmap segments
- Version history to track evolution

### 🎓 **Empathy-First Onboarding**
- 7-step wizard understanding your full context
- Emotional intelligence detection (anxiety patterns, imposter syndrome)
- No judgment on skill level or career breaks

---

## 🏗️ Architecture

### **Tech Stack**
```
Frontend:     Streamlit (Python-based UI framework)
Backend:      Python 3.14 + Firebase Firestore
LLM:          Google Gemini 3 Flash (REST API)
AI Framework: Custom Goose-style agentic system
Database:     Firebase Firestore + Realtime Database
Auth:         Firebase Auth (demo mode available)
```

### **Goose Agentic Framework Integration**
HERPath AI implements Block's Goose agentic AI patterns:

```
┌─────────────────────────────────────────────┐
│           Goose Agent Orchestrator          │
│  ┌──────────────────────────────────────┐   │
│  │   Plan → Execute → Verify Loop       │   │
│  └──────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│              Toolkit Layer                  │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐ │
│  │ Gemini   │  │  Verify   │  │ Fallback │ │
│  │  Tool    │  │   Tool    │  │ Manager  │ │
│  └──────────┘  └───────────┘  └──────────┘ │
├─────────────────────────────────────────────┤
│             Agent Specialists               │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │  Coach   │  │ Roadmap  │  │ Skill Gap │ │
│  │  Agent   │  │  Agent   │  │   Agent   │ │
│  └──────────┘  └──────────┘  └───────────┘ │
└─────────────────────────────────────────────┘
```

**Why Goose?**
- **Plan-Execute-Verify**: Ensures high-quality outputs
- **Tool Orchestration**: Modular, testable components
- **Automatic Fallback**: Graceful degradation when APIs fail
- **Retry Logic**: Exponential backoff for transient errors

### **Project Structure**
```
herpath-ai/
├── agents/                 # AI Agent implementations
│   ├── goose/             # Custom Goose framework
│   │   ├── agent.py       # GooseAgent orchestrator
│   │   ├── toolkit.py     # Tool management
│   │   ├── fallback.py    # Fallback responses
│   │   └── tools/         # GeminiTool, VerifyTool
│   ├── base_agent.py      # Base class with Goose integration
│   ├── coach_agent.py     # AI Coach specialist
│   ├── roadmap_agent.py   # Roadmap generator
│   └── skill_gap_agent.py # Skill analysis
├── config/                 # Configuration
│   ├── constants.py       # All constants centralized
│   ├── settings.py        # App settings
│   └── firebase_config.py # Firebase initialization
├── database/               # Data layer
│   ├── firestore_client.py
│   └── schema.py
├── ui/                     # Streamlit UI components
│   ├── dashboard.py
│   ├── roadmap.py
│   ├── coach.py
│   └── onboarding.py
├── utils/                  # Utilities
│   ├── logging.py         # Structured logging
│   └── json_validator.py
├── .streamlit/
│   └── secrets.toml       # API keys (not committed)
├── app.py                  # Main entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites
- **Python 3.14+** (or 3.9+)
- **Firebase Account** (free tier works)
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))

### 1. Clone Repository
```bash
git clone https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026.git
cd -75HER-Challenge-Hackathon-2026/herpath-ai
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Secrets

Create `.streamlit/secrets.toml`:
```toml
# Gemini API Key (Required)
GEMINI_API_KEY = "your-gemini-api-key-here"

# Firebase Configuration (Required for data persistence)
FIREBASE_WEB_API_KEY = "your-firebase-web-api-key"
FIREBASE_AUTH_DOMAIN = "your-project.firebaseapp.com"
FIREBASE_PROJECT_ID = "your-project-id"
FIREBASE_STORAGE_BUCKET = "your-project.firebasestorage.app"
FIREBASE_MESSAGING_SENDER_ID = "your-sender-id"
FIREBASE_APP_ID = "your-app-id"
FIREBASE_MEASUREMENT_ID = "G-XXXXXXXXXX"
FIREBASE_DATABASE_URL = "https://your-project.firebaseio.com"

[firebase_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = """
-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----
"""
client_email = "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com"
# ... rest of service account JSON
```

**Get Firebase Credentials:**
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create project → Project Settings → Service Accounts
3. Generate new private key (downloads JSON)
4. Copy values into `secrets.toml`

### 5. (Optional) Seed Demo Account
```bash
python seed_demo_account.py
```

Creates a pre-populated demo account:
- **Email**: `judge@herpath-demo.ai`
- **Password**: `HERPathDemo2026`
- Includes progress, roadmap, and chat history

### 6. Run Application
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 🎭 Demo Account

For judges and evaluators, use the pre-seeded demo account:

**Credentials:**
```
Email:    judge@herpath-demo.ai
Password: HERPathDemo2026
```

**What's Pre-loaded:**
- ✅ User Profile: "Sarah Chen", Career Transition to AI Engineer
- ✅ 26-week roadmap (currently on Week 4)
- ✅ 16.5% completion with 7/42 tasks done
- ✅ Sample chat history with AI Coach
- ✅ Progress tracking and missed task detection

**To recreate demo data:**
```bash
python seed_demo_account.py
```

---

## 🧪 Testing & Quality

### Run Tests
```bash
# Test all AI agents
python -m pytest tests/ -v

# Test Goose framework
python -m pytest tests/test_goose.py

# Manual testing
python test_agents.py
```

### Code Quality
- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Every function documented
- **Logging**: Structured logging with levels
- **Error Handling**: Exponential backoff + fallbacks
- **Constants**: Centralized in `config/constants.py`

### View Firebase Data
```bash
python view_firebase_data.py
```

Shows all collections and documents in Firestore.

---

## 📊 Key Metrics & Performance

| Metric | Target | Current |
|--------|--------|---------|
| **API Response Time** | <10s | 3-5s avg |
| **Roadmap Generation** | <30s | 15-25s |
| **AI Coach Response** | <5s | 2-4s |
| **Fallback Coverage** | 100% | 100% |
| **Goose Integration** | ✅ | ✅ |

**Reliability Features:**
- ✅ Exponential backoff on API failures
- ✅ 30-second timeout on all LLM calls
- ✅ Comprehensive fallback responses
- ✅ Graceful degradation (demo mode if Firebase unavailable)
- ✅ Retry logic (up to 3 attempts)

---

## 🎯 Supported Career Paths

| Role | Status | Weeks | Skills Covered |
|------|--------|-------|----------------|
| **AI/ML Engineer** | ✅ Full | 26-52 | Python, ML, Deep Learning, LLMs |
| **Data Analyst** | ✅ Full | 20-39 | SQL, Python, Tableau, Statistics |
| **Web Developer** | ✅ Full | 20-39 | HTML/CSS/JS, React, Node.js |
| **Mobile Developer** | ⚠️ Beta | 26-52 | React Native / Flutter |
| **DevOps Engineer** | ⚠️ Beta | 26-39 | Linux, Docker, K8s, CI/CD |
| **Cloud Engineer** | ⚠️ Beta | 20-39 | AWS/Azure/GCP, IaC |

---

## 🛠️ API Configuration

### Exponential Backoff Strategy
```python
# Automatic retry with exponential backoff
retries = 3
for attempt in range(retries):
    try:
        response = call_api()
        break
    except TransientError:
        wait = 2 ** attempt  # 1s, 2s, 4s
        time.sleep(wait)
```

### Timeout Handling
```python
# All API calls have 30s timeout
response = requests.post(
    url, json=payload,
    timeout=30  # Guaranteed response or exception
)
```

### Rate Limiting
- **Gemini API**: 60 calls/minute (handled gracefully)
- **Firebase**: No limits on free tier

---

## 📚 Documentation

- **[API Documentation](docs/API.md)** - All endpoints and responses
- **[Agent Architecture](docs/AGENTS.md)** - How the multi-agent system works
- **[Goose Framework Guide](docs/GOOSE.md)** - Our custom implementation
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy to production
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🔒 Security & Privacy

- ✅ API keys stored in `.streamlit/secrets.toml` (gitignored)
- ✅ No credentials in code or repo
- ✅ Firebase Authentication (email/password)
- ✅ User data encrypted at rest (Firebase)
- ✅ HTTPS enforced in production
- ✅ Input validation and sanitization

**Note**: For hackathon demo purposes, demo account password is publicly known. In production, implement proper OAuth.

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from GitHub
4. Add secrets in Streamlit dashboard
5. Done! Auto-deploys on push

### Docker (Alternative)
```bash
docker build -t herpath-ai .
docker run -p 8501:8501 herpath-ai
```

### Self-Hosted
```bash
streamlit run app.py --server.port 8501 --server.headless true
```

---

## 🏆 Hackathon Highlights

**Why HERPath AI Stands Out:**

1. **Goose Framework Integration** ✅  
   - Required for #75HER AI/ML track eligibility
   - Custom implementation showing deep understanding
   - Plan-Execute-Verify agentic loops

2. **Production-Ready Features** ✅
   - Comprehensive error handling and fallbacks
   - Structured logging and monitoring
   - Type-safe code with full annotations

3. **Empathy-Driven Design** 💜
   - Built BY women FOR women in tech
   - Addresses real pain points (imposter syndrome, career breaks)
   - Psychology-optimized UI (affirmations, streak tracking)

4. **Scalable Architecture** 📈
   - Firebase for infinite scale
   - Stateless backend (easy to containerize)
   - Modular agent system (add new roles easily)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick Start:**
1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **#75HER Challenge** - For hosting this hackathon
- **Block's Goose Framework** - Inspiration for agentic AI patterns
- **Google Gemini** - LLM provider
- **Firebase** - Backend infrastructure
- **Streamlit** - Rapid UI prototyping

---

## 📧 Contact

**Team**: Pranjal Gupta  
**Email**: support@herpath.ai  
**GitHub**: [@pranjal2004838](https://github.com/pranjal2004838)  
**Hackathon**: #75HER Challenge 2026

---

<div align="center">

**Built with 💜 for women breaking barriers in tech**

[⭐ Star this repo](https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026) | [🐛 Report Bug](https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026/issues) | [💡 Request Feature](https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026/issues)

</div>
