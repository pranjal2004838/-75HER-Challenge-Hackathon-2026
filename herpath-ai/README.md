# HERPath AI 🚀

**Adaptive Career Execution System for Women in Tech**

Transform vague career goals into structured, trackable, and recalibrating roadmaps.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What is HERPath AI?

HERPath AI is a **stateful, multi-agent career execution system** designed to help women entering or re-entering tech transform vague goals into structured, trackable, and recalibrating roadmaps.

### It is NOT:
- ❌ A generic chatbot
- ❌ A motivational app
- ❌ A resume builder
- ❌ A job board

### It IS:
- ✅ A structured planning engine
- ✅ A constraint-aware roadmap generator
- ✅ A progress-tracking system
- ✅ A contextual AI execution coach

---

## ✨ Features

### 🎓 Smart Onboarding
- 7-step wizard to understand your goals, constraints, and background
- Emotional intelligence integration (anxiety, imposter syndrome detection)
- Adaptive pacing based on your situation

### 🗺️ Personalized Roadmaps
- AI-generated week-by-week learning plans
- Phase-based organization with clear milestones
- Resource recommendations (free and paid)

### 📊 Progress Tracking
- Real-time completion metrics
- Pace analysis and projections
- Visual progress breakdowns

### 🤖 AI Coach
- Context-aware guidance
- Multiple coaching modes:
  - Clarify Plan
  - Feeling Stuck
  - Interview Guidance

### ⚖️ Adaptive Rebalancing
- Automatic detection of when to rebalance
- Rule engine monitors missed tasks and pace
- Version history for roadmaps

---

## 🛠️ Supported Roles (V1)

1. **AI Engineer**
2. **Web Developer**
3. **Data Analyst**
4. **Career Re-entry into Tech**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Firebase project (optional for demo mode)
- OpenAI or Anthropic API key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/herpath-ai.git
cd herpath-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets

Create `.streamlit/secrets.toml`:
```toml
# LLM API Keys (choose one or both)
OPENAI_API_KEY = "sk-your-openai-key"
ANTHROPIC_API_KEY = "sk-ant-your-anthropic-key"

# Firebase Configuration (optional - demo mode works without this)
FIREBASE_WEB_API_KEY = "your-web-api-key"

[firebase_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

### 4. Run the Application
```bash
# For Python 3.14+ (recommended)
python -X utf8 -m streamlit run app.py

# Or with standard Python
streamlit run app.py
```

### 5. Open in Browser
Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
herpath-ai/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── config/
│   ├── __init__.py
│   ├── firebase_config.py # Firebase initialization
│   └── settings.py        # Application settings & constants
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Base LLM agent class
│   ├── skill_gap_agent.py # Skill analysis agent
│   ├── roadmap_agent.py   # Roadmap generation agent
│   ├── rebalance_agent.py # Roadmap rebalancing agent
│   └── coach_agent.py     # AI coaching agent
│
├── database/
│   ├── __init__.py
│   ├── firestore_client.py # Firestore operations
│   └── schema.py          # Pydantic data models
│
├── ui/
│   ├── __init__.py
│   ├── onboarding.py      # Onboarding wizard
│   ├── dashboard.py       # Main dashboard
│   ├── roadmap.py         # Roadmap view
│   ├── progress.py        # Progress analytics
│   ├── coach.py           # AI Coach chat
│   └── settings.py        # User settings
│
├── utils/
│   ├── __init__.py
│   ├── rule_engine.py     # Adaptive rebalancing rules
│   └── json_validator.py  # JSON validation utilities
│
└── .streamlit/
    └── secrets.toml       # API keys & credentials (not in git)
```

---

## 🔧 Configuration

### LLM Provider
Edit `config/settings.py` to switch between OpenAI and Anthropic:
```python
LLM_PROVIDER = "openai"  # or "anthropic"
```

### Rule Engine Thresholds
Customize rebalancing triggers in `config/settings.py`:
```python
MISSED_TASK_THRESHOLD_PERCENT = 30  # Trigger rebalance if >30% missed
```

---

## 📊 Firestore Data Model

### Collections:
- `users` - User profiles and settings
- `roadmaps` - Versioned roadmaps (Option B - history preserved)
- `tasks` - Individual task tracking
- `progress_summary` - Aggregated progress metrics
- `chat_history` - AI Coach conversation logs

---

## 🎥 Demo Flow

1. **Login/Signup** → Create account or use demo mode
2. **Onboarding** → 7-step wizard collects goals & constraints
3. **Dashboard** → View current week's focus and progress
4. **Roadmap** → Explore full learning path with milestones
5. **Progress** → Analyze completion rates and pace
6. **AI Coach** → Get contextual guidance and support
7. **Settings** → Update preferences and trigger rebalancing

---

## 🏆 Hackathon Submission

**#75HER Challenge Hackathon 2026**

- **Track:** AI/Machine Learning
- **Problem:** Women entering tech face overwhelm, inconsistent guidance, and lack structured execution
- **Solution:** Stateful multi-agent career execution engine
- **Differentiator:** Adaptive roadmap recalibration + emotional context integration + structured AI orchestration
- **Measurable Outcome:** Transforms vague ambition into structured execution roadmap in under 60 seconds

---

## 🛣️ Roadmap

### Current (V1)
- [x] Multi-step onboarding wizard
- [x] AI-powered skill gap analysis
- [x] Personalized roadmap generation
- [x] Progress tracking
- [x] AI Coach chat
- [x] Adaptive rebalancing

### Future
- [ ] OAuth authentication (Google/GitHub)
- [ ] More career tracks
- [ ] Community features
- [ ] Mobile app
- [ ] Integration with learning platforms

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- Built for the **#75HER Challenge Hackathon 2026**
- Powered by **OpenAI GPT-4** / **Anthropic Claude**
- Database: **Firebase Firestore**
- UI Framework: **Streamlit**

---

## 📞 Support

For issues or questions, please open a GitHub issue or reach out on Discord.

---

**Made with 💜 for women in tech**
