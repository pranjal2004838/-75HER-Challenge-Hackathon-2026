"""
Resources page UI component.
Shows curated learning resources organized by role, cost, and type.
Includes both roadmap-extracted resources and a static curated catalog.
"""

import streamlit as st
from typing import Dict, Any, List

# ============================================================================
# CURATED RESOURCE CATALOG — organized by role → category → cost
# ============================================================================

CURATED_RESOURCES = {
    "AI Engineer": {
        "DSA & Coding Interview": [
            {
                "name": "NeetCode.io — Blind 75 + NeetCode 150 (Full DSA roadmap with pattern-based video explanations)",
                "type": "Video + Practice",
                "url": "https://neetcode.io/roadmap",
                "cost": "Free",
                "why": "Best structured DSA prep. Groups problems by pattern (Two Pointer, Sliding Window, Trees, DP). Each video explains the intuition BEFORE code.",
                "level": "Beginner → Advanced",
                "time": "8–12 weeks at 10 hrs/week"
            },
            {
                "name": "LeetCode — Top Interview Questions (150 problems curated by FAANG)",
                "type": "Practice Platform",
                "url": "https://leetcode.com/studyplan/top-interview-150/",
                "cost": "Free (premium: $35/mo for company-specific questions)",
                "why": "The closest thing to actual interview questions. Filter by company and topic. Track your weak areas.",
                "level": "Intermediate",
                "time": "Self-paced"
            },
            {
                "name": "AlgoExpert — 170 problems with video solutions (Clément Mihailescu)",
                "type": "Course + Practice",
                "url": "https://www.algoexpert.io",
                "cost": "$99/year",
                "why": "Every solution comes with time/space complexity analysis and multiple approaches. Best for understanding WHY, not just HOW.",
                "level": "Intermediate → Advanced",
                "time": "10–14 weeks"
            }
        ],
        "Machine Learning Fundamentals": [
            {
                "name": "fast.ai — Practical Deep Learning for Coders (Jeremy Howard)",
                "type": "Free Course",
                "url": "https://course.fast.ai",
                "cost": "Free",
                "why": "Top-down, practice-first approach. Build real models before theory. Hugely respected in the ML community. Jupyter notebooks included.",
                "level": "Beginner → Intermediate",
                "time": "7 weeks (3–5 hrs/week)"
            },
            {
                "name": "Stanford CS229 — Machine Learning (Andrew Ng, open courseware)",
                "type": "University Course",
                "url": "https://cs229.stanford.edu/syllabus-autumn2018.html",
                "cost": "Free",
                "why": "The mathematical foundation of ML. Teaches you WHY algorithms work — essential for interviews at research-heavy companies.",
                "level": "Intermediate → Advanced",
                "time": "12 weeks"
            },
            {
                "name": "Zero to Mastery — PyTorch for Deep Learning (Daniel Bourke)",
                "type": "Paid Course",
                "url": "https://zerotomastery.io/courses/learn-pytorch/",
                "cost": "$39/mo (Zero To Mastery)",
                "why": "Step-by-step PyTorch from tensors to custom training loops. All code on GitHub, community Discord included.",
                "level": "Beginner",
                "time": "20–25 hours"
            }
        ],
        "LLMs & Generative AI": [
            {
                "name": "Andrej Karpathy's 'Neural Networks: Zero to Hero' playlist",
                "type": "YouTube Series",
                "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ",
                "cost": "Free",
                "why": "Builds a GPT from scratch in numpy. The best intuition-builder for transformers, attention mechanisms, and backprop. 8 videos, ~30 hrs total.",
                "level": "Intermediate → Advanced",
                "time": "30 hours"
            },
            {
                "name": "DeepLearning.AI — LLM Specialization (Andrew Ng + OpenAI)",
                "type": "Course",
                "url": "https://www.deeplearning.ai/courses/large-language-models-specialization/",
                "cost": "Free to audit on Coursera",
                "why": "Covers prompt engineering, fine-tuning, RLHF, and RAG. Direct from the creators of ChatGPT's training pipeline.",
                "level": "Intermediate",
                "time": "4 weeks"
            }
        ],
        "MLOps & Deployment": [
            {
                "name": "Made With ML — MLOps course (Goku Mohandas)",
                "type": "Free Course",
                "url": "https://madewithml.com",
                "cost": "Free",
                "why": "End-to-end ML system design: data pipelines, model versioning, CI/CD for ML, serving. Used by Netflix, Apple engineers as reference.",
                "level": "Intermediate",
                "time": "10–15 hours"
            },
            {
                "name": "Weights & Biases — MLOps fundamentals course",
                "type": "Free Course",
                "url": "https://www.wandb.courses/courses/mlops-fundamentals",
                "cost": "Free",
                "why": "Hands-on experiment tracking, model versioning, and deployment monitoring using industry-standard W&B tooling.",
                "level": "Beginner → Intermediate",
                "time": "5–8 hours"
            }
        ],
        "Interview Prep": [
            {
                "name": "Exponent — System Design Interview Prep (ML focus)",
                "type": "Course + Mock Interviews",
                "url": "https://www.tryexponent.com/courses/ml-engineer",
                "cost": "$12/mo",
                "why": "Real mock interviews by ex-FAANG engineers. ML system design questions: recommendation systems, search ranking, fraud detection. Video feedback included.",
                "level": "Advanced",
                "time": "4–8 weeks"
            },
            {
                "name": "Interviewing.io — Anonymous mock technical interviews (free practice)",
                "type": "Mock Interview Platform",
                "url": "https://interviewing.io",
                "cost": "Free (practice sessions)",
                "why": "Anonymous mock interviews with senior engineers. See how you rank without the anxiety of being judged. Recorded for review.",
                "level": "Intermediate → Advanced",
                "time": "Ongoing"
            }
        ],
        "Communities": [
            {
                "name": "Women in Machine Learning (WiML) — Discord & events",
                "type": "Community",
                "url": "https://wimlworkshop.org",
                "cost": "Free",
                "why": "Largest professional community for women in ML. Annual workshops co-located with NeurIPS. Mentorship program.",
                "level": "All levels",
                "time": "Ongoing"
            },
            {
                "name": "r/learnmachinelearning — Reddit community (250k+ members)",
                "type": "Community",
                "url": "https://reddit.com/r/learnmachinelearning",
                "cost": "Free",
                "why": "Ask questions, share wins, get resource recommendations. Weekly threads for beginners and project showcases.",
                "level": "All levels",
                "time": "Ongoing"
            }
        ]
    },
    "Web Developer": {
        "HTML/CSS/JavaScript Foundations": [
            {
                "name": "The Odin Project — Full Stack JavaScript curriculum (open source)",
                "type": "Free Curriculum",
                "url": "https://www.theodinproject.com/paths/full-stack-javascript",
                "cost": "Free",
                "why": "Project-based, community-driven curriculum used by thousands of self-taught developers who got hired. No fluff — you build real things from day 1.",
                "level": "Beginner",
                "time": "20–40 weeks (self-paced)"
            },
            {
                "name": "Jonas Schmedtmann — The Complete JavaScript Course 2024 (Udemy)",
                "type": "Paid Course",
                "url": "https://www.udemy.com/course/the-complete-javascript-course/",
                "cost": "$15–20 on sale (Udemy)",
                "why": "165 hours, 68 coding challenges, covers JavaScript deeply including closures, prototypes, async/await, ES6+. The most comprehensive JS course available.",
                "level": "Beginner → Advanced",
                "time": "60–80 hours focused"
            },
            {
                "name": "CSS Tricks — Complete Guide to Flexbox & Grid",
                "type": "Reference Documentation",
                "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/",
                "cost": "Free",
                "why": "The most-bookmarked CSS reference on the internet. Visual diagrams for every property. Use it every time you write Flexbox/Grid.",
                "level": "Beginner",
                "time": "Reference (not linear)"
            }
        ],
        "React & Modern Frontend": [
            {
                "name": "React Official Docs — react.dev (with interactive exercises)",
                "type": "Official Documentation",
                "url": "https://react.dev/learn",
                "cost": "Free",
                "why": "Completely rewritten in 2023 with interactive sandboxes. Learn useState, useEffect, useContext from the source. Much better than any third-party course.",
                "level": "Beginner → Intermediate",
                "time": "10–15 hours"
            },
            {
                "name": "Scrimba — Learn React (Bob Ziroll) — interactive code editor in browser",
                "type": "Free Interactive Course",
                "url": "https://scrimba.com/learn/learnreact",
                "cost": "Free",
                "why": "20 hours, 140+ challenges, you code INSIDE the video. Best for hands-on learners who hate watching passively.",
                "level": "Beginner",
                "time": "20 hours"
            }
        ],
        "Backend & APIs": [
            {
                "name": "Node.js — Official Getting Started Guide",
                "type": "Documentation",
                "url": "https://nodejs.dev/en/learn/",
                "cost": "Free",
                "why": "Official, up-to-date. Modules, file system, HTTP, streams, async patterns. Read this before any Node.js framework.",
                "level": "Beginner",
                "time": "5 hours"
            },
            {
                "name": "Traversy Media — Express JS Crash Course (YouTube)",
                "type": "YouTube Tutorial",
                "url": "https://www.youtube.com/watch?v=L72fhGm1tfE",
                "cost": "Free",
                "why": "90 minutes to production-ready Express API. REST endpoints, middleware, error handling, MongoDB integration. Highly practical.",
                "level": "Beginner",
                "time": "90 minutes"
            }
        ],
        "DSA for Web Dev Interviews": [
            {
                "name": "Roadmap.sh — JavaScript Algorithms (with visual explanations)",
                "type": "Reference + Practice",
                "url": "https://roadmap.sh/javascript",
                "cost": "Free",
                "why": "Web-specific DSA patterns: DOM manipulation complexity, event loop deep dive, prototype chain. Directly relevant to JS interviews.",
                "level": "Intermediate",
                "time": "5–8 hours"
            }
        ],
        "Interview Prep": [
            {
                "name": "Frontend Expert — Frontend system design crash course",
                "type": "Free Articles",
                "url": "https://www.frontendexpert.io",
                "cost": "Free (premium for full access)",
                "why": "Frontend system design questions: virtual DOM, event delegation, lazy loading, caching strategies. Rarely covered in generic interview prep.",
                "level": "Intermediate → Advanced",
                "time": "5–10 hours"
            }
        ],
        "Communities": [
            {
                "name": "Tech Ladies — Community for women in tech (jobs + mentors)",
                "type": "Community + Job Board",
                "url": "https://www.hiretechladies.com",
                "cost": "Free (premium job alerts available)",
                "why": "50,000+ women in tech. Job board with women-friendly company tags, mentorship matching, Slack community with role-specific channels.",
                "level": "All levels",
                "time": "Ongoing"
            }
        ]
    },
    "Data Analyst": {
        "SQL": [
            {
                "name": "Mode Analytics SQL Tutorial — beginner to advanced (with real datasets)",
                "type": "Interactive Tutorial",
                "url": "https://mode.com/sql-tutorial/",
                "cost": "Free",
                "why": "Goes from SELECT to window functions to query optimization. Practice on real-world data sets. Interactive SQL editor — no setup needed.",
                "level": "Beginner → Advanced",
                "time": "8–10 hours"
            },
            {
                "name": "StrataScratch — SQL interview questions by company",
                "type": "Practice Platform",
                "url": "https://www.stratascratch.com",
                "cost": "Free (premium: $29/mo)",
                "why": "Actual SQL interview questions from Netflix, Amazon, Airbnb. Filter by difficulty and company. Explains expected output step-by-step.",
                "level": "Intermediate",
                "time": "2–4 weeks practice"
            }
        ],
        "Python for Data Analysis": [
            {
                "name": "Kaggle — Pandas (micro-course, free certificates)",
                "type": "Free Course",
                "url": "https://www.kaggle.com/learn/pandas",
                "cost": "Free",
                "why": "4-hour focused pandas course: indexing, groupby, merge/join, time series. Exercises run in Kaggle notebook — no setup. Free certificate.",
                "level": "Beginner",
                "time": "4 hours"
            },
            {
                "name": "Wes McKinney — Python for Data Analysis (O'Reilly book)",
                "type": "Book",
                "url": "https://wesmckinney.com/book/",
                "cost": "Free online (HTML version)",
                "why": "Written by the creator of pandas. Goes deep on NumPy internals, pandas IO, time series. The definitive reference — free to read online.",
                "level": "Intermediate",
                "time": "Self-paced reference"
            }
        ],
        "Data Visualization": [
            {
                "name": "Storytelling With Data (Cole Nussbaumer Knaflic) — book + blog",
                "type": "Book + Blog",
                "url": "https://www.storytellingwithdata.com/books",
                "cost": "Free blog / $25 book",
                "why": "The go-to book for transforming data into compelling narratives. Learn when to use which chart, how to declutter, how to tell a data story executives understand.",
                "level": "Beginner → Intermediate",
                "time": "5–7 hours to read"
            },
            {
                "name": "Observable — D3.js notebooks community (visual inspiration + code)",
                "type": "Platform + Community",
                "url": "https://observablehq.com/@d3/gallery",
                "cost": "Free",
                "why": "Browse 500+ interactive visualizations with open source code. Fork any notebook and modify. Best way to learn D3 by example from the creator Mike Bostock.",
                "level": "Intermediate → Advanced",
                "time": "Reference"
            }
        ],
        "Interview Prep": [
            {
                "name": "DataLemur — SQL & Statistics interview questions (Nick Singh)",
                "type": "Practice Platform",
                "url": "https://datalemur.com",
                "cost": "Free",
                "why": "SQL questions from Meta, Google, Microsoft interviews organized by difficulty. Includes Python, machine learning, and stats questions. Explanation videos for each.",
                "level": "Intermediate",
                "time": "4–8 weeks practice"
            },
            {
                "name": "Nick Singh & Kevin Huo — Ace the Data Science Interview (book)",
                "type": "Book",
                "url": "https://www.acethedatascienceinterview.com",
                "cost": "$30",
                "why": "201 real interview questions from FAANG. Chapters on statistics, probability, ML, SQL, product sense. The most-recommended data interview prep book.",
                "level": "Intermediate → Advanced",
                "time": "10–15 hours"
            }
        ],
        "Communities": [
            {
                "name": "Data Is Plural — weekly newsletter of interesting datasets",
                "type": "Newsletter",
                "url": "https://www.data-is-plural.com",
                "cost": "Free",
                "why": "Find real datasets for practice projects. Signals you're keeping up with the field in interviews. 50,000+ subscribers.",
                "level": "All levels",
                "time": "10 min/week"
            }
        ]
    },
    "Career Re-entry into Tech": {
        "Refreshing Fundamentals": [
            {
                "name": "CS50P — Harvard's Introduction to Programming with Python (free certificate)",
                "type": "Free University Course",
                "url": "https://cs50.harvard.edu/python/2022/",
                "cost": "Free (certificate: $49)",
                "why": "Most respected free intro course on the internet. Problem sets are challenging but approachable. Certificate signals commitment to employers.",
                "level": "Beginner",
                "time": "10 weeks (5 hrs/week)"
            },
            {
                "name": "Git Immersion — hands-on Git tutorial (grounded in reality)",
                "type": "Interactive Tutorial",
                "url": "https://gitimmersion.com",
                "cost": "Free",
                "why": "Step-by-step Git exercises you run on your own machine. Covers branching, merging, rebasing. 3 hours to go from zero to confident.",
                "level": "Beginner",
                "time": "3 hours"
            }
        ],
        "Rebuilding Confidence": [
            {
                "name": "Reentry Works — career re-entry guide for tech professionals",
                "type": "Free Guide",
                "url": "https://www.returnship.com",
                "cost": "Free",
                "why": "Strategies specifically for people returning after a career break. Resume framing, interview scripts for explaining the gap, returnship program lists.",
                "level": "All levels",
                "time": "2–3 hours to read"
            },
            {
                "name": "Path Forward — returnship programs at top tech companies",
                "type": "Job Program",
                "url": "https://www.pathforward.org",
                "cost": "Free",
                "why": "Paid returnship programs at Amazon, PayPal, IBM specifically for people with 2+ year career breaks. Structured re-entry with mentoring.",
                "level": "All levels",
                "time": "Application-based"
            }
        ],
        "Portfolio Building": [
            {
                "name": "GitHub Pages — free portfolio hosting with custom domain support",
                "type": "Platform",
                "url": "https://pages.github.com",
                "cost": "Free",
                "why": "Shows technical skills (Git, HTML/CSS) AND gives a public URL to send to recruiters. Every project you build should live here.",
                "level": "Beginner",
                "time": "2 hours to set up"
            }
        ],
        "Communities": [
            {
                "name": "Tech Returners — community and programs for career returners in tech",
                "type": "Community + Program",
                "url": "https://techreturners.com",
                "cost": "Free",
                "why": "UK-based but global community. Structured returners programs, peer support, employer connections. Focuses specifically on tech career breaks.",
                "level": "All levels",
                "time": "Ongoing"
            },
            {
                "name": "iReTurn — global network for professionals returning after a career break",
                "type": "Community",
                "url": "https://ireturn.com",
                "cost": "Free",
                "why": "Connects returners to mentors and returnship programs globally. Events, webinars, peer groups organized by industry.",
                "level": "All levels",
                "time": "Ongoing"
            }
        ]
    }
}


def _get_roadmap_resources(roadmap_data: Dict) -> List[Dict]:
    """Extract all resources from the user's roadmap phases."""
    resources = []
    for phase in roadmap_data.get('phases', []):
        for week in phase.get('weeks', []):
            week_num = week.get('week_number', '?')
            focus = week.get('focus_skill', '')
            for res in week.get('resources', []):
                resources.append({
                    **res,
                    "_week": week_num,
                    "_skill": focus
                })
    return resources


def render_resources(db_client, user_data: Dict, roadmap_data: Dict, progress_data: Dict):
    """Render the Resources page with curated and roadmap resources."""
    
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h1 style="color: #1E293B; margin: 0;">📚 Your Learning Resources</h1>
        <p style="color: #64748B; margin-top: 0.25rem; font-size: 1.1rem;">
            Curated free & paid resources — specific, deep, and matched to your role
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # SECTION 1: ROADMAP RESOURCES (personalized to their path)
    # =========================================================
    roadmap_resources = _get_roadmap_resources(roadmap_data)
    
    if roadmap_resources:
        st.markdown("## 🗺️ From Your Personal Roadmap")
        st.caption("Resources your AI-generated roadmap specifically recommended for your goals")

        cost_filter = st.radio(
            "Filter by cost:", 
            ["All", "Free only", "Paid only"],
            horizontal=True,
            key="roadmap_res_filter"
        )

        free_count = sum(1 for r in roadmap_resources if str(r.get('cost', '')).lower() in ('free', '0', '$0'))
        paid_count = len(roadmap_resources) - free_count

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Resources", len(roadmap_resources))
        col2.metric("🆓 Free", free_count)
        col3.metric("💳 Paid", paid_count)

        st.markdown("---")

        for res in roadmap_resources:
            cost_raw = str(res.get('cost', '')).lower()
            is_free = cost_raw in ('free', '0', '$0')
            if cost_filter == "Free only" and not is_free:
                continue
            if cost_filter == "Paid only" and is_free:
                continue

            badge = "🆓" if is_free else "💳"
            cost_display = res.get('cost', 'Free')
            
            with st.container():
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"### {badge} {res.get('name', 'Resource')}")
                    st.caption(f"Week {res.get('_week', '?')} · {res.get('_skill', '')} · `{res.get('type', '')}` · {cost_display} · ⏱ {res.get('time_estimate', 'N/A')}")
                    if res.get('why_recommended'):
                        st.info(f"💡 **Why:** {res.get('why_recommended')}")
                with col_b:
                    url = res.get('url', '')
                    if url and url.startswith('http'):
                        st.markdown(f"\n\n[→ Open Resource]({url})", unsafe_allow_html=False)
            st.markdown("---")
    
    else:
        st.info("Your roadmap hasn't been generated yet, or doesn't have resources. Complete onboarding to get your personalized roadmap with curated resources.")

    # =========================================================
    # SECTION 2: CURATED CATALOG (role-specific)
    # =========================================================
    st.markdown("## 🎯 Curated Catalog by Role")
    st.caption("Expert-vetted resources organized by role, topic, and cost — not random, not generic")

    goal = user_data.get('goal', '')

    # Map goal to catalog key
    catalog_key = None
    if 'AI' in goal or 'Machine Learning' in goal or 'ML' in goal or 'Data Scientist' in goal:
        catalog_key = "AI Engineer"
    elif 'Web' in goal or 'Frontend' in goal or 'Full Stack' in goal or 'Backend' in goal:
        catalog_key = "Web Developer"
    elif 'Data Analyst' in goal or 'Analytics' in goal or 'BI' in goal:
        catalog_key = "Data Analyst"
    elif 'Re-entry' in goal or 'Career Break' in goal or 'Returning' in goal:
        catalog_key = "Career Re-entry into Tech"

    available_roles = list(CURATED_RESOURCES.keys())

    # Default tab to user's role
    default_idx = available_roles.index(catalog_key) if catalog_key and catalog_key in available_roles else 0

    tabs = st.tabs(available_roles)

    for tab, role_key in zip(tabs, available_roles):
        with tab:
            role_resources = CURATED_RESOURCES.get(role_key, {})

            # Cost filter for this tab
            tab_cost_filter = st.radio(
                "Show:", ["All", "Free only", "Paid only"],
                horizontal=True,
                key=f"catalog_filter_{role_key}"
            )

            for category, items in role_resources.items():
                st.markdown(f"### 📂 {category}")
                
                for item in items:
                    cost_raw = str(item.get('cost', '')).lower()
                    is_free = 'free' in cost_raw and '$' not in cost_raw.replace('free', '')
                    
                    if tab_cost_filter == "Free only" and not is_free:
                        continue
                    if tab_cost_filter == "Paid only" and is_free:
                        continue

                    badge = "🆓" if is_free else "💳"
                    
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{badge} {item.get('name', '')}**")
                            meta = f"`{item.get('type', '')}` · {item.get('cost', '')} · ⏱ {item.get('time', '')} · 📶 {item.get('level', '')}"
                            st.caption(meta)
                            st.markdown(f"> {item.get('why', '')}")
                        with col2:
                            url = item.get('url', '')
                            if url:
                                st.markdown(f"\n\n[→ Open]({url})")
                    
                    st.markdown("---")

    # =========================================================
    # SECTION 3: INTERVIEW PREP RESOURCES (always visible)
    # =========================================================
    st.markdown("## 🎤 Interview Prep Master List")
    st.caption("Resources specifically for getting hired, regardless of your role")

    interview_resources = [
        {
            "name": "Grokking the System Design Interview (Educative.io)",
            "type": "Interactive Course",
            "url": "https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers",
            "cost": "$33/mo (Educative)",
            "why": "The industry standard for system design prep. Covers URL shorteners, Twitter feeds, ride-sharing — exact format used in FAANG interviews.",
            "badge": "💳"
        },
        {
            "name": "Tech Interview Handbook — free guide by Blind 75 creator",
            "type": "Free Guide",
            "url": "https://www.techinterviewhandbook.org",
            "cost": "Free",
            "why": "Everything from resume to offer negotiation. Coding patterns cheatsheet, behavioral question templates, timeline planner. 50k GitHub stars.",
            "badge": "🆓"
        },
        {
            "name": "Pramp — free mock peer-to-peer technical interviews",
            "type": "Mock Interview",
            "url": "https://www.pramp.com",
            "cost": "Free (6 free sessions, then pay-per-use)",
            "why": "Practice as both interviewer and candidate. Real coding environment. Structured feedback form. Reduces interview jitters through repetition.",
            "badge": "🆓"
        },
        {
            "name": "Levels.fyi — salary data and interview experiences by company",
            "type": "Data Platform",
            "url": "https://www.levels.fyi",
            "cost": "Free",
            "why": "Know your market value BEFORE negotiating. Filter by role, location, company, YOE. Interview process details for specific companies.",
            "badge": "🆓"
        },
        {
            "name": "Cracking the Coding Interview 6th Ed. (Gayle Laakmann McDowell)",
            "type": "Book",
            "url": "https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850",
            "cost": "$24 (Amazon)",
            "why": "189 programming questions with detailed solutions. Chapter on behavioral questions, negotiation, and what interviewers actually look for. Classic for a reason.",
            "badge": "💳"
        },
        {
            "name": "She Geeks Out — community + job board for women in tech",
            "type": "Community",
            "url": "https://shegeeksout.com",
            "cost": "Free",
            "why": "Job board filters by 'women-friendly' companies. Events, mentorship, salary transparency. Specifically addresses the unique challenges of women in tech interviews.",
            "badge": "🆓"
        }
    ]

    cost_filter_interview = st.radio(
        "Filter:", ["All", "Free only", "Paid only"],
        horizontal=True,
        key="interview_res_filter"
    )

    for item in interview_resources:
        cost_raw = item.get('cost', '').lower()
        is_free = 'free' in cost_raw and '$' not in cost_raw.replace('free (', '')
        if cost_filter_interview == "Free only" and not is_free:
            continue
        if cost_filter_interview == "Paid only" and is_free:
            continue

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{item['badge']} {item['name']}**")
            st.caption(f"`{item.get('type', '')}` · {item.get('cost', '')}")
            st.markdown(f"> {item.get('why', '')}")
        with col2:
            if item.get('url'):
                st.markdown(f"\n\n[→ Open]({item['url']})")
        st.markdown("---")
