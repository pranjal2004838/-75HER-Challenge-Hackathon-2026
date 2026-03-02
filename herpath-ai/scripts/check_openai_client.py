import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from agents.base_agent import get_openai_client
print('st.secrets keys:', list(st.secrets.keys()))
client = get_openai_client()
print('openai client instance:', client)
if client:
    try:
        from openai import OpenAI
        print('OpenAI class available')
    except Exception as e:
        print('OpenAI import failed', e)
