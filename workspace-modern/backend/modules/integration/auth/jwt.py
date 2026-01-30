"""
Integration Module - JWT Authentication
Enterprise-grade authentication with security best practices
Following vulnerability-scanner and api-patterns skills
"""
from datetime import datetime, timedelta
from typing import Optional
import logging

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"  # TODO: Move to env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


class TokenData(BaseModel):
    """Token payload data"""
    user_id: str
    email: str
    rol: str
    exp: datetime


class Token(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    
    Following vulnerability-scanner: Secure password hashing
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    
    Following clean-code: Clear function naming
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Following api-patterns: JWT for stateless auth
    Following vulnerability-scanner: Token expiration
    
    Args:
        data: Payload data to encode
        expires_delta: Custom expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token with longer expiration.
    
    Following api-patterns: Refresh token pattern
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify and decode JWT token.
    
    Following vulnerability-scanner: Token validation
    
    Args:
        token: JWT token to verify
    
    Returns:
        Decoded token data
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        rol: str = payload.get("rol")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"))
        
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenData(user_id=user_id, email=email, rol=rol, exp=exp)
        
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    FastAPI dependency to get current authenticated user.
    
    Following python-patterns: Dependency injection
    Following api-patterns: Bearer token authentication
    
    Usage:
        @router.get("/protected")
        async def protected_route(user: TokenData = Depends(get_current_user)):
            return {"user_id": user.user_id}
    """
    token = credentials.credentials
    return verify_token(token)


async def get_current_active_user(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """
    Get current active user (additional validation can be added).
    
    Following clean-code: Separation of concerns
    """
    # TODO: Check if user is active in database
    return current_user


async def require_admin(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """
    Require admin role.
    
    Following api-patterns: Role-based access control
    """
    if current_user.rol not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def create_tokens(user_id: str, email: str, rol: str) -> Token:
    """
    Create access and refresh tokens for user.
    
    Following clean-code: Single function for token creation
    
    Args:
        user_id: User's unique identifier
        email: User's email
        rol: User's role
    
    Returns:
        Token object with access and refresh tokens
    """
    token_data = {
        "sub": user_id,
        "email": email,
        "rol": rol
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds
    )
