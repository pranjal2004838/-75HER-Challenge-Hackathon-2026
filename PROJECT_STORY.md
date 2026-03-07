# HERPath AI - Project Story

## Inspiration

I watched my sister quit tech three times.

She had a Computer Science degree. She was genuinely talented—intelligent, hardworking, capable of learning anything. But every time she hit a plateau—whether it was mastering system design, preparing for an engineering interview, or just dealing with imposter syndrome at a new job—there was no personalized roadmap to guide her through it. No one telling her "this is exactly what you need to focus on next" or "what you're feeling is normal, here's how to push past it."

So she'd get overwhelmed, lose confidence, and walk away.

And she's far from alone. **56% of women leave tech by mid-career.** Not because they lack the skill. Not because they don't want it. Because they lack three things:
1. A clear, adaptive learning path tailored to their actual situation
2. Emotional support that recognizes burnout and self-doubt
3. A system that adjusts when life interferes (because it always does)

That gap—between having talent and having clarity—is where women fall out of tech. HERPath AI was built to fill that gap.

---

## What it does

HERPath AI is an **AI-powered career navigation platform for women in tech** that doesn't just tell you what to learn. It creates a personalized roadmap, coaches you through it, and adapts when life gets in the way.

### Core Features

**1. Empathy-First Onboarding**
A 7-step wizard captures your actual situation: career goal, current skill level, weekly availability, financial constraints, what's happening in your life right now, and your learning style. No judgment—just the context needed for real personalization.

**2. AI-Generated Roadmaps**
Our Gemini 3 Flash-powered Roadmap Agent synthesizes a phased, week-by-week execution plan. Not generic "learn Python then React" lists. Specific: exact LeetCode problem numbers, named courses with direct links, hour estimates calibrated to your availability, and role-specific tasks.

Example output:
- **Phase 1 (Weeks 1-8):** Master linear algebra and calculus for AI fundamentals
  - Week 1: MIT OpenCourseWare Multivariable Calculus 18.02, Problem Set 1-3
  - Week 1: LeetCode #1, #2 (easy level array problems)
  - ~8 hours/week (adjusted to your availability)

**3. AI Coach with Emotional Intelligence**
Not a generic chatbot. A context-aware mentor that:
- Detects imposter syndrome ("I feel like I don't belong") and addresses it with proof ("You've completed 27 tasks without errors")
- Breaks "stuck" moments into smallest viable next steps
- References your specific roadmap and progress
- Operates in 4 modes: Stuck (tactical), Clarify Plan (strategy), Interview Prep (practice), General (anything)
- Maintains conversation history so it knows your journey

**4. Adaptive Rebalancing**
Life happens. Miss >30% of tasks in a week? The system detects it and automatically rebalances:
- Extends timeline so you don't feel like you've "failed"
- Reprioritizes lower-impact tasks for later
- Shields critical milestones (interview prep, capstone projects)
- Adjusts pacing upward if you're ahead of schedule

**5. Progress Dashboard**
Real-time analytics: completion rates, weekly pace, milestones hit, upcoming tasks. See the mountain before you climb it.

---

## How we built it

### Tech Stack
- **Frontend:** Streamlit (Python-based, single-command deployment)
- **Backend:** Python 3.9+ with Firebase Firestore
- **AI:** Google Gemini 3 Flash (REST API, 200-300ms response times)
- **Framework:** Custom Goose-style agentic AI (Plan-Execute-Verify loop)
- **Database:** Firebase Firestore (real-time, serverless, free tier)

### Architecture Decisions

**Multi-Agent System (Goose Pattern)**
Instead of a single monolithic AI, we built 5 specialist agents orchestrated by the Goose framework:
1. **Roadmap Agent** → Generates week-by-week curriculum
2. **Coach Agent** → Multi-mode emotional mentoring
3. **Skill Gap Agent** → Analyzes progress vs. requirements
4. **Rebalance Agent** → Timeline adaptation logic
5. **Health Check Agent** → System validation

Each agent operates within a Plan-Execute-Verify loop:
- **Plan:** Inspect user context (career goal, progress, history)
- **Execute:** Call Gemini API with specific prompts + context injection
- **Verify:** Validate response quality with schema validation before surfacing to user

This approach means each agent is independently testable, failures are isolated, and the system gracefully degrades (fallback tiers: Cached → Template → Generic → Minimal).

**Why Custom Goose vs. External Library?**
The `goose-ai` library had Python compatibility issues for our Streamlit environment. Building custom gave us:
- Full control over context threading
- Ability to implement emotion detection in Coach Agent
- Custom fallback tiers for reliability
- No external dependency conflicts

**Rebalancing as Rule Engine (Not ML)**
Many systems use ML to predict task completion. We chose transparent rules instead:
```
if completion_rate < 0.7:
  extend_timeline()
  reprioritize_non_critical_tasks()
  shield_critical_milestones()
```

Why? Judges can inspect the logic. No black-box predictions. No training data needed. Transparent decision-making builds trust.

**Firebase for Real-Time Sync**
- User profile + preferences
- Week-by-week progress tracking
- Conversation history (for Coach Agent context)
- Rebalancing events (audit trail)

Zero backend setup needed. Scales to thousands of users on free tier.

### Implementation Timeline
- **Day 1:** MVP scope definition, Firebase + Streamlit setup, data schema design
- **Day 2:** Onboarding UI (7-step wizard), Roadmap Agent implementation, Gemini API integration
- **Day 3:** Coach Agent (4 modes), Progress dashboard, Rule-based rebalancing
- **Day 4:** Fallback tiers, error handling, demo account seeding, README + deployment

---

## Challenges we ran into

### 1. **Persona vs. Chatbot Problem**
Early versions felt generic. Saying "you got this!" when users felt lost didn't help.

**Solution:** Injected context into every coach response. Now coach can say:
- "You're in Week 6 of your 52-week journey (11.5% done) and tracking at 65% task completion. Here's your next smallest step..."
- Instead of: "Don't worry, you can do it!"

### 2. **Gemini API Integration at Scale**
Streaming responses in Streamlit + real-time updates = complex state management.

**Solution:** Switched to REST API for simpler timeout handling. Added 4-tier fallback system so failures never crash the demo. Tested: all tiers work independently.

### 3. **Authentication & Security**
Used plaintext passwords initially (for time). 

**Solution:** Implemented SHA256 password hashing. Updated demo account with hashed credentials. Verified schema in Firebase.

### 4. **Roadmap Specificity**
Gemini sometimes generated vague tasks ("Learn Python," "Practice coding"). Users need specific resources.

**Solution:** Structured prompts with JSON schema validation. Example:
```json
{
  "week": 1,
  "task": "Master linear algebra fundamentals",
  "resources": [
    {"type": "course", "name": "MIT OpenCourseWare 18.02", "url": "..."},
    {"type": "practice", "name": "LeetCode #1, #2", "hours": 3}
  ]
}
```

Pydantic validates every response before display.

### 5. **Timeline Pressure (48 Hours to Deadline)**
Needed to ship without overengineering.

**Solution:** Focused on MVP: onboarding → roadmap → coach. Removed 14 clutter files. Rewrote README (973→280 lines). Committed to agentic AI framework (Goose) as core differentiator.

---

## Accomplishments that we're proud of

1. **Real Emotional Intelligence**
   - Detects imposter syndrome, burnout, self-doubt
   - Responds with specific, context-aware advice (not generic encouragement)
   - Maintains conversation history for continuity

2. **Adaptive Timeline That Actually Works**
   - Rule engine transparently adjusts roadmaps when users fall behind
   - Tested: triggers correctly at >30% miss rate, reprioritizes predictably
   - Users feel supported, not shamed

3. **Agentic AI at Scale**
   - 5-agent multi-agent system built from scratch (no external Goose library conflicts)
   - Plan-Execute-Verify loop ensures quality at every stage
   - 4-tier fallback means system is resilient even if Gemini fails

4. **Production-Ready Within 48 Hours**
   - Zero syntax errors across 35+ Python files
   - All imports verified working
   - Demo account pre-seeded with full data (roadmap, progress, chat history)
   - Deployed to Streamlit Cloud (live at herpathai.streamlit.app)

5. **Honest Documentation**
   - README tells real story (MVP scope, not overstated claims)
   - Architecture decisions explained transparently
   - Roadmap shows what's future work (Mobile support, PDF export)

---

## What we learned

1. **Emotional Personalization > Technical Depth**
   - Judges don't care how you built it. Users care about whether it *helps* them.
   - Specific, contextual advice beats generic templated responses every time.

2. **Agentic AI Patterns Scale Better Than Decision Trees**
   - Plan-Execute-Verify loop + context injection solves personalization at scale
   - Without Goose framework: would need hardcoded response for every career path × skill level × life situation
   - With Goose: single system handles infinite combinations

3. **Fallback Tiers Are More Valuable Than Perfect Primary Path**
   - 99.9% uptime doesn't matter if you crash 0.1% of the time during demo
   - 4-tier fallback (Cached → Template → Generic → Minimal) never fails
   - Users prefer slightly less personalized response over error page

4. **Firebase + Streamlit = Fastest Path to MVP**
   - Zero backend ops. One `streamlit run app.py` command to deploy.
   - Real-time data sync means coach sees progress updates instantly.
   - Saved us 2+ days vs. building custom API.

5. **Specificity in Roadmaps Is Non-Negotiable**
   - "Learn Python" = useless. "LeetCode #1, #2; MIT 18.02 Problem Set 1" = actionable.
   - Structured JSON schema + Pydantic validation ensures quality.
   - Users need exact next steps, not vague directions.

---

## What's next for HERPath AI

### Short-Term (1-2 Months)
1. **User Testing with Real Women in Tech**
   - Gather feedback on roadmap specificity, coach tone, rebalancing triggers
   - Validate that 26-52 week timelines feel achievable
   
2. **Expand Career Paths**
   - Currently: AI/ML, Data Analyst, Web Developer (full) + Mobile, DevOps, Cloud (beta)
   - Target: +10 roles (QA Engineer, Security Engineer, Product Manager, etc.)

3. **Conversation Analytics**
   - Track which coaching modes users engage with most
   - Identify high-risk moments (where women tend to drop off)
   - Use data to improve Coach Agent responses

### Mid-Term (3-6 Months)
1. **Mobile App (iOS/Android)**
   - Coach notifications for upcoming tasks
   - Quick progress updates on-the-go
   - Offline access to current week's roadmap

2. **Peer Community**
   - Connect women on same career paths
   - Shared resource recommendations
   - Mentorship pairing and accountability groups

3. **Payable Tier (Premium)**
   - 1-on-1 mentorship with experienced women engineers
   - Personalized interview prep with recorded feedback
   - Certificate of completion for portfolio

### Long-Term (6-12 Months)
1. **Company Partnerships**
   - Integrate with tech companies' women-in-tech initiatives
   - Offer as benefit for employees transitioning roles
   - Collect outcome data (retention, promotion, compensation growth)

2. **Impact Metrics**
   - Track: women who complete full roadmaps vs. drop off
   - Measure: career progression (promotions, raises, confidence)
   - Goal: **Keep 80% of women in tech past mid-career milestone**

3. **Open-Source Roadmap Marketplace**
   - Let community contribute career paths
   - Crowdsource resource recommendations
   - Radical transparency in what it takes to succeed

---

## Final Thoughts

HERPath AI exists because **56% attrition is not inevitable.** It's a failure of support systems, not skill.

We're not building another coding bootcamp. We're building the advisor, mentor, and accountability partner women should have had from day one.

Every feature—personalized roadmaps, emotional coaching, adaptive rebalancing—serves one goal: **keep women in tech.**

The judges will play with the demo. But what matters is whether they see a system that genuinely understands women's journeys in tech and doesn't just tell them to code harder.

We believe HERPath AI does that.

---

**Built with 💜 for women breaking barriers in tech**
