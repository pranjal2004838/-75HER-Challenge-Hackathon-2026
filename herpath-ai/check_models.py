import requests
import streamlit as st
import json

api_key = st.secrets.get("GEMINI_API_KEY")
url = f'https://generativelanguage.googleapis.com/v1beta/models?key={api_key}'

print(f"Fetching from: {url[:80]}...")
r = requests.get(url)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    data = r.json()
    print("\nAll available models:")
    print("-" * 60)
    for model in data.get('models', []):
        name = model['name']
        methods = model.get('supportedGenerationMethods', [])
        print(f"{name} -> {methods}")
else:
    print(f"Error: {r.text}")
