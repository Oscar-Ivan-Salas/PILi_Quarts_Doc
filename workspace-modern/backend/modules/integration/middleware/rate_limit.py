"""
Integration Module - Rate Limiting Middleware
Enterprise-grade rate limiting using sliding window algorithm
Following vulnerability-scanner and python-patterns skills
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import deque
import logging
import asyncio

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm.
    
    Features:
    - Per-IP rate limiting
    - Configurable limits
    - Sliding window algorithm
    - Automatic cleanup
    
    Following vulnerability-scanner: DoS protection
    Following python-patterns: Async middleware
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        cleanup_interval: int = 300  # 5 minutes
    ):
        """
        Initialize rate limiter.
        
        Args:
            app: FastAPI application
            requests_per_minute: Max requests per minute per IP
            cleanup_interval: Cleanup old entries interval (seconds)
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        
        # Store request timestamps per IP: {ip: deque([timestamp, ...])}
        self.request_history: Dict[str, deque] = {}
        
        # Lock for thread safety
        self._lock = asyncio.Lock()
        
        # Start cleanup task
        self._cleanup_interval = cleanup_interval
        self._cleanup_task = None
        
        logger.info(f"Rate limiter initialized: {requests_per_minute} req/min")
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request with rate limiting.
        
        Following python-patterns: Async middleware pattern
        """
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check rate limit
        is_allowed, retry_after = await self._check_rate_limit(client_ip)
        
        if not is_allowed:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "RateLimitExceeded",
                    "message": "Too many requests. Please try again later.",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = await self._get_remaining(client_ip)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(datetime.utcnow().timestamp()) + self.window_seconds)
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Get client IP from request.
        
        Following clean-code: Single responsibility
        """
        # Check X-Forwarded-For header (proxy/load balancer)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    async def _check_rate_limit(self, client_ip: str) -> tuple[bool, int]:
        """
        Check if request is within rate limit.
        
        Following vulnerability-scanner: Sliding window algorithm
        
        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        async with self._lock:
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=self.window_seconds)
            
            # Initialize history for new IP
            if client_ip not in self.request_history:
                self.request_history[client_ip] = deque()
            
            history = self.request_history[client_ip]
            
            # Remove old requests outside window
            while history and history[0] < window_start:
                history.popleft()
            
            # Check if limit exceeded
            if len(history) >= self.requests_per_minute:
                # Calculate retry after
                oldest_request = history[0]
                retry_after = int((oldest_request - window_start).total_seconds()) + 1
                return False, retry_after
            
            # Add current request
            history.append(now)
            
            return True, 0
    
    async def _get_remaining(self, client_ip: str) -> int:
        """Get remaining requests for IP"""
        async with self._lock:
            if client_ip not in self.request_history:
                return self.requests_per_minute
            
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=self.window_seconds)
            
            # Count requests in current window
            history = self.request_history[client_ip]
            current_count = sum(1 for ts in history if ts >= window_start)
            
            return max(0, self.requests_per_minute - current_count)
    
    async def cleanup_old_entries(self):
        """
        Periodic cleanup of old entries.
        
        Following clean-code: Resource management
        """
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                
                async with self._lock:
                    now = datetime.utcnow()
                    cutoff = now - timedelta(seconds=self.window_seconds * 2)
                    
                    # Remove IPs with no recent requests
                    ips_to_remove = []
                    for ip, history in self.request_history.items():
                        if not history or history[-1] < cutoff:
                            ips_to_remove.append(ip)
                    
                    for ip in ips_to_remove:
                        del self.request_history[ip]
                    
                    if ips_to_remove:
                        logger.info(f"Cleaned up {len(ips_to_remove)} old IP entries")
                        
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}", exc_info=True)


class CORSMiddleware:
    """
    Custom CORS middleware configuration.
    
    Following vulnerability-scanner: Secure CORS configuration
    """
    
    @staticmethod
    def get_config(environment: str = "development") -> dict:
        """
        Get CORS configuration based on environment.
        
        Following deployment-procedures: Environment-specific config
        
        Args:
            environment: Environment name (development, staging, production)
        
        Returns:
            CORS configuration dict
        """
        if environment == "production":
            return {
                "allow_origins": [
                    "https://pili-quarts.com",
                    "https://www.pili-quarts.com",
                    "https://app.pili-quarts.com"
                ],
                "allow_credentials": True,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                "allow_headers": ["*"],
                "max_age": 600,  # 10 minutes
            }
        
        elif environment == "staging":
            return {
                "allow_origins": [
                    "https://staging.pili-quarts.com",
                    "http://localhost:3009"
                ],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"],
                "max_age": 300,
            }
        
        else:  # development
            return {
                "allow_origins": [
                    "http://localhost:3009",
                    "http://localhost:3000",
                    "http://127.0.0.1:3009",
                    "http://127.0.0.1:3000"
                ],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"],
                "max_age": 0,  # No caching in dev
            }
