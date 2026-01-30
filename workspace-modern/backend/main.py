"""
Main FastAPI Application
Enterprise-grade application setup with all modules integrated
Following clean-code, python-patterns, architecture, and deployment-procedures skills
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
from modules.pili.api.router import router as pili_router
from modules.pili.api.websocket import websocket_endpoint
from modules.integration.middleware.rate_limit import RateLimitMiddleware, CORSMiddleware as CORSConfig
from modules.integration.middleware.logging import RequestLoggingMiddleware, SecurityHeadersMiddleware
from modules.database.base import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Following python-patterns: Async context manager
    Following deployment-procedures: Startup/shutdown hooks
    """
    # Startup
    logger.info("🚀 Starting PILi Quarts application...")
    
    try:
        # Initialize database (commented out for testing without PostgreSQL)
        logger.info("Skipping database initialization for testing...")
        # init_db()
        # logger.info("✅ Database initialized")
        
        # Additional startup tasks
        logger.info("✅ Application started successfully")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # Cleanup tasks here
    logger.info("✅ Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="PILi Quarts API",
    description="Enterprise-grade construction project management and quotation system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)


# ============================================================================
# MIDDLEWARE CONFIGURATION
# Following architecture: Middleware order matters!
# ============================================================================

# 1. Security headers (first)
app.add_middleware(SecurityHeadersMiddleware)

# 2. CORS (before rate limiting)
cors_config = CORSConfig.get_config(environment="development")  # TODO: Use env var
app.add_middleware(CORSMiddleware, **cors_config)

# 3. Rate limiting
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=60  # TODO: Make configurable
)

# 4. Request logging (last, to log everything)
app.add_middleware(
    RequestLoggingMiddleware,
    log_body=False  # Set to True for debugging (careful with sensitive data)
)


# ============================================================================
# ROUTERS
# Following api-patterns: Modular router organization
# ============================================================================

# PILI AI Module
app.include_router(pili_router)

# WebSocket endpoint
app.websocket("/ws/pili/{user_id}")(websocket_endpoint)

# TODO: Add more routers
# app.include_router(workspaces_router)
# app.include_router(projects_router)
# app.include_router(documents_router)
# app.include_router(auth_router)


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    
    Following api-patterns: Health check at root
    """
    return {
        "service": "PILi Quarts API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Following deployment-procedures: Health monitoring
    """
    return {
        "status": "healthy",
        "service": "PILi Quarts",
        "version": "1.0.0"
    }


@app.get("/api/info", tags=["Info"])
async def api_info():
    """
    API information endpoint.
    
    Following clean-code: Expose useful information
    """
    return {
        "name": "PILi Quarts API",
        "version": "1.0.0",
        "description": "Enterprise construction project management system",
        "modules": {
            "pili_ai": "AI-powered chat and data extraction",
            "documents": "PDF/Word/Excel generation",
            "database": "PostgreSQL with SQLAlchemy",
            "auth": "JWT authentication with RBAC"
        },
        "features": [
            "Real-time WebSocket chat",
            "Document generation (PDF, Word, Excel)",
            "Role-based access control",
            "Rate limiting",
            "Request logging",
            "Security headers"
        ]
    }


# ============================================================================
# ERROR HANDLERS
# Following api-patterns: Consistent error responses
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An internal server error occurred"
        }
    )


# ============================================================================
# STARTUP MESSAGE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 80)
    logger.info("PILi Quarts - Enterprise Construction Management System")
    logger.info("=" * 80)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
