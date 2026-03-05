"""
GeminiTool - Gemini API Integration Tool
========================================

A Goose-style tool for calling Google's Gemini API.
Handles all API communication, error handling, and response parsing.

Features:
- Configurable model selection
- Temperature and token limit controls
- Automatic retry with exponential backoff
- Response validation and parsing
- Comprehensive error handling
"""

import json
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional

import requests

from ..toolkit import Tool, ToolResult, ToolParameter

logger = logging.getLogger(__name__)


def _get_api_key() -> Optional[str]:
    """
    Get Gemini API key from multiple sources with fallback.
    
    Priority:
    1. Streamlit secrets (production on Streamlit Cloud)
    2. Environment variable 
    3. .env file (local development)
    4. Hardcoded fallback key
    """
    # Try Streamlit secrets first
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY")
        if key and len(key) > 20:
            logger.debug("Loaded GEMINI_API_KEY from Streamlit secrets")
            return key
    except Exception as e:
        logger.debug(f"Streamlit secrets unavailable: {type(e).__name__}")
    
    # Try environment variable
    key = os.getenv("GEMINI_API_KEY")
    if key and len(key) > 20:
        logger.debug("Loaded GEMINI_API_KEY from environment")
        return key
    
    # Try loading from .env file
    try:
        from dotenv import load_dotenv, find_dotenv
        dotenv_path = find_dotenv()
        if dotenv_path:
            load_dotenv(dotenv_path, override=False)
            key = os.getenv("GEMINI_API_KEY")
            if key and len(key) > 20:
                logger.debug(f"Loaded GEMINI_API_KEY from {dotenv_path}")
                return key
    except Exception as e:
        logger.debug(f"Failed to load .env: {e}")
    
    # Fallback to hardcoded key (from production secrets.toml)
    fallback_key = "AIzaSyAgCHTHi7rOuBm7Jp3o5DFAWgPY1Ah0ar8"
    if fallback_key and len(fallback_key) > 20:
        logger.warning("Using fallback GEMINI_API_KEY - ensure config is properly loaded")
        return fallback_key
    
    logger.error("GEMINI_API_KEY not found in any source!")
    return None


class GeminiTool(Tool):
    """
    Tool for generating content using Google Gemini API.
    
    This tool wraps the Gemini generateContent endpoint and provides:
    - Configurable prompts and system instructions
    - Temperature and output token controls
    - Retry logic for transient failures
    - Response parsing (text and JSON extraction)
    
    Usage:
        tool = GeminiTool(model="gemini-3-flash-preview")
        result = tool.execute(
            prompt="Explain machine learning",
            system_prompt="You are a helpful teacher",
            temperature=0.7
        )
    """
    
    def __init__(
        self,
        model: str = "gemini-3-flash-preview",
        api_endpoint: str = "https://generativelanguage.googleapis.com/v1beta/models",
        max_output_tokens: int = 16384,
        default_temperature: float = 0.7,
        timeout_seconds: float = 30.0,
        max_retries: int = 3
    ):
        """
        Initialize the Gemini tool.
        
        Args:
            model: Gemini model to use
            api_endpoint: Base API endpoint
            max_output_tokens: Maximum tokens in response
            default_temperature: Default sampling temperature
            timeout_seconds: Request timeout
            max_retries: Maximum retry attempts
        """
        self.model = model
        self.api_endpoint = api_endpoint
        self.max_output_tokens = max_output_tokens
        self.default_temperature = default_temperature
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
    
    @property
    def name(self) -> str:
        return "gemini_generate"
    
    @property
    def description(self) -> str:
        return "Generate text content using Google Gemini AI model. Supports system prompts, temperature control, and JSON extraction."
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="prompt",
                description="The main prompt/question for the AI",
                param_type="string",
                required=True
            ),
            ToolParameter(
                name="system_prompt",
                description="System instructions to guide AI behavior",
                param_type="string",
                required=False
            ),
            ToolParameter(
                name="temperature",
                description="Sampling temperature (0-2, higher = more creative)",
                param_type="number",
                required=False,
                default=0.7
            ),
            ToolParameter(
                name="extract_json",
                description="Whether to extract JSON from response",
                param_type="boolean",
                required=False,
                default=False
            )
        ]
    
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute Gemini API call.
        
        Args:
            prompt: Main prompt text
            system_prompt: Optional system instructions
            temperature: Optional temperature override
            extract_json: Whether to parse JSON from response
            
        Returns:
            ToolResult with generated text or parsed JSON
        """
        prompt = kwargs.get("prompt", "")
        system_prompt = kwargs.get("system_prompt", "")
        temperature = kwargs.get("temperature", self.default_temperature)
        extract_json = kwargs.get("extract_json", False)
        
        if not prompt:
            return ToolResult.failure("No prompt provided")
        
        # Get API key
        api_key = _get_api_key()
        if not api_key:
            logger.error("Gemini API key not found")
            return ToolResult.failure(
                "Gemini API key not configured. Please add GEMINI_API_KEY to secrets."
            )
        
        # Build request
        url = f"{self.api_endpoint}/{self.model}:generateContent?key={api_key}"
        
        # Combine system prompt and user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "contents": [
                {
                    "parts": [{"text": full_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": min(max(float(temperature), 0), 2),
                "maxOutputTokens": self.max_output_tokens
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        # Execute with retry
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self._make_request(url, headers, payload)
                text = self._extract_text(response)
                
                if text:
                    if extract_json:
                        json_data = self._extract_json(text)
                        if json_data:
                            return ToolResult.success(
                                json_data,
                                raw_text=text,
                                model=self.model
                            )
                        # Return text if JSON extraction failed but text exists
                        return ToolResult.success(
                            text,
                            json_extraction_failed=True,
                            model=self.model
                        )
                    
                    return ToolResult.success(text, model=self.model)
                
                return ToolResult.failure("Empty response from Gemini API")
                
            except requests.exceptions.Timeout:
                last_error = "Request timed out"
                logger.warning(f"Gemini timeout (attempt {attempt + 1})")
                
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {str(e)}"
                logger.warning(f"Gemini connection error (attempt {attempt + 1})")
                
            except requests.exceptions.HTTPError as e:
                error_msg = str(e)
                last_error = error_msg
                
                # Check if retryable
                if not self._is_retryable_http_error(e.response):
                    # Non-retryable error, return immediately
                    return ToolResult.failure(
                        f"Gemini API error: {error_msg}",
                        status_code=e.response.status_code if e.response else None
                    )
                
                logger.warning(f"Gemini HTTP error (attempt {attempt + 1}): {error_msg}")
                
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                logger.exception(f"Gemini unexpected error (attempt {attempt + 1})")
            
            # Exponential backoff
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        return ToolResult.failure(f"Gemini API failed after {self.max_retries} attempts: {last_error}")
    
    def _make_request(
        self,
        url: str,
        headers: Dict[str, str],
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make HTTP request to Gemini API."""
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout_seconds
        )
        response.raise_for_status()
        return response.json()
    
    def _extract_text(self, response: Dict[str, Any]) -> Optional[str]:
        """Extract text from Gemini API response."""
        try:
            if "candidates" in response and len(response["candidates"]) > 0:
                candidate = response["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0:
                        return parts[0].get("text", "")
        except (KeyError, IndexError, TypeError) as e:
            logger.warning(f"Failed to extract text from response: {e}")
        
        return None
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from response text."""
        if not text:
            return None
        
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try extracting from code blocks
        patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    clean = match.strip()
                    if not clean.startswith('{'):
                        start = clean.find('{')
                        end = clean.rfind('}')
                        if start != -1 and end != -1:
                            clean = clean[start:end + 1]
                    return json.loads(clean)
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def _is_retryable_http_error(self, response: Optional[requests.Response]) -> bool:
        """Check if HTTP error is retryable."""
        if response is None:
            return True
        
        # Retry on server errors and rate limits
        return response.status_code in (429, 500, 502, 503, 504)
