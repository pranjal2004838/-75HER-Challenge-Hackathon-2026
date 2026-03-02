import os, sys, traceback
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.roadmap_agent import RoadmapAgent, get_fallback_roadmap
from config import firebase_config
import streamlit as st

print('Initializing Firebase (noop)')
try:
    firebase_config.init_firebase()
    print('Firebase init ok')
except Exception as e:
    print('Firebase init error', e)

agent = RoadmapAgent(provider='openai')
inputs = dict(
    role='Software Engineer',
    missing_skills=['Python','Data Structures','Algorithms'],
    priority_order=['Python','Algorithms','System Design'],
    deadline_weeks=None,
    weekly_hours=10,
    financial_constraint='Mixed',
    situation='career pivot',
    emotional_signals={'anxiety_level':'low'}
)

print('\nBuilding prompt...')
prompt = agent.build_prompt(**inputs)
print('Prompt length:', len(prompt))

print('\nCalling LLM...')
try:
    raw = agent.call_llm(prompt, temperature=0.3)
    print('Raw response type:', type(raw))
    if isinstance(raw, str):
        print('Raw response preview:\n', raw[:2000])
    else:
        print('Raw response is None or non-string')
except Exception:
    traceback.print_exc()

print('\nAttempting to extract JSON...')
try:
    parsed = agent.extract_json(raw)
    print('Parsed JSON type:', type(parsed))
    if parsed is None:
        print('Parsed is None — falling back to fallback roadmap')
        fb = get_fallback_roadmap(inputs['role'], inputs['weekly_hours'], inputs['deadline_weeks'])
        print('Fallback roadmap total_weeks:', fb.get('total_weeks'))
    else:
        print('Parsed keys:', list(parsed.keys())[:10])
except Exception:
    traceback.print_exc()
