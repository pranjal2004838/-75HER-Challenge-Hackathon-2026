import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from agents.base_agent import get_openai_client

client = get_openai_client()
if client:
    try:
        models = client.models.list()
        gpt_models = [m.id for m in models.data if 'gpt' in m.id.lower()]
        print('Available GPT models:')
        for m in sorted(gpt_models)[:20]:
            print(f'  - {m}')
    except Exception as e:
        print('Error listing models:', e)
else:
    print('No OpenAI client')
