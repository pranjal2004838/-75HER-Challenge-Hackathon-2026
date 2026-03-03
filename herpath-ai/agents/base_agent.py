"""
Base agent class for HERPath AI.
Handles LLM communication with Google Gemini API (REST).
"""

import json
import re
import time
import requests
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

# Gemini API configuration
_gemini_api_key = None


def get_gemini_api_key():
    """Get Gemini API key from environment or Streamlit secrets."""
    global _gemini_api_key
    if _gemini_api_key is None:
        import streamlit as st
        import os
        
        _gemini_api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    return _gemini_api_key


class BaseAgent(ABC):
    """Base class for all HERPath AI agents (Gemini-powered)."""
    
    def __init__(self, provider: str = "gemini"):
        """
        Initialize agent for Gemini.
        
        Args:
            provider: Currently only "gemini" is supported
        """
        self.provider = "gemini"  # Force Gemini
        self.model = "gemini-2.0-flash-exp"  # Latest available Gemini 2.0 Flash (experimental)
        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Define the agent's system prompt/role."""
        pass
    
    @abstractmethod
    def build_prompt(self, **kwargs) -> str:
        """Build the user prompt with context injection."""
        pass
    
    def call_llm(self, user_prompt: str, temperature: float = 0.7, retries: int = 3) -> Optional[str]:
        """
        Call Gemini API with retry logic to handle transient errors.
        
        Args:
            user_prompt: The user message/prompt
            temperature: Sampling temperature (0-1)
            retries: Number of retries on transient errors
            
        Returns:
            LLM response text or None if error
        """
        last_error = None
        for attempt in range(retries):
            try:
                return self._call_gemini(user_prompt, temperature)
            except Exception as e:
                last_error = e
                error_str = str(e)
                # Check if it's a retryable error (5xx, rate limit, timeout, connection)
                is_retryable = (
                    "500" in error_str or "502" in error_str or "503" in error_str or
                    "rate_limit" in error_str.lower() or "timeout" in error_str.lower() or
                    "connection" in error_str.lower()
                )
                if not is_retryable or attempt == retries - 1:
                    # Not retryable or last attempt; log and fail
                    import streamlit as st
                    st.error(f"LLM Error (attempt {attempt+1}/{retries}): {error_str}")
                    return None
                # Retryable; backoff and retry
                wait = 2 ** attempt  # exponential backoff: 1s, 2s, 4s
                import streamlit as st
                st.warning(f"LLM error (attempt {attempt+1}/{retries}), retrying in {wait}s: {error_str}")
                time.sleep(wait)
    
    def _call_gemini(self, user_prompt: str, temperature: float) -> Optional[str]:
        """Call Gemini API via REST."""
        api_key = get_gemini_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or Streamlit secrets")
        
        # Gemini API endpoint
        url = f"{self.api_endpoint}/{self.model}:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{self.system_prompt}\n\n{user_prompt}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": min(max(temperature, 0), 2),
                "maxOutputTokens": 16384
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.HTTPError as e:
            # Log the full response for debugging
            error_msg = f"Gemini API {response.status_code}: {response.text}"
            raise ValueError(error_msg)
        
        # Extract text from Gemini response
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            candidate = response_data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                if len(parts) > 0:
                    return parts[0].get("text", "")
        
        raise ValueError(f"Unexpected Gemini response format: {response_data}")
    
    def extract_json(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from LLM response."""
        if not response:
            return None
        
        # Try direct JSON parse
        try:
            return json.loads(response)
        except:
            pass
        
        # Try to find JSON in markdown code blocks
        json_patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response)
            for match in matches:
                try:
                    # Clean up the match
                    clean = match.strip()
                    if not clean.startswith('{'):
                        # Find the first { and last }
                        start = clean.find('{')
                        end = clean.rfind('}')
                        if start != -1 and end != -1:
                            clean = clean[start:end+1]
                    return json.loads(clean)
                except:
                    continue
        
        return None
    
    def execute(self, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Execute the agent with given inputs.
        
        Returns:
            Parsed JSON output or None
        """
        prompt = self.build_prompt(**kwargs)
        response = self.call_llm(prompt)
        return self.extract_json(response)
