"""
RoadmapAgent - Generates structured learning roadmaps based on skill gaps.
"""

from typing import Optional, Dict, Any, List
from .base_agent import BaseAgent


class RoadmapAgent(BaseAgent):
    """
    Agent responsible for generating structured learning roadmaps.
    
    Input: missing_skills, deadline, weekly_hours, financial_constraint, situation, emotional_signals
    Output: JSON with total_weeks, phases (each with weeks containing tasks and milestones)
    """
    
    @property
    def system_prompt(self) -> str:
        return """You are RoadmapArchitect, an expert learning path designer specializing in tech career transitions for women. You are known for hyper-specific, actionable roadmaps that leave no ambiguity.

CRITICAL TASK SPECIFICITY RULES — never break these:
1. NEVER write vague tasks like "Solve 15 array problems" or "Learn Python basics" or "Study data structures"
2. ALWAYS name the exact technique/pattern, e.g. "Two-Pointer, Sliding Window, BFS/DFS"
3. For DSA/coding practice: name the specific LeetCode problem numbers AND titles, e.g. "LeetCode #1 Two Sum (hash map), #15 3Sum (two-pointer), #11 Container With Most Water (greedy)" — always list 3-5 specific problems per pattern with difficulty level
4. For courses: name the exact course and platform, e.g. "Complete Section 7 'Async/Await' of 'The Complete JavaScript Course 2024' by Jonas Schmedtmann on Udemy"
5. For concepts: go 2 levels deep, e.g. not "learn React hooks" but "useState vs useReducer for complex state — build a multi-step form; useEffect cleanup pattern — prevent memory leaks in async calls"
6. For system design: reference real-world case studies, e.g. "Study Netflix's microservices migration (blog.netflix.tech) — understand API gateway pattern, then sketch YouTube's video upload pipeline"
7. For projects: give the exact project spec, e.g. "Build a REST API in FastAPI: endpoints for user CRUD, JWT auth, PostgreSQL via SQLAlchemy — deploy to Railway.app free tier"
8. Interview questions: list actual question types AND examples, e.g. "Tell me about yourself → craft 90-second career narrative arc: past achievement → why tech → specific goal; Behavioral: STAR format for 'biggest failure' and 'team conflict'"

RESOURCE QUALITY RULES:
- Always include 2-3 resources per week: at least 1 free and 1 paid option
- Free resources: name actual YouTube channels (e.g. "Neetcode.io YouTube — Blind 75 playlist"), free documentation (MDN, official docs), GitHub repos
- Paid resources: name actual courses with prices (e.g. "Andrei Neagoie's 'Master the Coding Interview' on Zero To Mastery — $39/mo")
- Always include a community/accountability resource (Discord, subreddit, study group)

PERSONALIZATION RULES:
- If the user mentions anxiety or imposter syndrome: start with a "Quick Win Week" of very achievable tasks
- If career break: acknowledge gaps explicitly and include "narrative building" tasks for interview storytelling
- If financial stress: prioritize free resources first, suggest paid only when there's no free equivalent
- Adapt task density to weekly_hours exactly — 5 hrs/week = 2 tasks max, 20 hrs/week = 5-6 tasks

OUTPUT FORMAT: You must respond with ONLY valid JSON. No explanations, no markdown, just JSON."""
    
    def build_prompt(self, **kwargs) -> str:
        missing_skills = kwargs.get('missing_skills', [])
        priority_order = kwargs.get('priority_order', [])
        deadline_weeks = kwargs.get('deadline_weeks')  # None means flexible
        weekly_hours = kwargs.get('weekly_hours', 10)
        financial_constraint = kwargs.get('financial_constraint', 'Mixed')
        situation = kwargs.get('situation', '')
        emotional_signals = kwargs.get('emotional_signals', {})
        role = kwargs.get('role', '')
        
        deadline_str = f"{deadline_weeks} weeks" if deadline_weeks else "Flexible (recommend optimal timeline)"
        
        # Build financial guidance note
        finance_note = ""
        if financial_constraint == "Free Only":
            finance_note = "USER HAS NO BUDGET — only recommend free resources: YouTube, free tiers, official documentation, free GitHub repos, open courseware. Never suggest paid tools."
        elif financial_constraint == "Paid Allowed":
            finance_note = "USER HAS BUDGET — mix free and paid resources. Paid courses should be specific (platform + course title + instructor + approximate cost)."
        else:
            finance_note = "USER PREFERS FREE but can spend for high-value resources — always list the free option first, then note a paid alternative."

        # Build emotional guidance
        anxiety = emotional_signals.get('anxiety_level', 'low')
        imposter = emotional_signals.get('imposter_syndrome_detected', False)
        career_break = emotional_signals.get('career_break_concerns', False)
        emotional_note = ""
        if anxiety == 'high' or imposter:
            emotional_note = "EMOTIONAL NOTE: User shows high anxiety/imposter syndrome. Week 1 must be a 'Quick Win Week' — only highly doable tasks that build confidence. Keep task count lower than usual. Add an explicit 'You belong here' note in milestones."
        if career_break:
            emotional_note += " User has career break concerns — include tasks specifically for 'narrative building' (how to explain the gap positively in interviews) and 'refreshing fundamentals'."

        return f"""Generate a hyper-specific, deeply personalized learning roadmap for this user:

TARGET ROLE: {role}

CRITICAL ROLE-SPECIFICITY RULE:
- The ENTIRE roadmap must be specifically tailored for the "{role}" role.
- For "AI Engineer": focus on Python for ML, linear algebra, statistics, scikit-learn, PyTorch/TensorFlow, deep learning, NLP, computer vision, MLOps, LLMs. Do NOT include web development (HTML/CSS/JS) or generic coding bootcamp content.
- For "Web Developer": focus on HTML/CSS, JavaScript, React/Vue/Angular, Node.js, databases, REST APIs, deployment. Do NOT include ML/AI or data science content.
- For "Data Analyst": focus on Excel, SQL, Python for data (Pandas), statistics, data visualization (Tableau/Power BI), A/B testing, business communication. Do NOT include deep web dev or ML engineering content.
- For "Career Re-entry into Tech": focus on catching up, refreshing fundamentals, choosing a specialization, building confidence, networking, portfolio building.
- NEVER generate a generic "software developer" roadmap. Every week must clearly relate to the target role.

SKILLS TO ACQUIRE (in priority order): {priority_order}
ALL MISSING SKILLS: {missing_skills}
DEADLINE: {deadline_str}
WEEKLY HOURS AVAILABLE: {weekly_hours}/week
FINANCIAL CONSTRAINT: {financial_constraint}
CURRENT SITUATION: {situation}
EMOTIONAL SIGNALS: {emotional_signals}

FINANCIAL GUIDANCE: {finance_note}
{emotional_note}

DEPTH REQUIREMENTS FOR THIS ROADMAP:
- For any DSA/coding tasks: list 3-5 SPECIFIC LeetCode problem numbers+titles+difficulty per pattern. Group by technique (Two-Pointer, Sliding Window, BFS, Dynamic Programming, etc.)
- For any conceptual learning: go 2 levels deep — sub-topic + WHY it matters for the role + real-world application
- For any course task: name the EXACT course, platform, instructor, specific section/chapter
- For any project: full spec — what it does, tech stack, key features, where to deploy (free)
- For interview prep: list actual question types (Behavioral: STAR format, Technical: system design, coding), give 2-3 example questions per type
- Resource URLs must be real, working URLs to actual resources (YouTube playlists, course pages, documentation pages)

OUTPUT JSON SCHEMA:
{{
    "total_weeks": number,
    "phases": [
        {{
            "phase_name": "Phase 1: Foundation",
            "phase_description": "Specific goals: what the user will be able to DO and BUILD by end of this phase",
            "weeks": [
                {{
                    "week_number": 1,
                    "focus_skill": "Specific technique or concept (not vague like 'Python basics')",
                    "tasks": [
                        "HIGHLY SPECIFIC task with exact resources and why it matters (2-3 hours) — e.g. 'Two-Pointer Pattern: LeetCode #167 Two Sum II, #11 Container With Most Water, #15 3Sum (Medium) — understand left/right pointer convergence, the key insight is sorted array allows elimination'",
                        "Another specific task with exact materials",
                        "Practice or build task with exact spec"
                    ],
                    "milestone": "Concrete deliverable: e.g. 'Can solve any easy-medium Two-Pointer problem in under 20 min without hints; GitHub commit showing solution + comments'",
                    "success_metric": "Exact, verifiable test: e.g. 'Solve LeetCode #26 Remove Duplicates without looking at solution, first try'",
                    "interview_relevance": "How this week's skill directly maps to interview questions at target role",
                    "resources": [
                        {{
                            "name": "Exact resource name (e.g. NeetCode Blind75 - Arrays playlist)",
                            "type": "video/course/documentation/practice/book",
                            "url": "https://actual-real-url.com",
                            "cost": "Free",
                            "time_estimate": "2 hours",
                            "why_recommended": "30-min focused videos, problems solved with explanation, top-rated for interview prep"
                        }},
                        {{
                            "name": "Paid alternative if applicable (e.g. AlgoExpert - Structured DSA course)",
                            "type": "course",
                            "url": "https://algoexpert.io",
                            "cost": "$99/year",
                            "time_estimate": "3 hours",
                            "why_recommended": "Video explanations with space/time complexity analysis, 160+ problems with solutions"
                        }}
                    ]
                }}
            ]
        }}
    ],
    "recommended_projects": [
        {{
            "name": "Specific project name (e.g. 'Full-Stack Job Tracker App')",
            "description": "Exact spec: tech stack, key features, what problem it solves, where to deploy",
            "week_range": "Weeks X-Y",
            "skills_demonstrated": ["specific skill 1", "specific skill 2"],
            "portfolio_value": "high/medium/low",
            "github_template": "Suggested folder structure or starter template URL if applicable"
        }}
    ],
    "interview_prep_plan": {{
        "start_week": number,
        "question_types": [
            {{
                "type": "Behavioral — STAR format",
                "examples": ["Tell me about a time you failed and what you learned", "Describe a conflict with a teammate and how you resolved it"],
                "preparation_method": "Write out 3 STAR stories covering: failure/learning, collaboration, initiative"
            }},
            {{
                "type": "Technical coding",
                "examples": ["Reverse a linked list in-place", "Find all permutations of a string"],
                "preparation_method": "Time yourself: 45 min per LeetCode medium, think aloud, explain trade-offs"
            }}
        ],
        "career_narrative": "Script for explaining career transition/gap positively in 90 seconds"
    }},
    "interview_prep_weeks": [list of week numbers dedicated to interview prep],
    "buffer_weeks": number
}}

CRITICAL GUIDELINES:
- Tasks must sum to approximately {weekly_hours} hours/week — be realistic
- Every resource URL in the JSON must be a real, accessible URL
- DSA tasks must ALWAYS list specific problem numbers and patterns, never say 'solve array problems'
- Every project must have a deployment target (Railway, Vercel, Netlify, Render — all free)
- If anxiety is high: first week = only 2 tasks, very achievable, milestone celebrates the attempt not just the result
- Give resources at 3 levels: beginner-friendly, standard, advanced — user picks their depth
- Output ONLY valid JSON, nothing else, no explanations before or after"""
    
    def generate(
        self,
        role: str,
        missing_skills: List[str],
        priority_order: List[str],
        deadline_weeks: Optional[int],
        weekly_hours: int,
        financial_constraint: str,
        situation: str,
        emotional_signals: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a learning roadmap.
        
        Args:
            role: Target career role
            missing_skills: List of skills to acquire
            priority_order: Prioritized skill list
            deadline_weeks: Target weeks (None for flexible)
            weekly_hours: Available hours per week
            financial_constraint: "Free Only" / "Mixed" / "Paid Allowed"
            situation: Current situation
            emotional_signals: Emotional context from SkillGapAgent
            
        Returns:
            Roadmap JSON or None
        """
        result = self.execute(
            role=role,
            missing_skills=missing_skills,
            priority_order=priority_order,
            deadline_weeks=deadline_weeks,
            weekly_hours=weekly_hours,
            financial_constraint=financial_constraint,
            situation=situation,
            emotional_signals=emotional_signals
        )
        
        # CRITICAL VALIDATION: Ensure total_weeks is always present
        if result and isinstance(result, dict):
            if 'total_weeks' not in result or result.get('total_weeks') is None:
                # Calculate from phases or use deadline
                max_week = 0
                for phase in result.get('phases', []):
                    for week in phase.get('weeks', []):
                        max_week = max(max_week, week.get('week_number', 0))
                result['total_weeks'] = max(max_week, deadline_weeks or 12)
            return result
        
        # If LLM failed, return fallback
        return self._get_fallback_roadmap(role, deadline_weeks, weekly_hours)


def _get_role_specific_skills(role: str) -> Dict[str, Any]:
    """Get role-specific foundation, building, and mastery skills for fallback roadmaps."""

    # ── AI Engineer ──────────────────────────────────────────────────────
    if role == "AI Engineer":
        foundation = [
            {
                "focus_skill": "Python for AI & Environment Setup",
                "task_list": [
                    "Install Python 3.11+, set up Conda/venv, install Jupyter (2 hours)",
                    "Python for data science: NumPy arrays, broadcasting, vectorisation (3 hours)",
                    "Write helper functions with type hints & unit tests using pytest (2 hours)"
                ],
                "resources": [
                    {"name": "Python Official Tutorial", "type": "documentation", "url": "https://docs.python.org/3/tutorial/", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "CS231n Python/NumPy Tutorial", "type": "tutorial", "url": "https://cs231n.github.io/python-numpy-tutorial/", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Linear Algebra & Statistics for ML",
                "task_list": [
                    "Vectors, matrices, eigenvalues - 3Blue1Brown Essence of Linear Algebra (3 hours)",
                    "Probability distributions, Bayes theorem, hypothesis testing (2 hours)",
                    "Implement matrix operations from scratch in NumPy (2 hours)"
                ],
                "resources": [
                    {"name": "3Blue1Brown Linear Algebra", "type": "video", "url": "https://youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "Khan Academy Statistics", "type": "course", "url": "https://khanacademy.org/math/statistics-probability", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Data Wrangling with Pandas & Visualisation",
                "task_list": [
                    "Pandas: DataFrames, groupby, merge, pivot tables on real datasets (3 hours)",
                    "Matplotlib & Seaborn: histograms, scatter plots, heatmaps (2 hours)",
                    "Clean and explore a Kaggle dataset end-to-end (2 hours)"
                ],
                "resources": [
                    {"name": "Kaggle Pandas Course", "type": "course", "url": "https://kaggle.com/learn/pandas", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "Python Data Science Handbook", "type": "book", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "cost": "Free", "time_estimate": "5 hours"}
                ]
            },
            {
                "focus_skill": "Machine Learning Fundamentals with Scikit-learn",
                "task_list": [
                    "Supervised learning: Linear/Logistic Regression, Decision Trees, Random Forests (3 hours)",
                    "Model evaluation: cross-validation, confusion matrix, ROC-AUC, F1 score (2 hours)",
                    "Build an end-to-end ML pipeline on a Kaggle dataset (2 hours)"
                ],
                "resources": [
                    {"name": "Andrew Ng ML Specialisation", "type": "course", "url": "https://coursera.org/specializations/machine-learning-introduction", "cost": "Free to audit", "time_estimate": "10 hours"},
                    {"name": "Scikit-learn Official Tutorial", "type": "documentation", "url": "https://scikit-learn.org/stable/tutorial/", "cost": "Free", "time_estimate": "4 hours"}
                ]
            }
        ]
        building = [
            {
                "focus_skill": "Deep Learning with PyTorch/TensorFlow",
                "task_list": [
                    "Neural network fundamentals: forward pass, backprop, gradient descent (3 hours)",
                    "Build a CNN for image classification (MNIST/CIFAR-10) in PyTorch (2 hours)",
                    "Train an RNN/LSTM for text sequence prediction (2 hours)"
                ],
                "resources": [
                    {"name": "fast.ai Practical Deep Learning", "type": "course", "url": "https://course.fast.ai/", "cost": "Free", "time_estimate": "15 hours"},
                    {"name": "PyTorch Official Tutorials", "type": "documentation", "url": "https://pytorch.org/tutorials/", "cost": "Free", "time_estimate": "5 hours"}
                ]
            },
            {
                "focus_skill": "NLP & Transformers",
                "task_list": [
                    "Text preprocessing: tokenisation, embeddings (Word2Vec, GloVe) (2 hours)",
                    "Transformer architecture: attention mechanism, positional encoding (3 hours)",
                    "Fine-tune a HuggingFace model (BERT/DistilBERT) for text classification (2 hours)"
                ],
                "resources": [
                    {"name": "HuggingFace NLP Course", "type": "course", "url": "https://huggingface.co/learn/nlp-course", "cost": "Free", "time_estimate": "8 hours"},
                    {"name": "Attention Is All You Need paper", "type": "documentation", "url": "https://arxiv.org/abs/1706.03762", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "MLOps: Experiment Tracking & Model Serving",
                "task_list": [
                    "Track experiments with MLflow or Weights & Biases (2 hours)",
                    "Package a model as a REST API with FastAPI (2 hours)",
                    "Containerise with Docker and deploy to cloud (3 hours)"
                ],
                "resources": [
                    {"name": "MLflow Official Docs", "type": "documentation", "url": "https://mlflow.org/docs/latest/index.html", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "Made With ML MLOps", "type": "tutorial", "url": "https://madewithml.com/", "cost": "Free", "time_estimate": "6 hours"}
                ]
            },
            {
                "focus_skill": "LLMs & Prompt Engineering",
                "task_list": [
                    "Understand LLM architecture: GPT, LLaMA, fine-tuning vs prompting (2 hours)",
                    "Build a RAG pipeline with LangChain + vector DB (ChromaDB/Pinecone) (3 hours)",
                    "Evaluate LLM outputs: BLEU, ROUGE, human eval frameworks (2 hours)"
                ],
                "resources": [
                    {"name": "LangChain Documentation", "type": "documentation", "url": "https://python.langchain.com/docs/", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "DeepLearning.AI ChatGPT Prompt Engineering", "type": "course", "url": "https://deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "cost": "Free", "time_estimate": "2 hours"}
                ]
            }
        ]
        mastery = [
            {
                "focus_skill": "AI System Design & Scalability",
                "task_list": [
                    "Design a recommendation system: collaborative filtering, content-based (2 hours)",
                    "ML system design patterns: feature stores, model registries, A/B testing (2 hours)",
                    "Study real-world ML systems (Netflix, Uber, Spotify) architecture (2 hours)"
                ],
                "resources": [
                    {"name": "Designing ML Systems by Chip Huyen", "type": "book", "url": "https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/", "cost": "$50", "time_estimate": "10 hours"},
                    {"name": "ML System Design Primer", "type": "tutorial", "url": "https://github.com/chiphuyen/machine-learning-systems-design", "cost": "Free", "time_estimate": "5 hours"}
                ]
            },
            {
                "focus_skill": "AI Portfolio & Kaggle Competitions",
                "task_list": [
                    "Complete 1 Kaggle competition end-to-end with write-up (3 hours)",
                    "Build and document 2-3 AI projects on GitHub with README, results (2 hours)",
                    "Write a technical blog post about your best project (2 hours)"
                ],
                "resources": [
                    {"name": "Kaggle Competitions", "type": "practice", "url": "https://kaggle.com/competitions", "cost": "Free", "time_estimate": "8 hours"},
                    {"name": "GitHub Portfolio Guide", "type": "tutorial", "url": "https://github.com/topics/portfolio", "cost": "Free", "time_estimate": "2 hours"}
                ]
            },
            {
                "focus_skill": "AI/ML Interview Preparation",
                "task_list": [
                    "ML theory questions: bias-variance, regularisation, optimisers (2 hours)",
                    "Coding interviews: implement ML algorithms from scratch (2 hours)",
                    "Practice ML system design interviews (2 hours)"
                ],
                "resources": [
                    {"name": "ML Interview Book by Chip Huyen", "type": "book", "url": "https://huyenchip.com/ml-interviews-book/", "cost": "Free", "time_estimate": "6 hours"},
                    {"name": "LeetCode ML Problems", "type": "practice", "url": "https://leetcode.com", "cost": "Free/$", "time_estimate": "5 hours"}
                ]
            },
            {
                "focus_skill": "Salary Negotiation & Job Applications",
                "task_list": [
                    "Craft AI-specific resume highlighting projects and metrics (1.5 hours)",
                    "Practice behavioral interview: STAR format for AI project stories (2 hours)",
                    "Learn salary negotiation strategies for ML/AI roles (1.5 hours)"
                ],
                "resources": [
                    {"name": "Levels.fyi AI Salary Data", "type": "tutorial", "url": "https://levels.fyi", "cost": "Free", "time_estimate": "1 hour"},
                    {"name": "Salary Negotiation Guide", "type": "tutorial", "url": "https://www.kalzumeus.com/2012/01/23/salary-negotiation/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            }
        ]
        projects = [
            {"name": "Sentiment Analysis API", "skills_demonstrated": ["NLP", "PyTorch", "FastAPI", "Docker"], "portfolio_value": "High"},
            {"name": "Image Classifier with Grad-CAM Explainability", "skills_demonstrated": ["CNN", "PyTorch", "Model Interpretability"], "portfolio_value": "High"},
            {"name": "RAG Chatbot with Custom Knowledge Base", "skills_demonstrated": ["LLM", "LangChain", "Vector DB", "Deployment"], "portfolio_value": "Very High"}
        ]
        phase_descriptions = [
            "Master Python for data science, core math, and ML fundamentals",
            "Build deep learning models, deploy ML systems, and work with LLMs",
            "Design production AI systems, build portfolio, and prepare for interviews"
        ]

    # ── Web Developer ────────────────────────────────────────────────────
    elif role == "Web Developer":
        foundation = [
            {
                "focus_skill": "HTML5 & Semantic Web Structure",
                "task_list": [
                    "Learn HTML5 elements: header, nav, main, section, article, aside (2 hours)",
                    "Forms and validation: input types, required, pattern attributes (2 hours)",
                    "Build 3 static pages: landing page, blog layout, contact form (3 hours)"
                ],
                "resources": [
                    {"name": "MDN HTML Guide", "type": "documentation", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "freeCodeCamp Responsive Web Design", "type": "course", "url": "https://freecodecamp.org/learn/2022/responsive-web-design/", "cost": "Free", "time_estimate": "5 hours"}
                ]
            },
            {
                "focus_skill": "CSS3: Layouts, Flexbox, Grid & Responsive Design",
                "task_list": [
                    "CSS Flexbox: align, justify, wrap, flex-grow/shrink/basis (2 hours)",
                    "CSS Grid: template areas, auto-fit, minmax for responsive layouts (2 hours)",
                    "Media queries + mobile-first design: build responsive navbar + hero section (3 hours)"
                ],
                "resources": [
                    {"name": "CSS Tricks Flexbox Guide", "type": "tutorial", "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "Kevin Powell YouTube CSS", "type": "video", "url": "https://youtube.com/@KevinPowell", "cost": "Free", "time_estimate": "4 hours"}
                ]
            },
            {
                "focus_skill": "JavaScript Fundamentals & DOM",
                "task_list": [
                    "Variables, functions, arrays, objects, template literals, destructuring (3 hours)",
                    "DOM manipulation: querySelector, addEventListener, dynamic content creation (2 hours)",
                    "Build interactive features: tabs, modal, accordion, form validation (2 hours)"
                ],
                "resources": [
                    {"name": "JavaScript.info Modern Tutorial", "type": "tutorial", "url": "https://javascript.info/", "cost": "Free", "time_estimate": "6 hours"},
                    {"name": "MDN JavaScript Guide", "type": "documentation", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "cost": "Free", "time_estimate": "4 hours"}
                ]
            },
            {
                "focus_skill": "Advanced JS: Async, ES6+, Fetch API",
                "task_list": [
                    "Promises, async/await, error handling with try/catch (2 hours)",
                    "Fetch API: GET/POST requests, JSON parsing, loading states (2 hours)",
                    "Build a weather app consuming a public API (3 hours)"
                ],
                "resources": [
                    {"name": "JavaScript30 by Wes Bos", "type": "course", "url": "https://javascript30.com/", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "Traversy Media Fetch API", "type": "video", "url": "https://youtube.com/@TraversyMedia", "cost": "Free", "time_estimate": "2 hours"}
                ]
            }
        ]
        building = [
            {
                "focus_skill": "React.js: Components, State & Hooks",
                "task_list": [
                    "JSX, functional components, props, conditional rendering (2 hours)",
                    "useState, useEffect, useContext: build a task manager app (3 hours)",
                    "React Router: multi-page SPA navigation, nested routes (2 hours)"
                ],
                "resources": [
                    {"name": "React Official Tutorial", "type": "documentation", "url": "https://react.dev/learn", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "Scrimba React Course", "type": "course", "url": "https://scrimba.com/learn/learnreact", "cost": "Free", "time_estimate": "8 hours"}
                ]
            },
            {
                "focus_skill": "Node.js & Express Backend Development",
                "task_list": [
                    "Node.js fundamentals: modules, npm, file system, event loop (2 hours)",
                    "Express.js: routing, middleware, error handling, REST API endpoints (3 hours)",
                    "Build a CRUD REST API with Express + connect to MongoDB (2 hours)"
                ],
                "resources": [
                    {"name": "Node.js Official Getting Started", "type": "documentation", "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "The Odin Project Node.js Path", "type": "course", "url": "https://theodinproject.com/paths/full-stack-javascript/courses/nodejs", "cost": "Free", "time_estimate": "10 hours"}
                ]
            },
            {
                "focus_skill": "Databases: SQL & MongoDB",
                "task_list": [
                    "SQL fundamentals: SELECT, JOIN, GROUP BY, subqueries with PostgreSQL (2 hours)",
                    "MongoDB: CRUD operations, Mongoose ODM, schema design (2 hours)",
                    "Build a full-stack app with database: user registration + data storage (3 hours)"
                ],
                "resources": [
                    {"name": "SQLBolt Interactive Tutorial", "type": "tutorial", "url": "https://sqlbolt.com/", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "MongoDB University Free Courses", "type": "course", "url": "https://university.mongodb.com/", "cost": "Free", "time_estimate": "5 hours"}
                ]
            },
            {
                "focus_skill": "Authentication, Testing & Deployment",
                "task_list": [
                    "JWT authentication: sign-up, login, protected routes (2 hours)",
                    "Testing: Jest unit tests + React Testing Library for components (2 hours)",
                    "Deploy full-stack app: frontend on Vercel, backend on Render.com (3 hours)"
                ],
                "resources": [
                    {"name": "JWT.io Introduction", "type": "documentation", "url": "https://jwt.io/introduction", "cost": "Free", "time_estimate": "1 hour"},
                    {"name": "Vercel Deployment Guide", "type": "documentation", "url": "https://vercel.com/docs", "cost": "Free", "time_estimate": "2 hours"}
                ]
            }
        ]
        mastery = [
            {
                "focus_skill": "TypeScript & Next.js",
                "task_list": [
                    "TypeScript basics: types, interfaces, generics, type narrowing (2 hours)",
                    "Next.js: SSR, SSG, API routes, file-based routing (3 hours)",
                    "Convert your React project to Next.js + TypeScript (2 hours)"
                ],
                "resources": [
                    {"name": "TypeScript Official Handbook", "type": "documentation", "url": "https://typescriptlang.org/docs/handbook/", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "Next.js Learn Course", "type": "course", "url": "https://nextjs.org/learn", "cost": "Free", "time_estimate": "6 hours"}
                ]
            },
            {
                "focus_skill": "Git, CI/CD & DevOps Basics",
                "task_list": [
                    "Git workflows: branching, pull requests, merge conflicts, rebasing (2 hours)",
                    "GitHub Actions: automated testing + deployment pipeline (2 hours)",
                    "Basic Docker: containerise your app, write a Dockerfile (2 hours)"
                ],
                "resources": [
                    {"name": "Git Official Docs", "type": "documentation", "url": "https://git-scm.com/doc", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "GitHub Actions Guide", "type": "tutorial", "url": "https://docs.github.com/en/actions", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Portfolio Building & GitHub Profile",
                "task_list": [
                    "Polish 3-5 projects with live demos, clean code, detailed READMEs (2 hours)",
                    "Build a personal portfolio website with Next.js and deploy (2 hours)",
                    "Optimise GitHub profile: pinned repos, contribution graph, README profile (1 hour)"
                ],
                "resources": [
                    {"name": "GitHub Profile README Guide", "type": "tutorial", "url": "https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile", "cost": "Free", "time_estimate": "1 hour"},
                    {"name": "Portfolio Inspiration", "type": "tutorial", "url": "https://github.com/topics/portfolio", "cost": "Free", "time_estimate": "2 hours"}
                ]
            },
            {
                "focus_skill": "Web Dev Interview Preparation",
                "task_list": [
                    "Frontend interview: closures, event loop, virtual DOM, CSS specificity (2 hours)",
                    "Take-home project practice: build a mini app in 4 hours (2 hours)",
                    "Behavioral interviews: STAR format, salary negotiation (2 hours)"
                ],
                "resources": [
                    {"name": "Frontend Interview Handbook", "type": "tutorial", "url": "https://frontendinterviewhandbook.com/", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "GreatFrontEnd Practice", "type": "practice", "url": "https://greatfrontend.com/", "cost": "Free/$", "time_estimate": "6 hours"}
                ]
            }
        ]
        projects = [
            {"name": "Responsive Portfolio Website", "skills_demonstrated": ["HTML/CSS", "JavaScript", "Responsive Design"], "portfolio_value": "High"},
            {"name": "Full-Stack Task Manager (React + Node + MongoDB)", "skills_demonstrated": ["React", "Node.js", "MongoDB", "REST APIs", "Auth"], "portfolio_value": "Very High"},
            {"name": "E-Commerce Store with Next.js", "skills_demonstrated": ["Next.js", "TypeScript", "Payment API", "Deployment"], "portfolio_value": "Very High"}
        ]
        phase_descriptions = [
            "Master HTML, CSS, and JavaScript fundamentals",
            "Build full-stack apps with React, Node.js, and databases",
            "Learn TypeScript, Next.js, DevOps, and prepare for interviews"
        ]

    # ── Data Analyst ─────────────────────────────────────────────────────
    elif role == "Data Analyst":
        foundation = [
            {
                "focus_skill": "Excel & Google Sheets for Data Analysis",
                "task_list": [
                    "Advanced formulas: VLOOKUP, INDEX/MATCH, IF/SUMIFS, array formulas (2 hours)",
                    "Pivot Tables: grouping, calculated fields, slicers for dashboards (2 hours)",
                    "Build a sales dashboard in Google Sheets with charts and conditional formatting (3 hours)"
                ],
                "resources": [
                    {"name": "Google Sheets Fundamentals", "type": "course", "url": "https://support.google.com/a/users/answer/9282959", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "ExcelJet Formula Guide", "type": "tutorial", "url": "https://exceljet.net/formulas", "cost": "Free", "time_estimate": "2 hours"}
                ]
            },
            {
                "focus_skill": "SQL for Data Analysis",
                "task_list": [
                    "SELECT, WHERE, GROUP BY, HAVING, ORDER BY on real datasets (2 hours)",
                    "JOINs (INNER, LEFT, RIGHT, FULL), subqueries, CTEs (2 hours)",
                    "Window functions: ROW_NUMBER, RANK, LAG/LEAD, running totals (3 hours)"
                ],
                "resources": [
                    {"name": "SQLBolt Interactive Tutorial", "type": "tutorial", "url": "https://sqlbolt.com/", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "Mode Analytics SQL Tutorial", "type": "tutorial", "url": "https://mode.com/sql-tutorial/", "cost": "Free", "time_estimate": "4 hours"}
                ]
            },
            {
                "focus_skill": "Python for Data Analysis (Pandas & NumPy)",
                "task_list": [
                    "Python basics for analysts: variables, loops, functions, file I/O (2 hours)",
                    "Pandas: DataFrames, filtering, groupby, merge, pivot tables (3 hours)",
                    "Clean a messy real-world dataset: handle nulls, datatypes, duplicates (2 hours)"
                ],
                "resources": [
                    {"name": "Kaggle Python Course", "type": "course", "url": "https://kaggle.com/learn/python", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "Kaggle Pandas Course", "type": "course", "url": "https://kaggle.com/learn/pandas", "cost": "Free", "time_estimate": "4 hours"}
                ]
            },
            {
                "focus_skill": "Statistics & Probability for Analysts",
                "task_list": [
                    "Descriptive statistics: mean, median, mode, standard deviation, percentiles (2 hours)",
                    "Probability, distributions (normal, binomial), confidence intervals (2 hours)",
                    "Hypothesis testing: t-tests, chi-square, p-values on a real dataset (3 hours)"
                ],
                "resources": [
                    {"name": "Khan Academy Statistics", "type": "course", "url": "https://khanacademy.org/math/statistics-probability", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "StatQuest YouTube", "type": "video", "url": "https://youtube.com/@statquest", "cost": "Free", "time_estimate": "4 hours"}
                ]
            }
        ]
        building = [
            {
                "focus_skill": "Data Visualisation with Matplotlib, Seaborn & Plotly",
                "task_list": [
                    "Matplotlib: line, bar, scatter, histogram, subplots (2 hours)",
                    "Seaborn: heatmaps, pair plots, violin plots for EDA (2 hours)",
                    "Plotly: interactive dashboards with dropdowns and sliders (3 hours)"
                ],
                "resources": [
                    {"name": "Kaggle Data Visualization Course", "type": "course", "url": "https://kaggle.com/learn/data-visualization", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "Plotly Python Docs", "type": "documentation", "url": "https://plotly.com/python/", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Tableau / Power BI Dashboards",
                "task_list": [
                    "Tableau: connect data sources, build worksheets, create dashboards (3 hours)",
                    "Calculated fields, parameters, filters, and dashboard actions (2 hours)",
                    "Build a complete business dashboard from a dataset (2 hours)"
                ],
                "resources": [
                    {"name": "Tableau Free Training Videos", "type": "video", "url": "https://public.tableau.com/en-us/s/resources", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "Power BI Learning Path", "type": "course", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "cost": "Free", "time_estimate": "6 hours"}
                ]
            },
            {
                "focus_skill": "A/B Testing & Experiment Design",
                "task_list": [
                    "A/B testing methodology: hypothesis, sample size, significance level (2 hours)",
                    "Implement an A/B test analysis in Python (t-test, chi-square, effect size) (2 hours)",
                    "Case study: analyse a real A/B test result and write recommendations (3 hours)"
                ],
                "resources": [
                    {"name": "Udacity A/B Testing Course", "type": "course", "url": "https://udacity.com/course/ab-testing--ud257", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "Evan Miller A/B Testing Calculator", "type": "tutorial", "url": "https://evanmiller.org/ab-testing/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            },
            {
                "focus_skill": "Data Storytelling & Business Communication",
                "task_list": [
                    "Structure a data narrative: context, insight, recommendation, impact (2 hours)",
                    "Build a stakeholder-ready presentation from a data analysis (2 hours)",
                    "Practice presenting findings: 5-minute data story with visuals (3 hours)"
                ],
                "resources": [
                    {"name": "Storytelling with Data by Cole Nussbaumer", "type": "book", "url": "https://storytellingwithdata.com/", "cost": "$30", "time_estimate": "6 hours"},
                    {"name": "Google Data Analytics Certificate", "type": "course", "url": "https://coursera.org/professional-certificates/google-data-analytics", "cost": "Free to audit", "time_estimate": "10 hours"}
                ]
            }
        ]
        mastery = [
            {
                "focus_skill": "Advanced SQL & ETL Pipelines",
                "task_list": [
                    "Advanced SQL: window functions, CTEs, recursive queries, query optimisation (2 hours)",
                    "ETL concepts: extract data from APIs, transform with Python, load to DB (2 hours)",
                    "Build an automated data pipeline with Python + SQL (3 hours)"
                ],
                "resources": [
                    {"name": "LeetCode SQL Problems", "type": "practice", "url": "https://leetcode.com/problemset/database/", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "DataCamp SQL Track", "type": "course", "url": "https://datacamp.com/tracks/sql-fundamentals", "cost": "$25/mo", "time_estimate": "6 hours"}
                ]
            },
            {
                "focus_skill": "Intro to Machine Learning for Analysts",
                "task_list": [
                    "Regression and classification basics with scikit-learn (2 hours)",
                    "Clustering (K-Means) and dimensionality reduction (PCA) (2 hours)",
                    "Apply ML to a business problem: customer segmentation or churn prediction (3 hours)"
                ],
                "resources": [
                    {"name": "Kaggle Intro to ML", "type": "course", "url": "https://kaggle.com/learn/intro-to-machine-learning", "cost": "Free", "time_estimate": "4 hours"},
                    {"name": "Scikit-learn Tutorials", "type": "documentation", "url": "https://scikit-learn.org/stable/tutorial/", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Data Analyst Portfolio & Case Studies",
                "task_list": [
                    "Complete 2-3 end-to-end analysis projects with write-ups (3 hours)",
                    "Create a portfolio on GitHub/Notion with dashboards and insights (2 hours)",
                    "Write Medium/blog posts explaining your analysis process (2 hours)"
                ],
                "resources": [
                    {"name": "Kaggle Datasets", "type": "practice", "url": "https://kaggle.com/datasets", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "Tableau Public Gallery", "type": "tutorial", "url": "https://public.tableau.com/app/discover", "cost": "Free", "time_estimate": "2 hours"}
                ]
            },
            {
                "focus_skill": "Data Analyst Interview Preparation",
                "task_list": [
                    "SQL interview questions: practice 20+ LeetCode/HackerRank SQL problems (2 hours)",
                    "Case study interviews: analyse a dataset and present findings in 30 min (2 hours)",
                    "Behavioral interviews: STAR format, salary negotiation (2 hours)"
                ],
                "resources": [
                    {"name": "DataLemur SQL Interview Questions", "type": "practice", "url": "https://datalemur.com/", "cost": "Free", "time_estimate": "5 hours"},
                    {"name": "Glassdoor Data Analyst Questions", "type": "tutorial", "url": "https://glassdoor.com", "cost": "Free", "time_estimate": "2 hours"}
                ]
            }
        ]
        projects = [
            {"name": "Sales Dashboard in Tableau/Power BI", "skills_demonstrated": ["SQL", "Data Viz", "Business Analysis"], "portfolio_value": "High"},
            {"name": "Customer Churn Analysis (Python + ML)", "skills_demonstrated": ["Pandas", "Scikit-learn", "Data Storytelling"], "portfolio_value": "Very High"},
            {"name": "A/B Test Analysis Report", "skills_demonstrated": ["Statistics", "Python", "Business Communication"], "portfolio_value": "High"}
        ]
        phase_descriptions = [
            "Master Excel, SQL, Python for data, and statistics fundamentals",
            "Build dashboards, run A/B tests, and communicate data insights",
            "Advanced SQL, intro ML, build portfolio, and prepare for interviews"
        ]

    # ── Career Re-entry into Tech ────────────────────────────────────────
    else:
        foundation = [
            {
                "focus_skill": "Tech Landscape & Career Direction",
                "task_list": [
                    "Overview of tech roles: front-end, back-end, data, AI, DevOps (2 hours)",
                    "Self-assessment: identify transferable skills from previous career (2 hours)",
                    "Research 10 job postings in your target area, list common requirements (2 hours)"
                ],
                "resources": [
                    {"name": "Roadmap.sh Career Paths", "type": "tutorial", "url": "https://roadmap.sh/", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "freeCodeCamp Career Guide", "type": "tutorial", "url": "https://freecodecamp.org/news/", "cost": "Free", "time_estimate": "2 hours"}
                ]
            },
            {
                "focus_skill": "Programming Fundamentals (Python)",
                "task_list": [
                    "Install Python, VS Code, set up first project (1 hour)",
                    "Python basics: variables, data types, if/else, loops, functions (3 hours)",
                    "Build a simple CLI project: calculator or to-do list (2 hours)"
                ],
                "resources": [
                    {"name": "Python Official Tutorial", "type": "documentation", "url": "https://docs.python.org/3/tutorial/", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "Automate the Boring Stuff with Python", "type": "book", "url": "https://automatetheboringstuff.com/", "cost": "Free", "time_estimate": "8 hours"}
                ]
            },
            {
                "focus_skill": "Git, GitHub & Developer Tools",
                "task_list": [
                    "Install Git, create GitHub account, set up SSH keys (1 hour)",
                    "Git basics: init, add, commit, push, pull, branching (2 hours)",
                    "Push 3 small practice projects to GitHub (2 hours)"
                ],
                "resources": [
                    {"name": "Git Official Docs", "type": "documentation", "url": "https://git-scm.com/doc", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "GitHub Skills", "type": "course", "url": "https://skills.github.com/", "cost": "Free", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Web Basics & Tech Communication",
                "task_list": [
                    "HTML/CSS fundamentals: structure, styling, responsiveness basics (2 hours)",
                    "How the internet works: HTTP, DNS, servers, APIs - conceptual overview (1 hour)",
                    "Practice tech communication: write a blog post about what you learned this week (1 hour)"
                ],
                "resources": [
                    {"name": "MDN Getting Started with the Web", "type": "documentation", "url": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "freeCodeCamp Responsive Web Design", "type": "course", "url": "https://freecodecamp.org/learn/2022/responsive-web-design/", "cost": "Free", "time_estimate": "5 hours"}
                ]
            }
        ]
        building = [
            {
                "focus_skill": "Career Gap Narrative & Confidence Building",
                "task_list": [
                    "Craft your career transition story: why tech, what you bring, where you aim (2 hours)",
                    "Identify 5 transferable skills and map them to tech roles (1 hour)",
                    "Join 2 tech communities: Discord, Reddit, Women Who Code, etc. (1 hour)"
                ],
                "resources": [
                    {"name": "Women Who Code", "type": "community", "url": "https://womenwhocode.com/", "cost": "Free", "time_estimate": "1 hour"},
                    {"name": "LinkedIn Career Transition Articles", "type": "tutorial", "url": "https://linkedin.com/learning/", "cost": "Free/$", "time_estimate": "2 hours"}
                ]
            },
            {
                "focus_skill": "Deepen Your Chosen Specialisation",
                "task_list": [
                    "Pick your track: Web Dev, Data, or AI and start the focused curriculum (3 hours)",
                    "Complete 1 guided project in your chosen area (2 hours)",
                    "Build a small portfolio piece demonstrating your new skills (2 hours)"
                ],
                "resources": [
                    {"name": "The Odin Project (Web)", "type": "course", "url": "https://theodinproject.com/", "cost": "Free", "time_estimate": "10 hours"},
                    {"name": "Kaggle Learn (Data/AI)", "type": "course", "url": "https://kaggle.com/learn", "cost": "Free", "time_estimate": "8 hours"}
                ]
            },
            {
                "focus_skill": "Projects & Practical Experience",
                "task_list": [
                    "Build a project that solves a real problem you care about (3 hours)",
                    "Document the project with a clear README and screenshots (1 hour)",
                    "Deploy the project online (Vercel, Render, or GitHub Pages) (2 hours)"
                ],
                "resources": [
                    {"name": "GitHub Pages", "type": "documentation", "url": "https://pages.github.com/", "cost": "Free", "time_estimate": "1 hour"},
                    {"name": "Render.com Free Tier", "type": "documentation", "url": "https://render.com/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            },
            {
                "focus_skill": "Networking & Online Presence",
                "task_list": [
                    "Optimise LinkedIn: headline, summary, skills, featured projects (2 hours)",
                    "Contribute to 1 open-source beginner-friendly project (2 hours)",
                    "Attend 1 virtual tech meetup or conference (1 hour)"
                ],
                "resources": [
                    {"name": "Good First Issues", "type": "practice", "url": "https://goodfirstissues.com/", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "Meetup.com Tech Events", "type": "community", "url": "https://meetup.com/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            }
        ]
        mastery = [
            {
                "focus_skill": "Advanced Project & Portfolio Polish",
                "task_list": [
                    "Build 1 capstone project combining multiple skills (3 hours)",
                    "Create a personal website/portfolio showcasing all projects (2 hours)",
                    "Get code review feedback from community or mentor (1 hour)"
                ],
                "resources": [
                    {"name": "Portfolio Inspiration", "type": "tutorial", "url": "https://github.com/topics/portfolio", "cost": "Free", "time_estimate": "2 hours"},
                    {"name": "Code Review Stack Exchange", "type": "community", "url": "https://codereview.stackexchange.com/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            },
            {
                "focus_skill": "Resume, Cover Letter & Job Applications",
                "task_list": [
                    "Write a tech-focused resume highlighting projects and transferable skills (2 hours)",
                    "Customise cover letter template for 3 target job types (1 hour)",
                    "Apply to 5 entry-level or returner-friendly positions (2 hours)"
                ],
                "resources": [
                    {"name": "Tech Resume Guide", "type": "tutorial", "url": "https://resumeworded.com/", "cost": "Free/$", "time_estimate": "2 hours"},
                    {"name": "Return-to-Work Programs List", "type": "tutorial", "url": "https://rewritingthecode.org/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            },
            {
                "focus_skill": "Interview Preparation",
                "task_list": [
                    "Behavioral interview prep: STAR format for career transition stories (2 hours)",
                    "Technical interview basics: problem-solving walkthroughs (2 hours)",
                    "Mock interview practice with a friend or on Pramp.com (2 hours)"
                ],
                "resources": [
                    {"name": "Pramp Free Mock Interviews", "type": "practice", "url": "https://pramp.com/", "cost": "Free", "time_estimate": "3 hours"},
                    {"name": "Interview.io", "type": "practice", "url": "https://interviewing.io/", "cost": "Free/$", "time_estimate": "3 hours"}
                ]
            },
            {
                "focus_skill": "Salary Negotiation & Career Growth Plan",
                "task_list": [
                    "Research salary ranges for your target role on Levels.fyi / Glassdoor (1 hour)",
                    "Practice negotiation scripts: initial offer, counter, benefits (2 hours)",
                    "Create a 6-month post-hire growth plan for continuous learning (1 hour)"
                ],
                "resources": [
                    {"name": "Levels.fyi Salary Data", "type": "tutorial", "url": "https://levels.fyi", "cost": "Free", "time_estimate": "1 hour"},
                    {"name": "Salary Negotiation Guide", "type": "tutorial", "url": "https://www.kalzumeus.com/2012/01/23/salary-negotiation/", "cost": "Free", "time_estimate": "1 hour"}
                ]
            }
        ]
        projects = [
            {"name": "Personal Portfolio Website", "skills_demonstrated": ["HTML/CSS", "Git", "Deployment"], "portfolio_value": "High"},
            {"name": "Project in Chosen Specialisation", "skills_demonstrated": ["Specialisation skills", "Problem solving"], "portfolio_value": "Very High"},
            {"name": "Open Source Contribution", "skills_demonstrated": ["Git", "Collaboration", "Code reading"], "portfolio_value": "High"}
        ]
        phase_descriptions = [
            "Explore tech roles, learn programming fundamentals, and set up developer tools",
            "Build confidence, deepen your specialisation, and create first projects",
            "Polish portfolio, prepare for interviews, and start applying"
        ]

    return {
        "foundation": foundation,
        "building": building,
        "mastery": mastery,
        "projects": projects,
        "phase_descriptions": phase_descriptions
    }


def get_fallback_roadmap(
    role: str,
    weekly_hours: int,
    deadline_weeks: Optional[int]
) -> Dict[str, Any]:
    """Generate a role-specific fallback roadmap if LLM fails."""

    # Calculate weeks
    if deadline_weeks:
        total_weeks = deadline_weeks
    else:
        total_hours_needed = 200
        total_weeks = max(12, min(52, total_hours_needed // weekly_hours))

    # Divide into phases
    foundation_weeks = total_weeks // 3
    building_weeks = total_weeks // 3
    mastery_weeks = total_weeks - foundation_weeks - building_weeks

    # Get role-specific skills
    role_data = _get_role_specific_skills(role)
    foundation_skills = role_data["foundation"]
    building_skills = role_data["building"]
    mastery_skills = role_data["mastery"]
    projects = role_data["projects"]
    phase_descriptions = role_data["phase_descriptions"]

    # Build phases with calculated weeks
    def create_weeks(skills_list, start_week_number):
        weeks_data = []
        week_num = start_week_number
        for skill in skills_list:
            weeks_data.append({
                "week_number": week_num,
                "focus_skill": skill["focus_skill"],
                "tasks": skill["task_list"],
                "milestone": f"Milestone: Complete all {skill['focus_skill']} learning",
                "success_metric": "All tasks completed + 1 hands-on project",
                "resources": skill["resources"]
            })
            week_num += 1
        return weeks_data

    phases = [
        {
            "phase_name": "Phase 1: Foundation",
            "phase_description": phase_descriptions[0],
            "weeks": create_weeks(foundation_skills, 1)
        },
        {
            "phase_name": "Phase 2: Application",
            "phase_description": phase_descriptions[1],
            "weeks": create_weeks(building_skills, 1 + foundation_weeks)
        },
        {
            "phase_name": "Phase 3: Mastery & Interview Prep",
            "phase_description": phase_descriptions[2],
            "weeks": create_weeks(mastery_skills, 1 + foundation_weeks + building_weeks)
        }
    ]

    # Add week ranges to projects
    for i, project in enumerate(projects):
        if i == 0:
            project["week_range"] = f"Weeks 1-{foundation_weeks}"
        elif i == 1:
            project["week_range"] = f"Weeks {foundation_weeks+1}-{foundation_weeks+building_weeks}"
        else:
            project["week_range"] = f"Weeks {foundation_weeks+building_weeks+1}-{total_weeks}"

    return {
        "total_weeks": total_weeks,
        "phases": phases,
        "recommended_projects": projects,
        "interview_prep_weeks": list(range(total_weeks - 3, total_weeks + 1)),
        "buffer_weeks": 2
    }
