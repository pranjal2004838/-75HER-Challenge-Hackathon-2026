# Contributing to HERPath AI

We welcome contributions from the community! This guide explains how to contribute code, documentation, and ideas.

---

## Code of Conduct

This project is dedicated to supporting women in tech. All contributors must:

- Treat others with respect and kindness
- Be inclusive of diverse backgrounds and experiences
- Provide constructive feedback
- Focus on the mission: helping women stay in and thrive in tech

---

## How to Contribute

### 1. **Report Bugs**

Found a bug? Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)

**Example:**
```
Title: Coach responds with generic advice for "feeling stuck" mode

Description:
When I ask the coach "I'm feeling imposter syndrome", the response 
doesn't mention my specific goal (AI Engineer) or reference my progress.

Expected: Personalized response mentioning my role and milestone.
Actual: Generic encouragement detached from my context.

Environment: Streamlit 1.28, Python 3.14
```

### 2. **Suggest Features**

Have an idea? Open an issue with:
- Clear description of feature
- Use case and user benefit
- Rough implementation idea (optional)

**Example:**
```
Title: Add LinkedIn profile builder based on completed projects

Description:
Users completing projects should get templates for writing LinkedIn posts
about their learning journey. This builds their professional brand.

Benefit: Helps women re-entering tech make themselves visible to recruiters.
```

### 3. **Fix Code**

Want to fix a bug or add a feature?

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/-75HER-Challenge-Hackathon-2026.git
   cd -75HER-Challenge-Hackathon-2026/herpath-ai
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b fix/bug-name
   # or
   git checkout -b feature/feature-name
   ```

3. **Make your changes**
   - Follow code style (see below)
   - Add docstrings and type hints
   - Test locally: `streamlit run app.py`

4. **Commit with clear messages**
   ```bash
   git commit -m "fix: Coach now personalizes responses to user goal"
   git commit -m "feat: Add interview question generator"
   ```

5. **Push and open a Pull Request**
   ```bash
   git push origin feature/feature-name
   ```
   Go to GitHub and click "Create Pull Request"

6. **Wait for review**
   - We review within 48 hours
   - Address feedback and update PR
   - Once approved, merge to main

---

## Code Style

### Python

- **Format:** Black (80-char lines)
  ```bash
  pip install black
  black .
  ```

- **Type hints:** Always add (required for new code)
  ```python
  def analyze(role: str, level: str) -> Dict[str, Any]:
      """Analyze user skill gaps."""
      pass
  ```

- **Docstrings:** Google style
  ```python
  def generate_roadmap(
      role: str,
      level: str,
      weeks: int
  ) -> Dict[str, Any]:
      """Generate a personalized learning roadmap.
      
      Args:
          role: Target career role (e.g., "AI Engineer")
          level: Current skill level (Beginner/Intermediate/Advanced)
          weeks: Weeks available to learn
          
      Returns:
          Dictionary with phases, tasks, and resources.
          
      Raises:
          ValueError: If role is not supported
      """
      pass
  ```

- **Comments:** Only for complex logic
  ```python
  # Exponential backoff: 1s, 2s, 4s, 8s...
  wait_time = 2 ** retry_count
  ```

- **Imports:** Sorted and organized
  ```python
  # Standard library
  import json
  from typing import Dict, List, Optional
  
  # Third party
  import streamlit as st
  from pydantic import BaseModel
  
  # Local
  from agents.coach_agent import CoachAgent
  from database.firestore_client import FirestoreClient
  ```

### Commit Messages

Use conventional commits:

```
feat: Add new coach mode for career break narratives
fix: Coach now handles imposter syndrome keywords
docs: Update API documentation for SkillGapAgent
test: Add unit tests for rebalance rule engine
refactor: Simplify GooseAgent retry logic
chore: Update dependencies
```

---

## Testing

### Run Tests:

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_agents.py -v

# Single test
python -m pytest tests/test_agents.py::test_coach_emotional_detection -v
```

### Write Tests:

Create `tests/test_my_feature.py`:

```python
import pytest
from agents.coach_agent import CoachAgent

def test_coach_detects_imposter_syndrome():
    """Coach should detect imposter syndrome in user background."""
    coach = CoachAgent()
    
    user_state = {
        "name": "Sarah",
        "background_text": "I always feel like I don't belong in tech"
    }
    
    response = coach.chat(
        user_state=user_state,
        message="Help with imposter feelings",
        mode="feeling_stuck"
    )
    
    # Assertions
    assert "imposter" in response.lower() or "belong" in response.lower()
    assert len(response) > 100  # Not a throwaway answer
    assert "you belong" in response.lower() or "You belong" in response
```

### Coverage:

```bash
pip install pytest-cov
pytest --cov=agents --cov=utils tests/
```

Goal: >80% coverage for critical paths

---

## Documentation

### Add Docs:

1. **Code docstrings:** Required for all functions/classes
   ```python
   def my_function(x: int) -> str:
       """One-line summary.
       
       Longer description if needed.
       
       Args:
           x: Brief description
           
       Returns:
           Description of return value
       """
       pass
   ```

2. **README updates:** If adding major features
   ```markdown
   ## New Feature: Example
   
   What it does, why it matters.
   
   ```bash
   # Example usage
   ```
   ```

3. **API docs:** In `docs/API.md` if adding new agent/tool
   ```markdown
   ### MyNewAgent
   
   **Input:** {...}
   **Output:** {...}
   **Example:** {...}
   ```

---

## Pull Request Process

1. **Title:** Clear and descriptive
   ```
   Fix: Coach personalizes responses to user goal
   ```

2. **Description:** 
   ```markdown
   ## Changes
   - Coach now references user's target role in responses
   - Added emotional signal detection for imposter syndrome
   
   ## Testing
   - Tested with demo account (judge@herpath-demo.ai)
   - All unit tests pass: `pytest -v`
   
   ## Checklist
   - [x] Code follows style guide
   - [x] Added/updated tests
   - [x] Updated documentation
   - [x] No new warnings
   ```

3. **Review:** 
   - At least 1 maintainer approval required
   - Address feedback promptly
   - Keep branch up-to-date with main

---

## Development Setup

### Prerequisites:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Testing, linting tools
```

### Dev Dependencies (in `requirements-dev.txt`):
```
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

### Quick Test:
```bash
# Run linter
black herpath-ai/

# Type check
mypy herpath-ai/

# Unit tests
pytest herpath-ai/tests/ -v

# Run app
streamlit run herpath-ai/app.py
```

---

## Project Structure

```
herpath-ai/
├── agents/              # AI agents (coach, roadmap, etc.)
├── database/            # Firebase schemas and client
├── ui/                  # Streamlit UI components
├── utils/               # Utilities (logging, validation)
├── config/              # Configuration
├── docs/                # Documentation (API, Architecture, etc.)
├── tests/               # Unit tests
├── app.py               # Main Streamlit app
└── requirements.txt     # Dependencies
```

**Where to add your change?**
- New agent → `agents/`
- Database schema → `database/schema.py`
- UI screen → `ui/`
- Helper function → `utils/`

---

## Help Wanted

We're especially looking for contributions in:

- [ ] **UI/UX:** Improve Streamlit design and accessibility
- [ ] **Agent improvements:** Better coaching, more accurate roadmaps
- [ ] **Testing:** Add edge cases, integration tests
- [ ] **Documentation:** Improve readability, add examples
- [ ] **New role support:** AI Engineer → Add Web3 Engineer, Cloud Engineer, etc.
- [ ] **Emotional intelligence:** Better imposter syndrome detection
- [ ] **Mobile version:** Build React Native mobile app

---

## Questions?

- Open an issue labeled "question"
- Join our Discord (coming soon)
- Email: support@herpath.ai

---

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file in repo
- GitHub contributors page
- Every release notes

Thank you for helping women thrive in tech! 💜
