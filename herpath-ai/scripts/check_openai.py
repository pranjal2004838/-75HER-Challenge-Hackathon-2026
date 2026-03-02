import traceback
import sys, os
# ensure project root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
print('--- OpenAI key diagnostic ---')
print('st.secrets keys:', list(st.secrets.keys()))
key = st.secrets.get('OPENAI_API_KEY')
print('OPENAI_API_KEY present:', bool(key))
if key:
    print('key length:', len(key))

try:
    # Try new OpenAI client (openai>=1.0)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        try:
            resp = client.models.list()
            print('OpenAI (new client) models.list succeeded. Models returned:', len(resp.data))
        except Exception:
            print('OpenAI (new client) models.list failed:')
            traceback.print_exc()
    except Exception:
        # Fallback to older openai usage
        import openai
        openai.api_key = key
        try:
            models = openai.Model.list()
            print('OpenAI (old client) Model.list succeeded. Models returned:', len(models.data))
        except Exception:
            print('OpenAI model.list failed:')
            traceback.print_exc()
except ImportError as e:
    print('openai package missing:', e)
