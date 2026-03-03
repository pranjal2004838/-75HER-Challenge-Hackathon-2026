"""
Onboarding wizard UI component.
Multi-step form for collecting user information and generating initial roadmap.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional

from config.settings import (
    SUPPORTED_ROLES,
    SKILL_LEVELS,
    TIMELINE_OPTIONS,
    FINANCIAL_OPTIONS,
    SITUATION_OPTIONS
)


def render_onboarding(db_client, on_complete: callable):
    """
    Render the multi-step onboarding wizard.
    
    Args:
        db_client: FirestoreClient instance
        on_complete: Callback function when onboarding completes
    """
    st.title("🚀 Welcome to HERPath AI")
    st.markdown("### Let's create your personalized career roadmap")
    st.markdown("---")
    
    # Initialize session state for wizard
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    
    if 'onboarding_data' not in st.session_state:
        st.session_state.onboarding_data = {}
    
    # Progress indicator
    total_steps = 7
    current_step = st.session_state.onboarding_step
    st.progress(current_step / total_steps)
    st.caption(f"Step {current_step} of {total_steps}")
    
    # Render current step
    if current_step == 1:
        _render_step_goal()
    elif current_step == 2:
        _render_step_level()
    elif current_step == 3:
        _render_step_hours()
    elif current_step == 4:
        _render_step_timeline()
    elif current_step == 5:
        _render_step_financial()
    elif current_step == 6:
        _render_step_situation()
    elif current_step == 7:
        _render_step_background(db_client, on_complete)


def _render_step_goal():
    """Step 1: Select career goal."""
    st.subheader("What's your career goal?")
    st.markdown("Choose the role you want to transition into:")
    
    goal = st.selectbox(
        "Select your target role",
        options=SUPPORTED_ROLES,
        index=None,
        placeholder="Choose a role..."
    )
    
    if goal:
        st.session_state.onboarding_data['goal'] = goal
        
        # Show role description
        descriptions = {
            "AI Engineer": "Build and deploy machine learning models and AI systems.",
            "Web Developer": "Create modern, responsive web applications.",
            "Data Analyst": "Transform data into actionable insights.",
            "Career Re-entry into Tech": "Get back into tech after a career break."
        }
        st.info(descriptions.get(goal, ""))
    
    col1, col2 = st.columns(2)
    with col2:
        if st.button("Next →", disabled=not goal, use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()


def _get_level_descriptions(role: str) -> dict:
    """Return role-specific skill level descriptions so users can self-assess."""

    if role == "AI Engineer":
        return {
            "Beginner": {
                "label": "No AI/ML experience yet",
                "skills": (
                    "Choose this if you:\n"
                    "- Have little or no programming experience\n"
                    "- Haven't worked with Python, NumPy, or Pandas\n"
                    "- Don't know what machine learning or neural networks are\n"
                    "- Are starting completely from scratch"
                )
            },
            "Intermediate": {
                "label": "Comfortable with Python & basic ML",
                "skills": (
                    "Choose this if you know:\n"
                    "- **Python** (functions, loops, OOP basics)\n"
                    "- **NumPy / Pandas** for data manipulation\n"
                    "- **Scikit-learn** basics (linear regression, decision trees)\n"
                    "- Basic **statistics** (mean, median, distributions)\n"
                    "- Have trained at least one ML model"
                )
            },
            "Advanced": {
                "label": "Strong ML skills, ready to specialise",
                "skills": (
                    "Choose this if you know:\n"
                    "- **PyTorch or TensorFlow** (CNNs, RNNs, training loops)\n"
                    "- **Deep Learning** concepts (backprop, optimisers, regularisation)\n"
                    "- **NLP or Computer Vision** fundamentals\n"
                    "- **MLOps** basics (experiment tracking, model deployment)\n"
                    "- Have built and deployed ML models"
                )
            }
        }

    elif role == "Web Developer":
        return {
            "Beginner": {
                "label": "No web development experience yet",
                "skills": (
                    "Choose this if you:\n"
                    "- Have never built a website or web app\n"
                    "- Don't know HTML, CSS, or JavaScript\n"
                    "- Are not familiar with how websites work\n"
                    "- Are starting completely from scratch"
                )
            },
            "Intermediate": {
                "label": "Comfortable with HTML/CSS/JS & frontend basics",
                "skills": (
                    "Choose this if you know:\n"
                    "- **HTML & CSS** (can build responsive layouts)\n"
                    "- **JavaScript** (DOM manipulation, events, async/await)\n"
                    "- A **frontend framework** like React, Vue, or Angular (basics)\n"
                    "- **Git** for version control\n"
                    "- Have built at least one interactive website"
                )
            },
            "Advanced": {
                "label": "Strong full-stack skills, ready to level up",
                "skills": (
                    "Choose this if you know:\n"
                    "- **React / Vue / Angular** (state management, routing, hooks)\n"
                    "- **Node.js / Express** or another backend framework\n"
                    "- **Databases** (SQL or MongoDB, CRUD operations)\n"
                    "- **REST APIs** (design and consume)\n"
                    "- Have built and deployed full-stack apps"
                )
            }
        }

    elif role == "Data Analyst":
        return {
            "Beginner": {
                "label": "No data analysis experience yet",
                "skills": (
                    "Choose this if you:\n"
                    "- Have basic Excel / Google Sheets knowledge only\n"
                    "- Don't know SQL or Python\n"
                    "- Haven't worked with datasets or dashboards\n"
                    "- Are starting completely from scratch"
                )
            },
            "Intermediate": {
                "label": "Comfortable with Excel/SQL & basic data tools",
                "skills": (
                    "Choose this if you know:\n"
                    "- **Advanced Excel** (VLOOKUP, pivot tables, charts)\n"
                    "- **SQL** (SELECT, JOIN, GROUP BY, filtering)\n"
                    "- **Python basics** with Pandas for data manipulation\n"
                    "- Basic **statistics** (mean, median, standard deviation)\n"
                    "- Have analysed at least one real dataset"
                )
            },
            "Advanced": {
                "label": "Strong analytical skills, ready to specialise",
                "skills": (
                    "Choose this if you know:\n"
                    "- **Advanced SQL** (window functions, CTEs, subqueries)\n"
                    "- **Python** (Pandas, Matplotlib/Seaborn for visualisation)\n"
                    "- **Tableau or Power BI** for dashboards\n"
                    "- **A/B testing** and hypothesis testing concepts\n"
                    "- Have built reports or dashboards for stakeholders"
                )
            }
        }

    else:  # Career Re-entry into Tech
        return {
            "Beginner": {
                "label": "Starting fresh or been away from tech for a long time",
                "skills": (
                    "Choose this if you:\n"
                    "- Have been away from tech for 2+ years\n"
                    "- Need to refresh all technical skills\n"
                    "- Are exploring which direction to take\n"
                    "- Have non-tech professional experience to leverage"
                )
            },
            "Intermediate": {
                "label": "Some prior tech experience, returning after a break",
                "skills": (
                    "Choose this if you:\n"
                    "- Worked in tech before but have been away for a while\n"
                    "- Remember basics of programming or tech tools\n"
                    "- Need to update skills to current industry standards\n"
                    "- Can write basic code but need practice"
                )
            },
            "Advanced": {
                "label": "Strong prior tech background, short career break",
                "skills": (
                    "Choose this if you:\n"
                    "- Had a senior/mid-level tech role before your break\n"
                    "- Still comfortable with programming concepts\n"
                    "- Mainly need to catch up on new tools and frameworks\n"
                    "- Want to re-enter at a similar or higher level"
                )
            }
        }


def _render_step_level():
    """Step 2: Select current skill level."""
    st.subheader("What's your current skill level?")
    
    goal = st.session_state.onboarding_data.get('goal', 'this field')
    st.markdown(f"How would you rate your current skills related to **{goal}**?")

    # Role-specific skill level descriptions
    level_descriptions = _get_level_descriptions(goal)
    
    level = st.radio(
        "Select your level",
        options=SKILL_LEVELS,
        index=None,
        horizontal=True
    )
    
    if level:
        st.session_state.onboarding_data['current_level'] = level
        
        # Show role-specific level description
        desc = level_descriptions.get(level, {})
        label = desc.get("label", level)
        skills_text = desc.get("skills", "")
        
        st.caption(f"**{label}**")
        if skills_text:
            st.markdown(skills_text)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 1
            st.rerun()
    with col2:
        if st.button("Next →", disabled=not level, use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()


def _render_step_hours():
    """Step 3: Weekly availability."""
    st.subheader("How many hours can you dedicate weekly?")
    st.markdown("Be realistic - we'll build your roadmap around this.")
    
    hours = st.slider(
        "Hours per week",
        min_value=3,
        max_value=40,
        value=st.session_state.onboarding_data.get('weekly_hours', 10),
        step=1,
        help="Consider your work, family, and other commitments."
    )
    
    st.session_state.onboarding_data['weekly_hours'] = hours
    
    # Provide feedback based on hours
    if hours < 5:
        st.warning("⚠️ Less than 5 hours/week will extend your timeline significantly, but it's absolutely doable!")
    elif hours < 10:
        st.info("📊 A steady pace. Expect a longer journey but consistent progress.")
    elif hours < 20:
        st.success("✅ A solid commitment! Great for making meaningful progress.")
    else:
        st.success("🚀 Intensive pace! Make sure this is sustainable for you.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True):
            st.session_state.onboarding_step = 4
            st.rerun()


def _render_step_timeline():
    """Step 4: Target timeline."""
    st.subheader("Do you have a target timeline?")
    
    timeline_labels = list(TIMELINE_OPTIONS.keys())
    
    timeline = st.radio(
        "Select your preferred timeline",
        options=timeline_labels,
        index=None
    )
    
    if timeline:
        st.session_state.onboarding_data['deadline_type'] = timeline
        
        # Show timeline context
        hours = st.session_state.onboarding_data.get('weekly_hours', 10)
        weeks = TIMELINE_OPTIONS.get(timeline)
        
        if weeks:
            total_hours = weeks * hours
            st.info(f"📅 {weeks} weeks × {hours} hrs/week = **{total_hours} total hours**")
        else:
            st.info("📅 Flexible timeline - we'll recommend the optimal duration based on your goals.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 3
            st.rerun()
    with col2:
        if st.button("Next →", disabled=not timeline, use_container_width=True):
            st.session_state.onboarding_step = 5
            st.rerun()


def _render_step_financial():
    """Step 5: Financial constraint."""
    st.subheader("What's your budget for learning resources?")
    
    financial = st.radio(
        "Resource preference",
        options=FINANCIAL_OPTIONS,
        index=None
    )
    
    if financial:
        st.session_state.onboarding_data['financial_constraint'] = financial
        
        info = {
            "Free Only": "📚 We'll prioritize free courses, tutorials, and open-source resources.",
            "Mixed (Free preferred, paid okay)": "📚 Mostly free resources, with paid options for key skills.",
            "Paid Allowed": "📚 Best available resources, regardless of cost."
        }
        st.caption(info.get(financial, ""))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 4
            st.rerun()
    with col2:
        if st.button("Next →", disabled=not financial, use_container_width=True):
            st.session_state.onboarding_step = 6
            st.rerun()


def _render_step_situation():
    """Step 6: Current situation."""
    st.subheader("What's your current situation?")
    
    situation = st.radio(
        "Select the option that best describes you",
        options=SITUATION_OPTIONS,
        index=None
    )
    
    if situation:
        st.session_state.onboarding_data['situation'] = situation
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 5
            st.rerun()
    with col2:
        if st.button("Next →", disabled=not situation, use_container_width=True):
            st.session_state.onboarding_step = 7
            st.rerun()


def _render_step_background(db_client, on_complete: callable):
    """Step 7: Personal background and story."""
    st.subheader("Tell us about yourself")
    st.markdown("This helps us personalize your roadmap and coaching.")
    
    prompts = """
**Consider sharing:**
- What have you tried so far in your learning journey?
- Where do you feel stuck or uncertain?
- What are your biggest fears or concerns?
- What would success look like for you?
    """
    st.markdown(prompts)
    
    background = st.text_area(
        "Your story (optional but recommended)",
        height=200,
        placeholder="I've been working in marketing for 5 years and want to transition to tech. I've tried some online courses but struggled with consistency. My biggest fear is that I'm too old to start..."
    )
    
    st.session_state.onboarding_data['background_text'] = background
    
    # Summary before submit
    st.markdown("---")
    st.subheader("Your Profile Summary")
    
    data = st.session_state.onboarding_data
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Goal:** {data.get('goal', 'Not set')}")
        st.markdown(f"**Level:** {data.get('current_level', 'Not set')}")
        st.markdown(f"**Hours/Week:** {data.get('weekly_hours', 'Not set')}")
    with col2:
        st.markdown(f"**Timeline:** {data.get('deadline_type', 'Not set')}")
        st.markdown(f"**Budget:** {data.get('financial_constraint', 'Not set')}")
        st.markdown(f"**Situation:** {data.get('situation', 'Not set')}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.onboarding_step = 6
            st.rerun()
    with col2:
        if st.button("🚀 Generate My Roadmap", type="primary", use_container_width=True):
            _process_onboarding(db_client, on_complete)


def _process_onboarding(db_client, on_complete: callable):
    """Process onboarding data and generate roadmap."""
    try:
        from agents import SkillGapAgent, RoadmapAgent, get_fallback_skills, get_fallback_roadmap
        from config.settings import TIMELINE_OPTIONS
        from utils import sanitize_roadmap_output, ensure_week_continuity
    except ImportError as e:
        st.error(f"😕 A required module could not be loaded. Please ensure all dependencies are installed.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(str(e), language="text")
        return
    
    data = st.session_state.onboarding_data
    uid = st.session_state.get('uid')
    
    try:
        with st.spinner("Analyzing your skill gaps..."):
            # Run SkillGapAgent
            skill_agent = SkillGapAgent()
            skill_analysis = skill_agent.analyze(
                role=data['goal'],
                current_level=data['current_level'],
                weekly_hours=data['weekly_hours'],
                background_text=data.get('background_text', ''),
                situation=data['situation']
            )
            
            # Fallback if LLM fails
            if not skill_analysis:
                skill_analysis = get_fallback_skills(data['goal'])
            
            st.session_state.skill_analysis = skill_analysis
        
        with st.spinner("Building your personalized roadmap..."):
            # Get deadline weeks
            deadline_weeks = TIMELINE_OPTIONS.get(data['deadline_type'])
            
            # Run RoadmapAgent
            roadmap_agent = RoadmapAgent()
            roadmap = roadmap_agent.generate(
                role=data['goal'],
                missing_skills=skill_analysis.get('missing_skills', []),
                priority_order=skill_analysis.get('priority_order', []),
                deadline_weeks=deadline_weeks,
                weekly_hours=data['weekly_hours'],
                financial_constraint=data['financial_constraint'],
                situation=data['situation'],
                emotional_signals=skill_analysis.get('emotional_signals', {})
            )
            
            # Fallback if LLM fails
            if not roadmap:
                roadmap = get_fallback_roadmap(data['goal'], data['weekly_hours'], deadline_weeks)
            
            # Sanitize roadmap
            roadmap = sanitize_roadmap_output(roadmap)
            roadmap['phases'] = ensure_week_continuity(roadmap['phases'])
        
        with st.spinner("Saving your profile and roadmap..."):
            # Save user to Firestore
            user_data = {
                'uid': uid,
                'name': st.session_state.get('user_name', 'User'),
                'email': st.session_state.get('user_email', ''),
                **data,
                'onboarding_completed': True,
                'created_at': datetime.utcnow()
            }
            
            # Save roadmap data
            roadmap_data = {
                'uid': uid,
                **roadmap,
                'current_week': 1,
                'is_active': True,
                'generated_at': datetime.utcnow()
            }
            
            # Save to Firestore if available, otherwise use session state for demo mode
            if db_client:
                db_client.create_user(user_data)
                db_client.create_roadmap(roadmap_data)
                db_client.update_progress(uid)
            else:
                # Demo mode: store in session state
                st.session_state.demo_user_data = user_data
                st.session_state.demo_roadmap_data = roadmap_data
                st.session_state.demo_progress_data = {
                    'uid': uid,
                    'completion_percentage': 0,
                    'completed_tasks_count': 0,
                    'total_tasks_count': sum(len(w.get('tasks', [])) for p in roadmap.get('phases', []) for w in p.get('weeks', [])),
                    'missed_tasks_count': 0,
                    'pace_status': 'on_track',
                    'current_week': 1
                }
        
        st.success("✅ Your roadmap is ready!")
        
        # Clear onboarding state
        st.session_state.onboarding_step = 1
        st.session_state.onboarding_data = {}
        st.session_state.onboarding_completed = True
        
        # Call completion callback
        if on_complete:
            on_complete()
        
        st.rerun()
    
    except Exception as e:
        st.error("😕 We ran into an issue while generating your roadmap.")
        st.markdown("Don't worry — your inputs are saved. Please try again.")
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"{type(e).__name__}: {e}", language="text")
        
        if st.button("🔄 Retry", type="primary"):
            st.rerun()


def reset_onboarding():
    """Reset onboarding state for re-onboarding."""
    st.session_state.onboarding_step = 1
    st.session_state.onboarding_data = {}
    if 'onboarding_completed' in st.session_state:
        del st.session_state.onboarding_completed
