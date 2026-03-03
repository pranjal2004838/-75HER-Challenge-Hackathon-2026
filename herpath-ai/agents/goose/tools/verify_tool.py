"""
VerifyTool - Response Verification Tool
=======================================

A Goose-style tool for verifying AI-generated responses.
Ensures responses meet quality standards before delivery.

Features:
- Content length validation
- Toxicity/safety checks
- Relevance scoring
- JSON structure validation
- Response cleaning and formatting
"""

import logging
import re
from typing import Any, Dict, List, Optional

from ..toolkit import Tool, ToolResult, ToolParameter

logger = logging.getLogger(__name__)


class VerifyTool(Tool):
    """
    Tool for verifying and validating AI responses.
    
    Checks responses for:
    - Minimum/maximum length requirements
    - Prohibited content patterns
    - Required content patterns
    - JSON structure validity
    - General quality metrics
    
    Usage:
        tool = VerifyTool(min_length=50, max_length=5000)
        result = tool.execute(
            content="Response text to verify",
            check_json=False
        )
    """
    
    def __init__(
        self,
        min_length: int = 20,
        max_length: int = 50000,
        prohibited_patterns: Optional[List[str]] = None,
        required_patterns: Optional[List[str]] = None
    ):
        """
        Initialize the verify tool.
        
        Args:
            min_length: Minimum acceptable content length
            max_length: Maximum acceptable content length
            prohibited_patterns: Regex patterns that should NOT appear
            required_patterns: Regex patterns that MUST appear
        """
        self.min_length = min_length
        self.max_length = max_length
        self.prohibited_patterns = prohibited_patterns or []
        self.required_patterns = required_patterns or []
        
        # Default prohibited patterns (safety)
        self._default_prohibited = [
            r'(?i)\b(api[_-]?key|password|secret)[:\s]*[\'"]?[a-zA-Z0-9]{10,}',
            r'(?i)I\s+(cannot|can\'t|won\'t|refuse\s+to)',  # AI refusals
        ]
    
    @property
    def name(self) -> str:
        return "verify_response"
    
    @property
    def description(self) -> str:
        return "Verify that an AI response meets quality and safety standards."
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="content",
                description="The content to verify",
                param_type="string",
                required=True
            ),
            ToolParameter(
                name="check_json",
                description="Whether to validate JSON structure",
                param_type="boolean",
                required=False,
                default=False
            ),
            ToolParameter(
                name="expected_fields",
                description="JSON fields that must be present",
                param_type="array",
                required=False
            )
        ]
    
    def execute(self, **kwargs) -> ToolResult:
        """
        Verify content meets quality standards.
        
        Args:
            content: Content to verify
            check_json: Whether to validate as JSON
            expected_fields: Required JSON fields
            
        Returns:
            ToolResult with verification status and cleaned content
        """
        content = kwargs.get("content")
        check_json = kwargs.get("check_json", False)
        expected_fields = kwargs.get("expected_fields", [])
        
        if content is None:
            return ToolResult.failure("No content provided for verification")
        
        issues = []
        warnings = []
        
        # Handle different content types
        if isinstance(content, dict):
            # It's already structured data
            if check_json and expected_fields:
                missing = [f for f in expected_fields if f not in content]
                if missing:
                    issues.append(f"Missing required fields: {missing}")
            
            if not issues:
                return ToolResult.success(
                    content,
                    verified=True,
                    content_type="json"
                )
            else:
                return ToolResult.failure(
                    f"Verification failed: {'; '.join(issues)}",
                    issues=issues
                )
        
        if isinstance(content, list):
            # It's a list, verify it's not empty
            if len(content) == 0:
                return ToolResult.failure("Content is an empty list")
            
            return ToolResult.success(
                content,
                verified=True,
                content_type="list"
            )
        
        # Convert to string for text verification
        text = str(content)
        
        # Length checks
        if len(text) < self.min_length:
            issues.append(f"Content too short ({len(text)} < {self.min_length} chars)")
        
        if len(text) > self.max_length:
            warnings.append(f"Content very long ({len(text)} > {self.max_length} chars)")
            # Truncate if needed
            text = text[:self.max_length] + "..."
        
        # Prohibited patterns
        for pattern in self._default_prohibited + self.prohibited_patterns:
            if re.search(pattern, text):
                # Sanitize by removing matched content
                text = re.sub(pattern, "[REDACTED]", text)
                warnings.append(f"Removed prohibited pattern match")
        
        # Required patterns
        for pattern in self.required_patterns:
            if not re.search(pattern, text):
                warnings.append(f"Missing expected pattern: {pattern}")
        
        # JSON validation if requested
        if check_json:
            import json
            try:
                parsed = json.loads(text)
                if expected_fields:
                    missing = [f for f in expected_fields if f not in parsed]
                    if missing:
                        issues.append(f"Missing required JSON fields: {missing}")
                
                if not issues:
                    return ToolResult.success(
                        parsed,
                        verified=True,
                        content_type="json",
                        warnings=warnings
                    )
            except json.JSONDecodeError:
                issues.append("Content is not valid JSON")
        
        # Return result
        if issues:
            return ToolResult.failure(
                f"Verification failed: {'; '.join(issues)}",
                issues=issues,
                warnings=warnings
            )
        
        # Clean and return
        cleaned = self._clean_content(text)
        
        return ToolResult.success(
            cleaned,
            verified=True,
            content_type="text",
            original_length=len(str(content)),
            cleaned_length=len(cleaned),
            warnings=warnings if warnings else None
        )
    
    def _clean_content(self, text: str) -> str:
        """Clean and format content."""
        if not text:
            return text
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\n{3,}', '\n\n', text)
        cleaned = re.sub(r' {2,}', ' ', cleaned)
        
        # Trim
        cleaned = cleaned.strip()
        
        return cleaned


class ResponseQualityChecker:
    """
    Advanced quality checker for AI responses.
    
    Provides scoring and detailed quality metrics.
    """
    
    @staticmethod
    def score_response(
        content: str,
        expected_topics: Optional[List[str]] = None,
        min_sentences: int = 2
    ) -> Dict[str, Any]:
        """
        Score a response on multiple quality dimensions.
        
        Args:
            content: Response content to score
            expected_topics: Topics that should be mentioned
            min_sentences: Minimum expected sentences
            
        Returns:
            Dict with scores and feedback
        """
        scores = {
            "length_score": 0,
            "structure_score": 0,
            "relevance_score": 0,
            "overall_score": 0
        }
        feedback = []
        
        if not content:
            return {"scores": scores, "feedback": ["No content provided"], "passed": False}
        
        # Length scoring
        content_len = len(content)
        if content_len < 50:
            scores["length_score"] = 0.2
            feedback.append("Response is very short")
        elif content_len < 200:
            scores["length_score"] = 0.5
            feedback.append("Response could be more detailed")
        elif content_len < 2000:
            scores["length_score"] = 1.0
        else:
            scores["length_score"] = 0.9
            feedback.append("Response is quite long")
        
        # Structure scoring
        sentences = len(re.findall(r'[.!?]+', content))
        paragraphs = len(content.split('\n\n'))
        
        if sentences >= min_sentences:
            scores["structure_score"] = min(1.0, sentences / 10)
        else:
            scores["structure_score"] = 0.3
            feedback.append(f"Expected at least {min_sentences} sentences")
        
        if paragraphs > 1:
            scores["structure_score"] = min(1.0, scores["structure_score"] + 0.2)
        
        # Relevance scoring
        if expected_topics:
            matches = sum(
                1 for topic in expected_topics
                if topic.lower() in content.lower()
            )
            scores["relevance_score"] = matches / len(expected_topics)
            if scores["relevance_score"] < 0.5:
                feedback.append("Response may not cover expected topics")
        else:
            scores["relevance_score"] = 0.7  # Default if no topics specified
        
        # Overall score
        scores["overall_score"] = (
            scores["length_score"] * 0.3 +
            scores["structure_score"] * 0.3 +
            scores["relevance_score"] * 0.4
        )
        
        passed = scores["overall_score"] >= 0.5
        
        return {
            "scores": scores,
            "feedback": feedback,
            "passed": passed
        }
