# 📸 Evidence Screenshot Guide

This guide walks you through capturing the 3 critical evidence screenshots for judges. Total time: ~10 minutes.

---

## 📋 Prerequisites

- HERPath AI live demo: https://herpathai.streamlit.app/
- Demo account: `judge@herpath-demo.ai` / `HERPathDemo2026`
- Screenshot tool (Windows: Snip & Sketch, Mac: Command+Shift+4, Linux: `gnome-screenshot`)

---

## ✅ Screenshot 1: Onboarding → Personalized Roadmap

**Goal**: Prove the system generates role-specific roadmaps with exact learning resources.

### Steps:

1. Open https://herpathai.streamlit.app/
2. If logged in, log out (click "Sign Out" in settings)
3. Sign in with **new credentials** (or use `judge@herpath-demo.ai` if fresh)
4. Start the 7-step onboarding:
   - **Step 1**: Select goal: "AI Engineer"
   - **Step 2**: Current level: "Beginner"
   - **Step 3**: Weekly hours: "15"
   - **Step 4**: Timeline: "6 months"
   - **Step 5**: Financial: "Mixed (free preferred)"
   - **Step 6**: Situation: "Career Break"
   - **Step 7**: Background: "I have 5 years as a product manager. Left tech for 2 years due to family. Want to re-enter as AI Engineer."
5. Click "Generate Roadmap"
6. System displays the roadmap. **Take screenshot of:**
   - Phase name (e.g., "Phase 1: Python & ML Fundamentals")
   - Week-by-week breakdown (Week 1, Week 2, etc.)
   - Tasks showing **specific resources** (LeetCode #s, course names, URLs)
   - Milestone and success metrics
   - **Ensure visible:** At least 2-3 LeetCode problem numbers (e.g., "#1 Two Sum", "#15 3Sum")

### Capture with:
```bash
# Windows
# Press Windows + Shift + S, drag to select, save to docs/evidence/01_onboarding_to_roadmap.png

# Mac
# Command + Shift + 4, then drag, saves to Desktop

# Linux
gnome-screenshot -a  # Click and drag to select area
```

---

## ✅ Screenshot 2: Coach Detects Imposter Syndrome

**Goal**: Show emotional intelligence—system detects anxiety from user text and responds empathetically.

### Steps:

1. In the same session (or log out and back in)
2. Go to **Coach** tab (left sidebar)
3. Select mode: **"Feeling Stuck"**
4. In the message box, type one of these:
   ```
   I always felt like I didn't belong in tech. I see people on Twitter building amazing things and I feel like a fraud. 
   How do I get over this imposter syndrome?
   ```
   
   **OR:**
   ```
   I'm having a career break and now I'm afraid to come back. What if I'm not good enough anymore?
   ```

5. Click "Send Message" (or press Enter)
6. Coach responds. **Take screenshot of:**
   - User's message (showing emotional keywords)
   - Coach's **full response** showing:
     - Explicit acknowledgment: "I notice you're experiencing..."
     - Specific advice: "Let's start with a Quick Win Week..."
     - Affirmations: "You belong here..."
     - Next steps: "Your next action..."
   - **Ensure visible:** Response should be personalized, not generic (references their career break, their feelings)

### Capture with:
```bash
# Scroll down in the chat to see full response, then screenshot the coach's message
```

---

## ✅ Screenshot 3: Adaptive Rebalancing Trigger

**Goal**: Show rule-based intelligence—system detects when user is falling behind and suggests adjustments.

### Steps:

1. Log in with demo account: `judge@herpath-demo.ai` / `HERPathDemo2026`
2. Go to **Dashboard** tab → scroll down to "Your Progress"
3. Find the task list showing Week 1-4 tasks
4. **Mark tasks as "Missed":**
   - Click on a task
   - Toggle status from "Pending" → "Missed"
   - Repeat for **15 tasks** (to trigger >30% miss rate)
   - Note: Demo account should have ~20-40 tasks, so marking 15-20 will trigger the rule
5. After marking, go to **Rebalance** tab (should appear in sidebar as red alert, or go to Settings → Rebalance)
6. System shows rebalance recommendation. **Take screenshot of:**
   - Rebalance alert: "You've missed X% of tasks"
   - Recommendation message: "Let's adjust your roadmap"
   - **Before/After comparison:**
     - Original timeline: "20 weeks"
     - New timeline: "28 weeks" (extended)
   - Suggested actions list (at least 2 visible)

### Capture with:
```bash
# Screenshot the entire "Rebalance Recommendation" card showing the alert and adjustments
```

---

## 📝 After Capturing: Upload & Commit

```bash
# 1. Save screenshots to the correct folder
# docs/evidence/01_onboarding_to_roadmap.png
# docs/evidence/02_coach_emotional_detection.png
# docs/evidence/03_rebalance_trigger.png

# 2. Commit the evidence
cd herpath-ai
git add docs/evidence/*.png
git commit -m "evidence: Add 3 screenshot proofs (onboarding, emotional detection, rebalance)"
git push origin main
```

---

## ✅ Verification Checklist

Before pushing, verify each screenshot:

- [ ] **Screenshot 1**: Shows personalized roadmap with LeetCode problem numbers
- [ ] **Screenshot 2**: Shows coach response personalizing to user's emotional language
- [ ] **Screenshot 3**: Shows rebalance rule trigger with before/after timeline

---

## 🎯 Why Judges Care About These

| Screenshot | Judge Criterion | Why It Matters |
|-----------|-----------------|----------------|
| **1. Onboarding → Roadmap** | Clarity + Usability | Proves system delivers on core promise (personalized roadmaps) |
| **2. Emotional Detection** | Rigor + Impact | Shows domain understanding (women's unique challenges) |
| **3. Rebalancing** | Proof + Rigor | Demonstrates adaptive logic (not just a wrapper) |

---

## 💡 Pro Tips

1. **Timing**: Take screenshots during daytime (better lighting for live demo)
2. **Clarity**: Make browser window full-screen for clean screenshots
3. **Text readability**: Zoom in to 125% if text is small
4. **Multiple attempts**: If first attempt doesn't show enough detail, re-run and try again
5. **README link**: After adding images, the README will automatically display them to judges

---

## 🚀 Quick Command Checklist

```bash
# Navigate to project
cd c:\Users\anurag\Desktop\-75HER-Challenge-Hackathon-2026\herpath-ai

# After saving screenshots
git add docs/evidence/
git commit -m "evidence: Add 3 screenshot proofs (onboarding, emotional detection, rebalance)"
git push origin main

# Verify on GitHub
# Go to: https://github.com/pranjal2004838/-75HER-Challenge-Hackathon-2026
# Check: docs/evidence/ folder shows all 3 PNGs
# Check: README.md displays images correctly
```

---

**Estimated time to complete: 8-10 minutes**

Need help? Run the steps once, then take high-quality screenshots. 📸
