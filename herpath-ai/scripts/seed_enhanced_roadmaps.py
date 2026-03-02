import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import firebase_config
firebase_config.init_firebase()
from firebase_admin import firestore
import json
from datetime import datetime

db = firestore.client()

# Enhanced fallback roadmap with real skill names and resources
def create_enhanced_roadmap(uid):
    """Create a realistic tech career roadmap with real skills and resources."""
    return {
        "uid": uid,
        "is_active": True,
        "current_week": 1,
        "total_weeks": 12,
        "roadmap_version": datetime.utcnow(),
        "generated_at": datetime.utcnow(),
        "phases": [
            {
                "phase_name": "Phase 1: Foundation - Core Programming & Data Structures",
                "phase_description": "Master programming fundamentals, data structures, and algorithms to build a strong foundation",
                "weeks": [
                    {
                        "week_number": 1,
                        "focus_skill": "Python Basics & Environment Setup",
                        "milestone": "Set up dev environment and understand Python fundamentals",
                        "success_metric": "Write and run 5+ Python programs covering variables, loops, functions",
                        "tasks": [
                            "Complete Python basics course (3 hours) - freeCodeCamp YouTube or codecademy.com",
                            "Install Python, VS Code, and Git; configure environment (1 hour)",
                            "Write 3 small programs: calculator, to-do list, number guessing game (2 hours)"
                        ],
                        "resources": [
                            {"name": "Python for Everybody", "type": "course", "url": "https://www.py4e.com/", "cost": "Free", "time_estimate": "20 hours"},
                            {"name": "freeCodeCamp Python Basics", "type": "video", "url": "https://www.youtube.com/watch?v=rfscVS0vtik", "cost": "Free", "time_estimate": "4 hours"},
                            {"name": "LeetCode Easy Problems", "type": "practice", "url": "https://leetcode.com", "cost": "Free", "time_estimate": "2 hours/week"}
                        ]
                    },
                    {
                        "week_number": 2,
                        "focus_skill": "Data Structures: Lists, Dicts, Sets & Time Complexity",
                        "milestone": "Understand and implement core data structures",
                        "success_metric": "Solve 8+ problems using lists, dictionaries involving search/sort",
                        "tasks": [
                            "Learn arrays, lists, dictionaries, sets (2 hours) - InterviewBit or GeeksforGeeks",
                            "Understand Big O notation and time complexity (1 hour)",
                            "Solve 10 coding problems on each data structure (3 hours)"
                        ],
                        "resources": [
                            {"name": "Data Structures Course - Abdul Bari", "type": "video", "url": "https://www.youtube.com/watch?v=7FfJqPjSdqY", "cost": "Free", "time_estimate": "12 hours"},
                            {"name": "GeeksforGeeks Data Structures", "type": "documentation", "url": "https://www.geeksforgeeks.org/", "cost": "Free", "time_estimate": "self-paced"},
                            {"name": "HackerRank Tutorials", "type": "practice", "url": "https://www.hackerrank.com", "cost": "Free", "time_estimate": "2 hours/week"}
                        ]
                    },
                    {
                        "week_number": 3,
                        "focus_skill": "Sorting & Searching Algorithms",
                        "milestone": "Master and implement common algorithms",
                        "success_metric": "Implement bubble, merge, quicksort; binary search from scratch",
                        "tasks": [
                            "Learn sorting: bubble, merge, quick sort (2 hours)",
                            "Learn searching: linear, binary search and applications (1 hour)",
                            "Implement all algorithms without looking at solutions (2 hours)"
                        ],
                        "resources": [
                            {"name": "Sorting and Searching - GeeksforGeeks", "type": "article", "url": "https://www.geeksforgeeks.org/sorting-algorithms/", "cost": "Free", "time_estimate": "5 hours"},
                            {"name": "Coding Challenge - Sorting", "type": "practice", "url": "https://leetcode.com/tag/sorting/", "cost": "Free", "time_estimate": "3 hours"}
                        ]
                    },
                    {
                        "week_number": 4,
                        "focus_skill": "Recursion & Problem Solving Patterns",
                        "milestone": "Master recursive thinking and backtracking",
                        "success_metric": "Solve 5 recursion problems, 3 backtracking problems",
                        "tasks": [
                            "Understand recursion with visual examples (1.5 hours)",
                            "Learn backtracking: permutations, combinations, N-Queens (1.5 hours)",
                            "Solve problems: Fibonacci, factorial, permutations, N-Queens (3 hours)"
                        ],
                        "resources": [
                            {"name": "Recursion & Backtracking - CodeHelp", "type": "video", "url": "https://www.youtube.com/playlist", "cost": "Free", "time_estimate": "8 hours"},
                            {"name": "LeetCode Recursion Tag", "type": "practice", "url": "https://leetcode.com/tag/recursion/", "cost": "Free", "time_estimate": "2 hours/week"}
                        ]
                    }
                ]
            },
            {
                "phase_name": "Phase 2: Application - Web Development & Projects",
                "phase_description": "Build real applications using web frameworks and apply learned concepts",
                "weeks": [
                    {
                        "week_number": 5,
                        "focus_skill": "Web Development Fundamentals (HTML, CSS, JS)",
                        "milestone": "Build responsive static websites",
                        "success_metric": "Create 2 responsive websites using HTML/CSS/JavaScript",
                        "tasks": [
                            "Learn HTML5 structure and semantic markup (1 hour)",
                            "Master CSS layouts: flexbox, grid, responsive design (2 hours)",
                            "Learn JavaScript basics: DOM manipulation, events (2 hours)"
                        ],
                        "resources": [
                            {"name": "freeCodeCamp Web Development Bootcamp", "type": "video", "url": "https://www.youtube.com/watch?v=e9IIVzlOufM", "cost": "Free", "time_estimate": "40 hours"},
                            {"name": "MDN Web Docs", "type": "documentation", "url": "https://developer.mozilla.org/", "cost": "Free", "time_estimate": "reference"},
                            {"name": "Codepen Projects", "type": "project", "url": "https://codepen.io", "cost": "Free", "time_estimate": "ongoing"}
                        ]
                    },
                    {
                        "week_number": 6,
                        "focus_skill": "Backend Development (Python Flask/Django)",
                        "milestone": "Create first full-stack application",
                        "success_metric": "Deploy a Flask app with database and user authentication",
                        "tasks": [
                            "Learn Flask basics: routing, templates, static files (2 hours)",
                            "Database design and SQLAlchemy ORM (1.5 hours)",
                            "Implement user authentication and form handling (1.5 hours)"
                        ],
                        "resources": [
                            {"name": "Flask + Python Web Development", "type": "course", "url": "https://www.udemy.com/course/python-and-flask-by-example/", "cost": "One-time ($15-50)", "time_estimate": "30 hours"},
                            {"name": "Real Python Flask Guide", "type": "article", "url": "https://realpython.com/", "cost": "Free/Premium", "time_estimate": "8 hours"}
                        ]
                    },
                    {
                        "week_number": 7,
                        "focus_skill": "APIs & Integration (REST, JSON, External APIs)",
                        "milestone": "Build RESTful API and integrate third-party services",
                        "success_metric": "Create multi-endpoint API; integrate 2 external APIs successfully",
                        "tasks": [
                            "Understand RESTful API design principles (1 hour)",
                            "Build a multi-resource API with Flask (2 hours)",
                            "Integrate external APIs: weather, GitHub, payment (2 hours)"
                        ],
                        "resources": [
                            {"name": "Building REST APIs with Flask", "type": "article", "url": "https://realpython.com/flask-connexion-rest-api/", "cost": "Free", "time_estimate": "5 hours"},
                            {"name": "OpenWeather API & GitHub API Practice", "type": "practice", "url": "https://openweathermap.org/api", "cost": "Free", "time_estimate": "4 hours"}
                        ]
                    },
                    {
                        "week_number": 8,
                        "focus_skill": "Database Design & SQL Optimization",
                        "milestone": "Design normalized database schema for complex application",
                        "success_metric": "Implement database with relationships; optimize slow queries",
                        "tasks": [
                            "Learn SQL: JOINs, subqueries, aggregation (2 hours)",
                            "Database normalization and indexing (1 hour)",
                            "Query optimization and performance tuning (2 hours)"
                        ],
                        "resources": [
                            {"name": "SQL Tutorial for Interviews", "type": "video", "url": "https://www.youtube.com/watch?v=rwnjsZFQfP8", "cost": "Free", "time_estimate": "6 hours"},
                            {"name": "SQLZoo Interactive SQL", "type": "practice", "url": "https://sqlzoo.net/", "cost": "Free", "time_estimate": "ongoing"}
                        ]
                    }
                ]
            },
            {
                "phase_name": "Phase 3: Mastery - Advanced Topics & Interview Prep",
                "phase_description": "Polish projects, build portfolio, prepare for interviews",
                "weeks": [
                    {
                        "week_number": 9,
                        "focus_skill": "System Design & Architecture",
                        "milestone": "Design scalable system architecture",
                        "success_metric": "Design 2 systems: chat app, social media feed. Justify choices",
                        "tasks": [
                            "Learn design patterns and architectural principles (1.5 hours)",
                            "Study at-scale systems design (1.5 hours)",
                            "Design 2 real-world systems and justify trade-offs (2 hours)"
                        ],
                        "resources": [
                            {"name": "System Design Interview - Karanpratap", "type": "course", "url": "https://www.youtube.com/playlist", "cost": "Free", "time_estimate": "20 hours"},
                            {"name": "Grokking the System Design Interview", "type": "course", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "cost": "$39-199", "time_estimate": "25 hours"}
                        ]
                    },
                    {
                        "week_number": 10,
                        "focus_skill": "Testing, CI/CD & DevOps Basics",
                        "milestone": "Set up automated testing and deployment pipeline",
                        "success_metric": "Write unit + integration tests; set up GitHub Actions CI/CD",
                        "tasks": [
                            "Write unit tests and integration tests (pytest, unittest) (1.5 hours)",
                            "Basic CI/CD concepts and GitHub Actions (1 hour)",
                            "Deploy to cloud (Heroku, AWS free tier) (1.5 hours)"
                        ],
                        "resources": [
                            {"name": "Python Testing with pytest", "type": "article", "url": "https://docs.pytest.org/", "cost": "Free", "time_estimate": "4 hours"},
                            {"name": "GitHub Actions Workflow - Example Repo", "type": "guide", "url": "https://docs.github.com/en/actions", "cost": "Free", "time_estimate": "3 hours"}
                        ]
                    },
                    {
                        "week_number": 11,
                        "focus_skill": "Portfolio Polish & Real-World Projects",
                        "milestone": "Finalize 2-3 portfolio-ready projects",
                        "success_metric": "Deploy projects; clear README, modern UI, good code quality",
                        "tasks": [
                            "Refactor code: clean it up, document, optimize (2 hours)",
                            "Improve UI/UX with responsive design and accessibility (2 hours)",
                            "Deploy to live domain, configure DNS (1 hour)"
                        ],
                        "resources": [
                            {"name": "awesome-readme", "type": "guide", "url": "https://github.com/matiassingers/awesome-readme", "cost": "Free", "time_estimate": "2 hours"},
                            {"name": "Web Accessibility Guidelines", "type": "documentation", "url": "https://www.w3.org/WAI/WCAG21/quickref/", "cost": "Free", "time_estimate": "3 hours"}
                        ]
                    },
                    {
                        "week_number": 12,
                        "focus_skill": "Interview Preparation & Negotiation",
                        "milestone": "Practice behavioral and technical interviews",
                        "success_metric": "Complete 5 mock interviews; research companies",
                        "tasks": [
                            "Research companies and prepare company-specific questions (1 hour)",
                            "Practice behavioral interview: STAR method (1.5 hours)",
                            "Do 4 mock coding interviews with peers (3 hours)"
                        ],
                        "resources": [
                            {"name": "LeetCode Interview Questions", "type": "practice", "url": "https://leetcode.com/", "cost": "Free/Premium", "time_estimate": "4 hours/week"},
                            {"name": "Blind 75 LeetCode Questions", "type": "curated", "url": "https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions", "cost": "Free", "time_estimate": "40 hours"},
                            {"name": "Negotiation Tactics -- Levels.fyi", "type": "guide", "url": "https://www.levels.fyi/", "cost": "Free", "time_estimate": "2 hours"}
                        ]
                    }
                ]
            }
        ],
        "recommended_projects": [
            {
                "name": "Task Management Application",
                "week_range": "Weeks 5-7",
                "skills_demonstrated": ["Flask", "JavaScript", "Database Design", "REST APIs"],
                "portfolio_value": "high"
            },
            {
                "name": "Weather Dashboard with External API Integration",
                "week_range": "Week 7",
                "skills_demonstrated": ["API Integration", "Frontend", "Error Handling"],
                "portfolio_value": "medium"
            },
            {
                "name": "E-commerce or Social Media Clone",
                "week_range": "Weeks 6-9",
                "skills_demonstrated": ["Full-stack", "Database", "System Design", "Authentication"],
                "portfolio_value": "high"
            }
        ],
        "interview_prep_weeks": [11, 12],
        "buffer_weeks": 1,
        "notes": "Generated as seed data. After user authenticates via onboarding, regenerate with LLM for personalized roadmap."
    }

print("Creating enhanced roadmap seed data and removing old placeholders...")

# Get all docs from roadmaps collection
all_docs = list(db.collection('roadmaps').stream())
print(f"Found {len(all_docs)} roadmap documents to remove")

# Delete all old roadmaps
for doc in all_docs:
    db.collection('roadmaps').document(doc.id).delete()
    print(f"  Deleted: {doc.id}")

# Get a sample UID from existing roadmap (if any had docs linked)
sample_uid = "test_user_herpath_demo"  # Use demo UID for seed data

# Create and insert enhanced roadmap
enhanced = create_enhanced_roadmap(sample_uid)
db.collection('roadmaps').add(enhanced)
print(f"✓ Inserted enhanced roadmap for {sample_uid}")

# Delete old tasks as well
old_tasks = list(db.collection('tasks').stream())
print(f"\nFound {len(old_tasks)} task documents")
for doc in old_tasks:
    db.collection('tasks').document(doc.id).delete()
print(f"✓ Cleaned up old task documents")

print("\n✓ Firestore roadmap data regenerated with real skills and resources!")
print(f"Sample roadmap UID: {sample_uid}")
print(f"Total weeks: 12")
print(f"Phases: {len(enhanced['phases'])}")
