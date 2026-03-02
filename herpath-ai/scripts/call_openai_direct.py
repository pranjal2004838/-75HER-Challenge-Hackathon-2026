import sys, os, traceback
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.roadmap_agent import RoadmapAgent
agent = RoadmapAgent(provider='openai')
prompt = agent.build_prompt(role='SE', missing_skills=['Python'], priority_order=['Python'], deadline_weeks=None, weekly_hours=10, financial_constraint='Mixed', situation='', emotional_signals={})
print('Prompt length', len(prompt))
try:
    resp = agent._call_openai(prompt, 0.3)
    print('Response type:', type(resp))
    if isinstance(resp, str):
        print('Resp preview:', resp[:2000])
    else:
        print('Resp is None')
except Exception:
    traceback.print_exc()
