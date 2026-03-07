# HERPath AI

**AI-Powered Career Navigation for Women in Tech**

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)](https://streamlit.io)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange)](https://firebase.google.com)
[![Goose Framework](https://img.shields.io/badge/Goose-Agentic_AI-purple)](https://block.github.io/goose)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **#75HER Challenge Hackathon 2026** | Built for International Women's Day
> Transforming career uncertainty into structured, achievable roadmaps

---

## Live Demo

**[herpathai.streamlit.app](https://herpathai.streamlit.app/)**

| | |
|---|---|
| **Email** | `demo@herpath.ai` |
| **Password** | `HERPath2026!` |

Sign in to explore the full system — personalized roadmap, AI coach, progress tracking, and adaptive rebalancing — all live.

---

## The Problem

**56% of women leave tech by mid-career** — not because they lack skill, but because they lack:
- A clear, adaptive learning path tailored to their situation
- Emotional support that recognizes imposter syndrome and burnout
- Accountability systems that adapt when life gets in the way

HERPath AI solves this with agentic AI that doesn't just tell you *what* to learn — it sticks with you until you've learned it.

---

## How It Works

### 1. Empathy-First Onboarding
A 7-step wizard captures your career goal, skill level, weekly availability, financial constraints, life situation, and personal background. No judgment — just context that powers hyper-personalized recommendations.

### 2. AI-Generated Roadmap
Our Roadmap Agent (powered by Gemini 3 Flash) synthesizes a phased, week-by-week execution plan. Every task includes specific resources — exact LeetCode problem numbers, named courses with URLs, and hour estimates calibrated to your availability.

### 3. AI Coach with Emotional Intelligence
Not a chatbot. A context-aware mentor that references your roadmap, progress, and history. It detects imposter syndrome signals, breaks "stuck" moments into the smallest viable next step, and provides interview prep with actual question frameworks.

### 4. Adaptive Rebalancing
Life happens. If you miss >30% of tasks, the Rule Engine automatically restructures your timeline — extending deadlines, reprioritizing tasks, and adjusting pacing so you never feel like you've "failed" the program.

---

## Architecture

```
Frontend:     Streamlit (Python-based UI)
Backend:      Python 3.9+ / Firebase Firestore
AI:           Google Gemini 3 Flash (REST API)
Framework:    Custom Goose-style agentic system (Plan-Execute-Verify)
Database:     Firebase Firestore (NoSQL, real-time, serverless)
```

```
┌─────────────────────────────────────────────┐
│          Goose Agent Orchestrator            │
│     Plan → Execute → Verify loop            │
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

**Data Flow:**
1. **Onboarding** → User context stored in Firestore
2. **Roadmap Generation** → GooseAgent calls Gemini → 3-phase roadmap with week-by-week tasks
3. **Coach** → Multi-turn conversation with context injection (roadmap + progress + history)
4. **Rebalancing** → Rule engine monitors progress → auto-adjusts timeline if behind

---

## Project Structure

```
herpath-ai/
├── agents/                 # AI Agent implementations
│   ├── goose/              # Custom Goose framework
│   │   ├── agent.py        # GooseAgent orchestrator
│   │   ├── toolkit.py      # Tool management
│   │   ├── fallback.py     # Tiered fallback system
│   │   └── tools/          # GeminiTool, VerifyTool
│   ├── base_agent.py       # Base class with retry + fallback
│   ├── coach_agent.py      # AI Coach (4 modes)
│   ├── roadmap_agent.py    # Roadmap generator
│   ├── rebalance_agent.py  # Adaptive rebalancing
│   └── skill_gap_agent.py  # Skill analysis
├── config/                 # Configuration
│   ├── constants.py        # Centralized constants
│   ├── settings.py         # App settings
│   └── firebase_config.py  # Firebase initialization
├── database/               # Data layer
│   ├── firestore_client.py # CRUD operations + demo mode
│   └── schema.py           # Pydantic models
├── ui/                     # Streamlit UI
│   ├── onboarding.py       # 7-step wizard
│   ├── dashboard.py        # Main dashboard
│   ├── roadmap.py          # Roadmap view
│   ├── coach.py            # AI Coach chat
│   ├── progress.py         # Analytics
│   ├── resources.py        # Curated resources
│   └── settings.py         # Life events + rebalancing
├── utils/                  # Utilities
│   ├── json_validator.py   # Response validation
│   ├── rule_engine.py      # Rebalancing rules
│   ├── logging.py          # Structured logging
│   └── button_helper.py    # UI helpers
├── app.py                  # Entry point
├── seed_demo_account.py    # Demo account seeder
└── requirements.txt        # Dependencies
```

---

## Demo Evidence

### Video Walkthrough

📹 [**Watch Demo Video**](herpath-ai/scripts/demo_video.mp4) (10 MB, MP4)

Full walkthrough: account creation → 7-step onboarding → AI roadmap generation → dashboard → AI coach interactions → adaptive rebalancing.

### Screenshots

| Feature | Screenshot |
|---------|-----------|
| Landing Page | ![Landing](herpath-ai/scripts/screenshots/01_landing_page.png) |
| Onboarding Wizard | ![Onboarding](herpath-ai/scripts/screenshots/05_step1_goal.png) |
| Profile Summary | ![Profile](herpath-ai/scripts/screenshots/11_step7_profile_summary.png) |
| AI-Generated Roadmap | ![Roadmap](herpath-ai/scripts/screenshots/Roadmap.png?raw=true) |
| Dashboard | ![Dashboard](herpath-ai/scripts/screenshots/Dashboard.png?raw=true) |
| AI Coach | ![Coach](herpath-ai/scripts/screenshots/Ai%20Coach.png?raw=true) |
| Progress Tracking | ![Progress](herpath-ai/scripts/screenshots/Progress.png?raw=true) |
| Rebalancing | ![Rebalance](herpath-ai/scripts/screenshots/Rebalancing.png?raw=true) |

---

## Success Tests

| # | Test | What Happens | Status |
|---|------|-------------|--------|
| 1 | **Onboarding → Roadmap** | Complete 7-step wizard → system generates phased roadmap with role-specific tasks, exact LeetCode #s, course names, URLs | ✅ |
| 2 | **Emotional Intelligence** | Type "I feel like I don't belong" → coach detects imposter syndrome, gives specific tactical advice tied to user's progress | ✅ |
| 3 | **Adaptive Rebalancing** | Miss >30% tasks → rule engine triggers rebalance → timeline extends, tasks reprioritize | ✅ |
| 4 | **Multi-Mode Coach** | Stuck / Clarify Plan / Interview Prep / General → each mode produces context-aware, specific responses | ✅ |

---

## Architecture Decisions

| Decision | Chosen | Why |
|----------|--------|-----|
| **AI Framework** | Custom Goose implementation | `goose-ai` has Python compatibility issues; custom gives full control + zero dependency conflicts |
| **LLM** | Gemini 3 Flash | Free tier, 200-300ms response times, multimodal-ready |
| **Frontend** | Streamlit | Full app in 2 days vs. 4+ with React; 1-click deployment |
| **Database** | Firebase Firestore | Zero setup, serverless, real-time sync, free tier sufficient |
| **Rebalancing** | Rule-based (not ML) | Transparent logic judges can inspect; no training data needed |

---

## Reliability

| Feature | Implementation |
|---------|---------------|
| **API Fallback** | Tiered: Cached → Template → Generic → Minimal (never crashes) |
| **Retry Logic** | Exponential backoff (1s, 2s, 4s) on transient errors |
| **Timeout** | 30s on all API calls, 45s on agent orchestration |
| **Validation** | JSON parsing + Pydantic schema validation on all responses |
| **Demo Mode** | In-memory fallback if Firebase unavailable |
| **Logging** | Structured logging with DEBUG/INFO/ERROR levels |

---

## Setup (Local Development)

```bash
# Clone
git clone https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026.git
cd -75HER-Challenge-Hackathon-2026/herpath-ai

# Virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# Install
pip install -r requirements.txt

# Configure secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit with your Gemini API key + Firebase credentials

# Seed demo account (optional)
python seed_demo_account.py

# Run
streamlit run app.py
```

---

## Supported Career Paths

| Role | Status | Timeline |
|------|--------|----------|
| AI/ML Engineer | Full | 26-52 weeks |
| Data Analyst | Full | 20-39 weeks |
| Web Developer | Full | 20-39 weeks |
| Mobile Developer | Beta | 26-52 weeks |
| DevOps Engineer | Beta | 26-39 weeks |
| Cloud Engineer | Beta | 20-39 weeks |

---

## Documentation

- [Agent Architecture](herpath-ai/docs/AGENTS.md) — Multi-agent system design
- [Goose Framework](herpath-ai/docs/GOOSE.md) — Custom agentic AI implementation
- [API Reference](herpath-ai/docs/API.md) — Endpoints and data models
- [Deployment Guide](herpath-ai/docs/DEPLOYMENT.md) — Production deployment
- [AI Trace Log](herpath-ai/docs/AI_TRACE_LOG.md) — AI decision-making log (required for AI/ML track)

---

## Team

**Pranjal Jha** — [@pranjal2004838](https://github.com/pranjal2004838)

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**Built with 💜 for women breaking barriers in tech**

</div>
