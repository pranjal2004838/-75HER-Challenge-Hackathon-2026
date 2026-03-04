# 📹 Evidence Recording & Screenshot Guide

## Quick 5-Minute Manual Process

### What You Need
- **Windows Screen Recorder** (built-in) OR **OBS Studio** (free)
- **Snip & Sketch** (Windows + Shift + S) for screenshots
- **Demo credentials:**
  - Email: `judge@herpath-demo.ai`
  - Password: `HERPathDemo2026`

---

## Step 1: Start Recording (1 minute)

### Using Windows Screen Recorder
```
1. Press Windows + Alt + R
2. Click "Start" to begin recording
3. Continue with steps below
```

### Using OBS Studio (Professional)
```
1. Open OBS Studio
2. Add "Display Capture" or "Window Capture" source
3. Click "Start Recording"
4. Continue with steps below
```

---

## Step 2: Navigate Demo (3 minutes)

### Login (slow, deliberate)
```
1. Open: https://herpathai.streamlit.app/
2. Email: judge@herpath-demo.ai  [pause 2 seconds]
3. Password: HERPathDemo2026       [pause 2 seconds]
4. Click Login                     [pause 3 seconds for load]
```

### Roadmap (30 seconds)
```
1. Click "Roadmap" tab
2. Scroll down slowly (viewers should see LeetCode #s)
3. Show at least 2 weeks of tasks with specific resources
```

### Coach (30 seconds)
```
1. Click "Coach" tab
2. Type: "I always felt like I didn't belong in tech"
3. Let coach respond (wait 10 seconds)
4. Show personalized response
```

### Progress (30 seconds)
```
1. Click "Progress" tab
2. Show completion %, missed tasks, pace status
3. Scroll to rebalance section
```

### Logout (20 seconds)
```
1. Find "Sign Out" button
2. Click and show login page again
```

---

## Step 3: Stop Recording (30 seconds)

### Windows Screen Recorder
```
1. Press Windows + Alt + R
2. Click "Stop"
3. Video saves to: Videos/Captures/
```

### OBS Studio
```
1. Click "Stop Recording"
2. Video saves to: [Your configured output folder]
```

---

## Step 4: Save Video to Repo

Move recording to: `docs/evidence/herpath_ai_demo.webm` (or .mp4)

```bash
# Example (adjust path to your recording)
cp "~/Videos/Captures/HERPath AI...mp4" docs/evidence/herpath_ai_demo.webm
```

---

## Step 5: Capture Key Screenshots

**Using Snip & Sketch (Windows + Shift + S):**

During or after recording, take screenshots of:

1. **Dashboard** → `docs/evidence/screenshots/01_dashboard.png`
2. **Roadmap Detail** → `docs/evidence/screenshots/02_roadmap_detail.png`
3. **Coach Response** → `docs/evidence/screenshots/03b_coach_response.png`
4. **Progress** → `docs/evidence/screenshots/04_progress_tracking.png`

---

## Step 6: Commit & Update README

```bash
cd herpath-ai

# Add all evidence
git add docs/evidence/

# Commit
git commit -m "evidence: Add demo video and screenshot evidence"

# Push
git push origin main
```

---

## ✅ Done!

Estimated total time: **5-8 minutes**

Now judges can:
- ▶️ Watch your 3-minute demo video
- 📸 See screenshots of key features
- ✅ Verify all claims in the README
