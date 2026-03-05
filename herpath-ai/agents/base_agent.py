"""
Base Agent - HERPath AI Agent Framework
=======================================

This module provides the base class for all HERPath AI agents.
It integrates with the Goose-style agentic framework for:
- Intelligent multi-step execution
- Automatic fallback on failures
- Tool orchestration
- Response validation

Architecture:
- BaseAgent: Abstract base with Goose integration
- Uses GeminiTool for LLM calls
- Uses VerifyTool for response validation
- Falls back gracefully when AI services fail

Inspired by Block's Goose Framework.
"""

import json
import logging
import re
import time
import os
import requests
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# Gemini API configuration cache
_gemini_api_key = None


def get_gemini_api_key() -> str:
    """
    Get Gemini API key from multiple sources with fallback.
    
    Priority:
    1. Streamlit secrets (production)
    2. Environment variable
    3. .env file (local development)
    4. Hardcoded key (last resort for demo)
    """
    global _gemini_api_key
    if _gemini_api_key is not None:
        return _gemini_api_key
    
    # Source 1: Streamlit secrets (production on Streamlit Cloud)
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY")
        if key and len(key) > 20:
            _gemini_api_key = key
            logger.info("Loaded GEMINI_API_KEY from Streamlit secrets")
            return _gemini_api_key
    except Exception as e:
        logger.debug(f"Streamlit secrets unavailable: {e}")
    
    # Source 2: Environment variable
    key = os.getenv("GEMINI_API_KEY")
    if key and len(key) > 20:
        _gemini_api_key = key
        logger.info("Loaded GEMINI_API_KEY from environment")
        return _gemini_api_key
    
    # Source 3: .env file (auto-loaded by dotenv)
    try:
        from dotenv import load_dotenv, find_dotenv
        dotenv_path = find_dotenv()
        if dotenv_path:
            load_dotenv(dotenv_path, override=False)
            key = os.getenv("GEMINI_API_KEY")
            if key and len(key) > 20:
                _gemini_api_key = key
                logger.info(f"Loaded GEMINI_API_KEY from {dotenv_path}")
                return _gemini_api_key
    except Exception as e:
        logger.debug(f"Failed to load from .env: {e}")
    
    # No hardcoded fallback - API key must come from config (secrets.toml or environment)
    logger.error("GEMINI_API_KEY not found in any configuration source!")
    logger.error("Ensure GEMINI_API_KEY is set in .streamlit/secrets.toml or GEMINI_API_KEY environment variable")
    return ""


# Import Goose components with fallback
_goose_available = False
try:
    from .goose import GooseAgent, Toolkit, AgentResult
    from .goose.tools import GeminiTool, VerifyTool
    from .goose.fallback import FallbackManager, get_fallback_manager
    _goose_available = True
except ImportError:
    logger.warning("Goose framework not available, using direct API calls")
    GooseAgent = None
    Toolkit = None
    AgentResult = None


class BaseAgent(ABC):
    """
    Base class for all HERPath AI agents.
    
    Integrates Goose-style agentic patterns with:
    - Automatic tool selection
    - Retry and fallback logic
    - Response validation
    - Graceful degradation
    
    Subclasses must implement:
    - system_prompt: The agent's role/persona
    - build_prompt: How to construct the user prompt
    """
    
    def __init__(self, provider: str = "gemini"):
        """
        Initialize the agent.
        
        Args:
            provider: LLM provider (currently only "gemini" supported)
        """
        self.provider = "gemini"
        self.model = "gemini-3-flash-preview"
        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Initialize Goose components if available
        self._goose_agent = None
        self._toolkit = None
        self._fallback_manager = None
        
        if _goose_available:
            try:
                self._toolkit = Toolkit([
                    GeminiTool(model=self.model),
                    VerifyTool()
                ])
                self._fallback_manager = get_fallback_manager()
                self._goose_agent = GooseAgent(
                    name=self.__class__.__name__,
                    toolkit=self._toolkit,
                    fallback_manager=self._fallback_manager,
                    max_steps=3,
                    timeout_seconds=45.0,
                    retry_on_failure=True,
                    max_retries=2
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Goose: {e}")
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Define the agent's system prompt/role."""
        pass
    
    @abstractmethod
    def build_prompt(self, **kwargs) -> str:
        """Build the user prompt with context injection."""
        pass
    
    def call_llm(
        self,
        user_prompt: str,
        temperature: float = 0.7,
        retries: int = 3
    ) -> Optional[str]:
        """
        Call LLM with Goose-style orchestration and fallback.
        
        Args:
            user_prompt: The user message/prompt
            temperature: Sampling temperature (0-2)
            retries: Number of retries on transient errors
            
        Returns:
            LLM response text, fallback response, or None
        """
        # Try Goose-style execution first
        if self._toolkit and self._toolkit.get("gemini_generate"):
            try:
                gemini_tool = self._toolkit.get("gemini_generate")
                result = gemini_tool.execute(
                    prompt=user_prompt,
                    system_prompt=self.system_prompt,
                    temperature=temperature,
                    extract_json=False
                )
                
                if result.is_success and result.data:
                    # Verify response if tool available
                    verify_tool = self._toolkit.get("verify_response")
                    if verify_tool:
                        verified = verify_tool.execute(content=result.data)
                        if verified.is_success:
                            return verified.data
                    return result.data
                    
            except Exception as e:
                logger.warning(f"Goose execution failed: {e}, falling back to direct API")
        
        # Fallback to direct API call
        return self._call_llm_direct(user_prompt, temperature, retries)
    
    def _call_llm_direct(
        self,
        user_prompt: str,
        temperature: float = 0.7,
        retries: int = 3
    ) -> Optional[str]:
        """Direct Gemini API call with retry logic."""
        last_error = None
        
        for attempt in range(retries):
            try:
                return self._call_gemini(user_prompt, temperature)
            except Exception as e:
                last_error = e
                error_str = str(e)
                
                # Check if retryable
                is_retryable = any(x in error_str.lower() for x in [
                    "500", "502", "503", "504",
                    "rate_limit", "timeout", "connection"
                ])
                
                if not is_retryable or attempt == retries - 1:
                    logger.error(f"LLM Error (attempt {attempt+1}/{retries}): {error_str}")
                    # Return fallback instead of None
                    return self._get_fallback_response()
                
                wait = 2 ** attempt
                logger.warning(f"LLM error, retrying in {wait}s: {error_str}")
                time.sleep(wait)
        
        return self._get_fallback_response()
    
    def _call_gemini(self, user_prompt: str, temperature: float) -> Optional[str]:
        """Direct Gemini API call via REST."""
        api_key = get_gemini_api_key()
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        url = f"{self.api_endpoint}/{self.model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"{self.system_prompt}\n\n{user_prompt}"}]}],
            "generationConfig": {
                "temperature": min(max(temperature, 0), 2),
                "maxOutputTokens": 16384
            }
        }
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        # Check for API key blacklist specifically
        if response.status_code == 403:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "")
                if "leaked" in error_msg.lower():
                    logger.critical(
                        "API KEY BLACKLISTED: Google detected this key as leaked. "
                        "Generate a new key at https://aistudio.google.com/apikey"
                    )
                    raise ValueError(
                        "API key is blacklisted (leaked). Generate a new key at "
                        "https://aistudio.google.com/apikey and update .streamlit/secrets.toml"
                    )
            except (ValueError) as ve:
                raise ve
            except Exception:
                pass
        
        response.raise_for_status()
        response_data = response.json()
        
        # Extract text
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            candidate = response_data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                if len(parts) > 0:
                    return parts[0].get("text", "")
        
        raise ValueError(f"Unexpected response format: {response_data}")
    
    def _get_fallback_response(self) -> Optional[str]:
        """Get a fallback text response when API fails."""
        if self._fallback_manager:
            agent_type = self._infer_agent_type()
            fallback = self._fallback_manager.get_fallback(
                agent_type=agent_type,
                mode="general"
            )
            return fallback.content if fallback else None
        
        # Hardcoded fallback for when manager isn't available
        return self._get_hardcoded_fallback()
    
    def _get_hardcoded_fallback(self) -> str:
        """Hardcoded fallback responses for maximum reliability."""
        agent_type = self._infer_agent_type()
        
        fallbacks = {
            "coach": "I'm here to support your learning journey. While I'm having a brief connectivity moment, here's what I know: consistent small steps lead to big progress. What specific challenge would you like to tackle? I'll help you break it down into actionable next steps.",
            "roadmap": "Your personalized roadmap is being prepared. A typical learning path includes: 1) Foundations (4-6 weeks), 2) Core Skills (6-8 weeks), 3) Advanced Topics (4-6 weeks), and 4) Interview Prep (4 weeks). We'll customize this based on your goals and timeline.",
            "skill_gap": "Based on career transition patterns, key areas to focus on typically include: technical fundamentals for your target role, practical project experience, and interview preparation. I'll provide a detailed analysis shortly.",
            "rebalance": "To optimize your learning pace, review your current progress and adjust weekly goals to match your available time. Consistency matters more than intensity."
        }
        
        return fallbacks.get(agent_type, fallbacks["coach"])
    
    def _infer_agent_type(self) -> str:
        """Infer agent type from class name."""
        class_name = self.__class__.__name__.lower()
        
        if "coach" in class_name:
            return "coach"
        elif "roadmap" in class_name:
            return "roadmap"
        elif "skill" in class_name or "gap" in class_name:
            return "skill_gap"
        elif "rebalance" in class_name:
            return "rebalance"
        
        return "coach"
    
    def extract_json(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from LLM response."""
        if not response:
            return None
        
        # Try direct JSON parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in code blocks
        json_patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response)
            for match in matches:
                try:
                    clean = match.strip()
                    if not clean.startswith('{'):
                        start = clean.find('{')
                        end = clean.rfind('}')
                        if start != -1 and end != -1:
                            clean = clean[start:end+1]
                    return json.loads(clean)
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def execute(self, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Execute the agent with given inputs.
        
        Returns:
            Parsed JSON output, fallback response, or None
        """
        try:
            prompt = self.build_prompt(**kwargs)
            response = self.call_llm(prompt)
            
            if response:
                parsed = self.extract_json(response)
                if parsed:
                    return parsed
            
            # Return fallback for this agent type
            return self._get_fallback_json()
            
        except Exception as e:
            logger.exception(f"Agent execution failed: {e}")
            return self._get_fallback_json()
    
    def _get_fallback_json(self) -> Optional[Dict[str, Any]]:
        """Get fallback JSON response."""
        if self._fallback_manager:
            agent_type = self._infer_agent_type()
            
            if agent_type == "roadmap":
                fallback = self._fallback_manager.get_roadmap_fallback(
                    goal="Technology Career",
                    weeks=26
                )
                return fallback.get("roadmap")
            
            fallback = self._fallback_manager.get_fallback(
                agent_type=agent_type,
                mode="default"
            )
            
            if isinstance(fallback.content, dict):
                return fallback.content
        
        return None
