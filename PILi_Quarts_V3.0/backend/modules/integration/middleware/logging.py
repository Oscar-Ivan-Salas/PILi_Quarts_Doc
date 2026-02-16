"""
Integration Module - Logging Middleware
Enterprise-grade request/response logging
Following clean-code and python-patterns skills
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging
import time
import json
from uuid import uuid4

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Request/Response logging middleware.
    
    Features:
    - Request ID generation
    - Request/response logging
    - Performance metrics
    - Error tracking
    
    Following clean-code: Comprehensive logging
    Following python-patterns: Async middleware
    """
    
    def __init__(self, app, log_body: bool = False):
        """
        Initialize logging middleware.
        
        Args:
            app: FastAPI application
            log_body: Whether to log request/response bodies
        """
        super().__init__(app)
        self.log_body = log_body
        logger.info("Request logging middleware initialized")
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process request with logging.
        
        Following python-patterns: Async pattern
        """
        # Generate request ID
        request_id = str(uuid4())
        request.state.request_id = request_id
        
        # Start timer
        start_time = time.time()
        
        # Log request
        await self._log_request(request, request_id)
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            await self._log_response(request, response, duration, request_id)
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{duration:.3f}s"
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration": f"{duration:.3f}s",
                    "error": str(e)
                },
                exc_info=True
            )
            raise
    
    async def _log_request(self, request: Request, request_id: str):
        """
        Log incoming request.
        
        Following clean-code: Separation of concerns
        """
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        # Log body if enabled (be careful with sensitive data)
        if self.log_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    log_data["body_size"] = len(body)
                    # Don't log actual body content for security
            except Exception:
                pass
        
        logger.info(f"Incoming request", extra=log_data)
    
    async def _log_response(
        self,
        request: Request,
        response,
        duration: float,
        request_id: str
    ):
        """Log outgoing response"""
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": f"{duration:.3f}s"
        }
        
        # Log level based on status code
        if response.status_code >= 500:
            logger.error(f"Request completed with error", extra=log_data)
        elif response.status_code >= 400:
            logger.warning(f"Request completed with client error", extra=log_data)
        else:
            logger.info(f"Request completed successfully", extra=log_data)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Security headers middleware.
    
    Following vulnerability-scanner: Security best practices
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Add security headers to response"""
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Content Security Policy (adjust based on your needs)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        
        return response
