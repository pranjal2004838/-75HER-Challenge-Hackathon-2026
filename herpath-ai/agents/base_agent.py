"""
Base agent class for HERPath AI.
Handles LLM communication with OpenAI or Anthropic.
"""

import json
import re
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

# Lazy imports for API clients
_openai_client = None
_anthropic_client = None


def get_openai_client():
    """Lazy load OpenAI client."""
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI
        import streamlit as st
        import os
        
        api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
        if api_key:
            _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def get_anthropic_client():
    """Lazy load Anthropic client."""
    global _anthropic_client
    if _anthropic_client is None:
        from anthropic import Anthropic
        import streamlit as st
        import os
        
        api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))
        if api_key:
            _anthropic_client = Anthropic(api_key=api_key)
    return _anthropic_client


class BaseAgent(ABC):
    """Base class for all HERPath AI agents."""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize agent.
        
        Args:
            provider: "openai" or "anthropic"
        """
        self.provider = provider
        self.model = "gpt-4-turbo-preview" if provider == "openai" else "claude-3-sonnet-20240229"
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Define the agent's system prompt/role."""
        pass
    
    @abstractmethod
    def build_prompt(self, **kwargs) -> str:
        """Build the user prompt with context injection."""
        pass
    
    def call_llm(self, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
        """
        Call LLM with the given prompt.
        
        Args:
            user_prompt: The user message/prompt
            temperature: Sampling temperature (0-1)
            
        Returns:
            LLM response text or None if error
        """
        try:
            if self.provider == "openai":
                return self._call_openai(user_prompt, temperature)
            else:
                return self._call_anthropic(user_prompt, temperature)
        except Exception as e:
            import streamlit as st
            st.error(f"LLM Error: {str(e)}")
            return None
    
    def _call_openai(self, user_prompt: str, temperature: float) -> Optional[str]:
        """Call OpenAI API."""
        client = get_openai_client()
        if not client:
            return None
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, user_prompt: str, temperature: float) -> Optional[str]:
        """Call Anthropic API."""
        client = get_anthropic_client()
        if not client:
            return None
        
        response = client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.content[0].text
    
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
