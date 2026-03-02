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
        return self.execute(
            role=role,
            missing_skills=missing_skills,
            priority_order=priority_order,
            deadline_weeks=deadline_weeks,
            weekly_hours=weekly_hours,
            financial_constraint=financial_constraint,
            situation=situation,
            emotional_signals=emotional_signals
        )


def get_fallback_roadmap(
    role: str,
    weekly_hours: int,
    deadline_weeks: Optional[int]
) -> Dict[str, Any]:
    """Generate a comprehensive fallback roadmap if LLM fails."""
    
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
    
    # Real skill progression for AI Engineer / Data roles
    foundation_skills = [
        {
            "focus_skill": "Python Basics & Environment Setup",
            "task_list": [
                "Install Python 3.11+ and set up development environment (2 hours)",
                "Learn Python syntax: variables, data types, operators (3 hours)",
                "Complete 20+ practice problems (2 hours)"
            ],
            "resources": [
                {"name": "Python Official Tutorial", "type": "documentation", "url": "https://docs.python.org/3/tutorial/", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "Codecademy Python Course", "type": "course", "url": "https://codecademy.com", "cost": "Free/$20/month", "time_estimate": "4 hours"},
                {"name": "LeetCode Easy Problems", "type": "practice", "url": "https://leetcode.com", "cost": "Free", "time_estimate": "3 hours"}
            ]
        },
        {
            "focus_skill": "Data Structures: Lists, Dicts, Sets & Time Complexity",
            "task_list": [
                "Study lists, dictionaries, tuples in Python (2 hours)",
                "Learn Big O notation and time complexity analysis (2 hours)",
                "Solve 15+ problems on Arrays/Strings (3 hours)"
            ],
            "resources": [
                {"name": "Data Structures Visualization", "type": "tutorial", "url": "https://visualgo.net/", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "LeetCode Array Problems", "type": "practice", "url": "https://leetcode.com/tag/array/", "cost": "Free/$", "time_estimate": "4 hours"},
                {"name": "GeeksforGeeks DSA Course", "type": "course", "url": "https://geeksforgeeks.org", "cost": "Free", "time_estimate": "3 hours"}
            ]
        },
        {
            "focus_skill": "Sorting, Searching & Problem-Solving",
            "task_list": [
                "Master sorting algorithms (merge, quick, heap sort) (2 hours)",
                "Learn binary search and two-pointer technique (2 hours)",
                "Solve 20+ coding problems implementing these concepts (3 hours)"
            ],
            "resources": [
                {"name": "Algorithms Course by MIT", "type": "video", "url": "https://ocw.mit.edu/courses/introduction-to-algorithms/", "cost": "Free", "time_estimate": "4 hours"},
                {"name": "LeetCode Medium Problems", "type": "practice", "url": "https://leetcode.com", "cost": "Free/$", "time_estimate": "5 hours"},
                {"name": "Neetcode.io", "type": "tutorial", "url": "https://neetcode.io/", "cost": "Free/$50", "time_estimate": "3 hours"}
            ]
        },
        {
            "focus_skill": "Recursion & Backtracking",
            "task_list": [
                "Understand recursive function design and call stack (2 hours)",
                "Master backtracking patterns (2 hours)",
                "Solve tree/graph recursion problems (3 hours)"
            ],
            "resources": [
                {"name": "Recursion Explained", "type": "tutorial", "url": "https://brilliant.org/courses/recursion/", "cost": "Free/$15/month", "time_estimate": "3 hours"},
                {"name": "LeetCode Tree & Backtracking", "type": "practice", "url": "https://leetcode.com", "cost": "$", "time_estimate": "4 hours"}
            ]
        }
    ]
    
    building_skills = [
        {
            "focus_skill": "Web Development Fundamentals (HTML, CSS, JavaScript)",
            "task_list": [
                "Learn HTML5 semantics and structure (1.5 hours)",
                "Learn CSS3: flexbox, grid, responsive design (2 hours)",
                "JavaScript basics: DOM manipulation, events (1.5 hours)"
            ],
            "resources": [
                {"name": "MDN Web Docs", "type": "documentation", "url": "https://developer.mozilla.org/", "cost": "Free", "time_estimate": "4 hours"},
                {"name": "freeCodeCamp Responsive Design", "type": "video", "url": "https://freecodecamp.org", "cost": "Free", "time_estimate": "4 hours"},
                {"name": "Codecademy JavaScript Course", "type": "course", "url": "https://codecademy.com", "cost": "Free/$20", "time_estimate": "5 hours"}
            ]
        },
        {
            "focus_skill": "Backend Development (Python Flask/FastAPI)",
            "task_list": [
                "Learn web frameworks: routing, requests, responses (1.5 hours)",
                "Build REST APIs with Flask or FastAPI (2 hours)",
                "Deploy to cloud platform (Heroku/Vercel) (1.5 hours)"
            ],
            "resources": [
                {"name": "Miguel Grinberg Flask Tutorial", "type": "tutorial", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world", "cost": "Free", "time_estimate": "4 hours"},
                {"name": "FastAPI Official Docs", "type": "documentation", "url": "https://fastapi.tiangolo.com/", "cost": "Free", "time_estimate": "3 hours"},
                {"name": "REST API Course", "type": "course", "url": "https://udemy.com", "cost": "$10-15", "time_estimate": "5 hours"}
            ]
        },
        {
            "focus_skill": "Databases (SQL & NoSQL)",
            "task_list": [
                "SQL fundamentals: SELECT, JOIN, GROUP BY (2 hours)",
                "Database design and normalization (1.5 hours)",
                "Work with PostgreSQL or MongoDB (1.5 hours)"
            ],
            "resources": [
                {"name": "SQL Tutorial by Mode Analytics", "type": "tutorial", "url": "https://mode.com/sql-tutorial/", "cost": "Free", "time_estimate": "3 hours"},
                {"name": "PostgreSQL Official Docs", "type": "documentation", "url": "https://postgresql.org/docs/", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "Udemy Database Design", "type": "course", "url": "https://udemy.com", "cost": "$10-15", "time_estimate": "5 hours"}
            ]
        },
        {
            "focus_skill": "APIs & Integration",
            "task_list": [
                "Design and build RESTful APIs (2 hours)",
                "Work with external APIs (payment, maps, auth) (1.5 hours)",
                "Testing and API documentation (1.5 hours)"
            ],
            "resources": [
                {"name": "REST API Best Practices", "type": "tutorial", "url": "https://restfulapi.net/", "cost": "Free", "time_estimate": "3 hours"},
                {"name": "Postman API Learning", "type": "tutorial", "url": "https://learning.postman.com/", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "API Design Course", "type": "course", "url": "https://udemy.com", "cost": "$10-15", "time_estimate": "4 hours"}
            ]
        }
    ]
    
    mastery_skills = [
        {
            "focus_skill": "System Design & Architecture",
            "task_list": [
                "Learn scalability concepts: sharding, caching, CDN (2 hours)",
                "Design patterns and microservices (1.5 hours)",
                "Analyze real-world system designs (1.5 hours)"
            ],
            "resources": [
                {"name": "System Design Primer", "type": "tutorial", "url": "https://github.com/donnemartin/system-design-primer", "cost": "Free", "time_estimate": "5 hours"},
                {"name": "Grokking the System Design Interview", "type": "course", "url": "https://designgurus.org/", "cost": "$50-100", "time_estimate": "8 hours"},
                {"name": "Designing Data-Intensive Applications", "type": "book", "url": "https://dataintensive.net/", "cost": "$50", "time_estimate": "10 hours"}
            ]
        },
        {
            "focus_skill": "CI/CD, DevOps & Cloud",
            "task_list": [
                "Learn Git workflows and GitHub (1.5 hours)",
                "Set up CI/CD pipelines (GitHub Actions, Jenkins) (1.5 hours)",
                "Deploy to AWS/GCP/Azure (1.5 hours)"
            ],
            "resources": [
                {"name": "Git Official Docs", "type": "documentation", "url": "https://git-scm.com/doc", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "GitHub Actions Guide", "type": "tutorial", "url": "https://github.com/features/actions", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "AWS Associate Developer Cert", "type": "course", "url": "https://aws.amazon.com/certification/", "cost": "$50-150", "time_estimate": "20 hours"}
            ]
        },
        {
            "focus_skill": "Portfolio Building & Demonstration",
            "task_list": [
                "Refine GitHub portfolio with 3-5 strong projects (2 hours)",
                "Create project documentation and READMEs (1 hour)",
                "Build personal website showcasing work (1 hour)"
            ],
            "resources": [
                {"name": "GitHub Portfolio Guide", "type": "tutorial", "url": "https://github.com/topics/portfolio", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "Portfolio Code Examples", "type": "practice", "url": "https://github.com", "cost": "Free", "time_estimate": "5 hours"}
            ]
        },
        {
            "focus_skill": "Interview Preparation & Negotiation",
            "task_list": [
                "Practice behavioral interview questions (1.5 hours)",
                "Mock technical interviews (2 hours)",
                "Learn salary negotiation and offer evaluation (1 hour)"
            ],
            "resources": [
                {"name": "Behavioral Interview Guide", "type": "tutorial", "url": "https://thebalancecareers.com/behavioral-interview-questions-and-answers-2061629", "cost": "Free", "time_estimate": "2 hours"},
                {"name": "LeetCode Mock Interviews", "type": "practice", "url": "https://leetcode.com", "cost": "$", "time_estimate": "8 hours"},
                {"name": "Salary Negotiation Guide", "type": "book", "url": "https://www.kalzumeus.com/2012/01/23/salary-negotiation/", "cost": "Free", "time_estimate": "1 hour"}
            ]
        }
    ]
    
    # Build phases with calculated weeks
    def create_weeks(skills_list, start_week_number):
        weeks_data = []
        week_num = start_week_number
        for i, skill in enumerate(skills_list[:len(skills_list)]):
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
            "phase_description": "Master Python fundamentals and core algorithmic concepts",
            "weeks": create_weeks(foundation_skills, 1)
        },
        {
            "phase_name": "Phase 2: Application",
            "phase_description": "Build real-world projects with web technologies and databases",
            "weeks": create_weeks(building_skills, 1 + foundation_weeks)
        },
        {
            "phase_name": "Phase 3: Mastery & Interview Prep",
            "phase_description": "Polish your portfolio and prepare for technical interviews",
            "weeks": create_weeks(mastery_skills, 1 + foundation_weeks + building_weeks)
        }
    ]
    
    return {
        "total_weeks": total_weeks,
        "phases": phases,
        "recommended_projects": [
            {
                "name": "CLI Todo App",
                "week_range": f"Weeks 1-{foundation_weeks}",
                "skills_demonstrated": ["Python basics", "Data structures", "File I/O"],
                "portfolio_value": "Medium"
            },
            {
                "name": "Blog/Portfolio Website",
                "week_range": f"Weeks {foundation_weeks+1}-{foundation_weeks+building_weeks//2}",
                "skills_demonstrated": ["HTML/CSS/JavaScript", "Python backend", "Database design"],
                "portfolio_value": "High"
            },
            {
                "name": "Full-Stack Project (Social App, E-Commerce, etc)",
                "week_range": f"Weeks {foundation_weeks+building_weeks//2+1}-{foundation_weeks+building_weeks}",
                "skills_demonstrated": ["Full stack development", "APIs", "Deployment"],
                "portfolio_value": "Very High"
            }
        ],
        "interview_prep_weeks": list(range(total_weeks - 3, total_weeks + 1)),
        "buffer_weeks": 2
    }
