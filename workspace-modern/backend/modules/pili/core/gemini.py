"""
Gemini AI Service - External API Integration
Enterprise-grade with retry logic, rate limiting, and error handling
Following python-patterns and clean-code skills
"""
import logging
from typing import Optional
import asyncio
from datetime import datetime, timedelta

import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from ..config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GeminiService:
    """
    Gemini AI service with enterprise features:
    - Retry logic with exponential backoff
    - Rate limiting
    - Error handling
    - Logging
    - Metrics tracking
    
    Following python-patterns: Async for I/O-bound operations
    """
    
    def __init__(self):
        """Initialize Gemini AI service"""
        genai.configure(api_key=settings.gemini_api_key)
        
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config={
                "temperature": settings.gemini_temperature,
                "max_output_tokens": settings.gemini_max_tokens,
            }
        )
        
        # Rate limiting
        self._request_times: list[datetime] = []
        self._rate_limit_lock = asyncio.Lock()
        
        # Metrics
        self._total_requests = 0
        self._total_errors = 0
        self._total_tokens = 0
        
        logger.info(f"Gemini service initialized with model: {settings.gemini_model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    async def generate_response(self, prompt: str) -> str:
        """
        Generate AI response with retry logic.
        
        Args:
            prompt: Input prompt for AI
        
        Returns:
            Generated response text
        
        Raises:
            ValueError: If prompt is empty
            ConnectionError: If API is unreachable
            TimeoutError: If request times out
        
        Following python-patterns: Async def for I/O operations
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Rate limiting
        await self._check_rate_limit()
        
        try:
            self._total_requests += 1
            logger.debug(f"Generating response for prompt (length: {len(prompt)})")
            
            # Call Gemini API (async)
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            # Extract text
            if not response or not response.text:
                raise ValueError("Empty response from Gemini")
            
            result = response.text.strip()
            
            # Track metrics
            if hasattr(response, 'usage_metadata'):
                self._total_tokens += response.usage_metadata.total_token_count
            
            logger.info(f"Successfully generated response (length: {len(result)})")
            return result
            
        except Exception as e:
            self._total_errors += 1
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise
    
    async def _check_rate_limit(self):
        """
        Check and enforce rate limiting.
        
        Following clean-code: Single Responsibility
        """
        async with self._rate_limit_lock:
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=settings.rate_limit_window)
            
            # Remove old requests
            self._request_times = [
                t for t in self._request_times
                if t > window_start
            ]
            
            # Check limit
            if len(self._request_times) >= settings.rate_limit_requests:
                wait_time = (self._request_times[0] - window_start).total_seconds()
                logger.warning(f"Rate limit reached, waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time + 0.1)
            
            # Record this request
            self._request_times.append(now)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: dict
    ) -> dict:
        """
        Generate structured output using JSON mode.
        
        This is a placeholder for future implementation.
        Gemini supports structured output via function calling.
        """
        # TODO: Implement structured output
        raise NotImplementedError("Structured output not yet implemented")
    
    def get_metrics(self) -> dict:
        """
        Get service metrics.
        
        Following clean-code: Expose useful information
        """
        return {
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "total_tokens": self._total_tokens,
            "error_rate": self._total_errors / max(self._total_requests, 1),
            "current_rate_limit": len(self._request_times),
            "max_rate_limit": settings.rate_limit_requests,
            "model": settings.gemini_model
        }
    
    def reset_metrics(self):
        """Reset metrics counters"""
        self._total_requests = 0
        self._total_errors = 0
        self._total_tokens = 0
        logger.info("Metrics reset")
