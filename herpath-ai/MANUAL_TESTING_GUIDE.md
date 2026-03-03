# DEPLOYMENT READINESS - MANUAL TESTING GUIDE

## 🎯 CRITICAL VERIFICATION CHECKLIST

This guide ensures all AI functionality and Firebase integration works correctly before deployment.

---

## TEST 1: Firebase & Authentication (5 mins)

### Goal: Verify user data is being persisted to Firestore

1. **Open the app in a browser**: http://localhost:8501
2. **Sign Up with a NEW account**:
   - Email: `testuser@herpath.ai`
   - Password: `test123`
   - Name: Your name
3. **Check Firebase Console**:
   - Go to: https://console.firebase.google.com/
   - Project: `her-challenge-hackathon`
   - Navigate to: **Firestore Database**
   - Look for collection: `users`
   - **VERIFY**: You should see a new document with your test email

✅ **PASS**: User document exists in Firestore  
❌ **FAIL**: No user document (app is in demo mode - check logs)

---

## TEST 2: Onboarding AI - Role Specificity (10 mins)

### Goal: Verify AI generates role-specific responses (not generic web dev for AI engineer)

### Test Case A: AI Engineer

1. Complete onboarding with:
   - **Role**: AI Engineer
   - **Level**: Intermediate
   - **Hours/Week**: 15
   - **Timeline**: 3-4 months
   - **Budget**: Paid Allowed
   - **Situation**: Working Professional
   - **Background**: "I'm a software developer with 3 years of experience. I know Python and basic web development. I want to transition to AI engineering, specifically machine learning and deep learning. My biggest fear is that my math skills aren't strong enough."

2. **Wait for roadmap generation** (30-60 seconds)

3. **Verify Roadmap Specificity**:
   - ✅ Week 1 should mention **AI-specific** topics like:
     - "Neural Networks", "Machine Learning", "NumPy/Pandas", "TensorFlow/PyTorch"
   - ✅ Tasks should be **SPECIFIC**, not vague:
     - GOOD: "Complete Section 3 of Andrew Ng's Machine Learning course - Linear Regression"
     - GOOD: "LeetCode #53 Maximum Subarray (dynamic programming), #121 Best Time to Buy Stock (greedy)"
     - BAD: "Learn Python basics" (too vague)
     - BAD: "Practice coding problems" (no specificity)
   - ❌ Should **NOT** mention:
     - "React", "Vue", "HTML/CSS", "DOM manipulation", "frontend frameworks"

### Test Case B: Web Developer (for comparison)

1. **Reset**: Clear browser data or use incognito window
2. Sign up with different email: `webdev@herpath.ai`
3. Complete onboarding with:
   - **Role**: Web Developer
   - **Background**: "Complete beginner to coding. Want to build websites."

4. **Verify Different Roadmap**:
   - ✅ Week 1 should mention: "HTML", "CSS", "JavaScript", "DOM"
   - ❌ Should **NOT** focus on: "TensorFlow", "Neural Networks", "ML algorithms"

✅ **PASS**: AI Engineer roadmap is distinct from Web Developer roadmap  
❌ **FAIL**: Both roadmaps are similar or mention wrong technologies

---

## TEST 3: AI Coach - Context Awareness (15 mins)

### Goal: Verify coach knows user's current state and adapts to changes

### Part 1: Initial Context

1. After onboarding, go to **Coach tab**
2. Ask: *"What should I focus on this week?"*
3. **Verify Response Includes**:
   - ✅ Your name or "you"
   - ✅ Reference to Week 1 or current week
   - ✅ Specific mention of your goal (AI Engineer / Web Developer)
   -  Specific actionable steps (not generic advice)

### Part 2: Context Adaptation

1. Ask: *"I'm struggling with understanding backpropagation"*
2. **Verify Response**:
   - ✅ Acknowledges backpropagation is part of neural networks (AI-specific)
   - ✅ Gives SPECIFIC resources or techniques
   - ❌ Does NOT give generic "just practice more" advice

### Part 3: Real-Time Adaptation (CRITICAL TEST)

1. Go to **Rebalance tab**
2. Change your settings:
   - **Increase hours/week** from 15 to 20
   - OR **Change timeline** from "3-4 months" to "5-6 months"
   - Click "Rebalance Roadmap"
3. Wait for new roadmap (30-60 seconds)
4. **Return to Coach tab**
5. Ask a NEW question: *"Now that I have more time, should I go deeper into math fundamentals?"*
6. **Verify Response Adapts**:
   - ✅ Mentions the new timeline or extra hours
   - ✅ Suggests deeper dive topics (since more time available)
   - ✅ References updated roadmap structure

✅ **PASS**: Coach adapts to rebalanced plan immediately  
❌ **FAIL**: Coach still references old timeline/schedule

---

## TEST 4: Firebase Persistence (5 mins)

### Goal: Verify data survives page refresh

1. After completing onboarding, note:
   - Your current week number
   - 1-2 task titles from your roadmap
2. **Refresh the page** (F5 or Ctrl+R)
3. **Re-login** if needed
4. **Verify**:
   - ✅ Roadmap is still there (same week, same tasks)
   - ✅ Progress is maintained
   - ✅ Chat history persists (go to Coach tab)

✅ **PASS**: All state preserved after refresh  
❌ **FAIL**: Data lost (app is in demo mode - SESSION STATE only)

---

## TEST 5: Roadmap Specificity Spot Check (5 mins)

### Goal: Ensure NO vague tasks anywhere in roadmap

1. Open your roadmap (Dashboard tab)
2. **Scan through Weeks 1-4**
3. Look for **VAGUE tasks** like:
   - "Learn Python" (too broad)
   - "Practice coding" (no specificity)
   - "Study data structures" (which ones?)
   - "Solve array problems" (which specific problems?)
4. **Check for SPECIFIC tasks** like:
   - "LeetCode #1 Two Sum, #15 3Sum, #11 Container (two-pointer pattern)"
   - "Complete Chapter 3 'Neural Networks Basics' in Deep Learning Specialization by Andrew Ng"
   - "Build REST API: User CRUD, JWT auth, PostgreSQL, deploy to Railway.app"

✅ **PASS**: At least 80% of tasks are specific (mention problem numbers, course names, chapters)  
❌ **FAIL**: Most tasks are vague ("learn X", "study Y")

---

## TEST 6: AI Role Confusion (CRITICAL) (5 mins)

### Goal: VERIFY AI Engineer roadmap does NOT mention web development

1. Open your AI Engineer roadmap (from Test 2A)
2. **Search entire roadmap** (Ctrl+F) for these keywords:
   - "React"
   - "HTML"
   - "CSS"
   - "DOM"
   - "frontend"
   - "Vue"
   - "Angular"
3. **Count mentions**:
   - These should appear: **0-2 times MAXIMUM**
   - (Okay if mentioned in passing for portfolio website, but NOT as core skills)

4. **Search for AI keywords**:
   - "machine learning" / "ML"
   - "deep learning"
   - "neural network"
   - "TensorFlow" / "PyTorch"
   - "NLP" / "Computer Vision"
5. **Count mentions**:
   - These should appear: **10+ times**

✅ **PASS**: AI keywords dominate, webdev keywords minimal  
❌ **FAIL**: Web development is heavily featured in AI Engineer roadmap

---

## FINAL VERIFICATION

### All Tests Must Pass for Deployment Readiness

- [ ] Firebase persistence working
- [ ] AI Engineer roadmap is role-specific (not web dev content)
- [ ] Roadmap tasks are SPECIFIC (not vague)
- [ ] Coach is context-aware
- [ ] Coach adapts to rebalancing in real-time
- [ ] Data survives page refresh

---

## 🚨 KNOWN ISSUES TO FIX IF TESTS FAIL

### If Firebase Tests Fail:
- Check Firebase Console: Project should have Firestore enabled
- Check browser console (F12) for errors
- Verify    secrets.toml` has correct Firebase credentials

### If AI Tests Fail (returns vague/wrong role):
- Check logs for Gemini API errors
- Verify Gemini API key is valid: `AIzaSyAeAMeFcUlFtKAdOv8Zv1x9qtkFAMKDzrg`
- Check `agents/base_agent.py` model is `gemini-2.5-flash`

### If Coach Doesn't Adapt:
- Verify `ui/coach.py` passes `user_state`, `roadmap_state`, `progress_state`
- Check if new roadmap is being marked as `is_active=True` in Firestore

---

## ✅ IF ALL TESTS PASS → APP IS DEPLOYMENT READY

Proceed with deployment to:
- Streamlit Cloud
- Railway
- Heroku
- Or your preferred hosting platform

---

## 📝 TEST RESULTS LOG

**Date**: ___________  
**Tester**: ___________

| Test | Status | Notes |
|------|--------|-------|
| Firebase & Auth | ⬜ Pass / ⬜ Fail | |
| Onboarding AI (AI Engineer) | ⬜ Pass / ⬜ Fail | |
| Onboarding AI (Web Dev) | ⬜ Pass / ⬜ Fail | |
| Coach Context Awareness | ⬜ Pass / ⬜ Fail | |
| Real-Time Adaptation | ⬜ Pass / ⬜ Fail | |
| Firebase Persistence | ⬜ Pass / ⬜ Fail | |
| Roadmap Specificity | ⬜ Pass / ⬜ Fail | |
| Role Confusion Check | ⬜ Pass / ⬜ Fail | |

**Overall**: ⬜ READY / ⬜ NOT READY
