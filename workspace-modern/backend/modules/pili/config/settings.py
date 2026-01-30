"""
PILI AI Module - Configuration
Enterprise-grade settings management
Following python-patterns and clean-code skills
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache


class PILISettings(BaseSettings):
    """
    PILI AI Module configuration.
    Uses Pydantic for validation and environment variable loading.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PILI_",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Gemini AI Configuration
    gemini_api_key: str = "dummy-key-for-testing"  # Default for testing
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_temperature: float = 0.7
    gemini_max_tokens: int = 8192
    
    # PILI Configuration
    pili_max_history: int = 50  # Max messages to keep in history
    pili_context_window: int = 10  # Messages to include in context
    pili_timeout_seconds: int = 30
    
    # WebSocket Configuration
    ws_heartbeat_interval: int = 30  # seconds
    ws_max_connections: int = 1000
    
    # Cache Configuration
    redis_url: Optional[str] = None
    cache_ttl_seconds: int = 3600  # 1 hour
    
    # Rate Limiting
    rate_limit_requests: int = 60  # requests per minute
    rate_limit_window: int = 60  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or text


@lru_cache()
def get_settings() -> PILISettings:
    """
    Get cached settings instance.
    Using lru_cache ensures singleton pattern.
    """
    return PILISettings()
