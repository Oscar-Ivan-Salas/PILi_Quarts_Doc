"""
Unit Tests for Authentication (JWT)
Following testing-patterns: AAA pattern, security testing
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt

from modules.integration.auth.jwt import (
    hash_password,
    verify_password,
    create_tokens,
    verify_token,
    decode_token,
    TokenData,
    SECRET_KEY,
    ALGORITHM
)


@pytest.mark.unit
class TestPasswordHashing:
    """
    Password hashing tests.
    
    Following testing-patterns: Test security functions
    """
    
    def test_hash_password_returns_hash(self):
        """Should hash password and return string"""
        # Arrange
        password = "SecurePassword123!"
        
        # Act
        hashed = hash_password(password)
        
        # Assert
        assert isinstance(hashed, str)
        assert hashed != password  # Not plaintext
        assert hashed.startswith("$2b$")  # bcrypt format
    
    def test_hash_password_different_each_time(self):
        """Should generate different hash each time (salt)"""
        # Arrange
        password = "SamePassword123"
        
        # Act
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Assert
        assert hash1 != hash2  # Different due to salt
    
    def test_verify_password_correct(self):
        """Should verify correct password"""
        # Arrange
        password = "CorrectPassword123"
        hashed = hash_password(password)
        
        # Act
        result = verify_password(password, hashed)
        
        # Assert
        assert result is True
    
    def test_verify_password_incorrect(self):
        """Should reject incorrect password"""
        # Arrange
        correct_password = "CorrectPassword123"
        wrong_password = "WrongPassword456"
        hashed = hash_password(correct_password)
        
        # Act
        result = verify_password(wrong_password, hashed)
        
        # Assert
        assert result is False
    
    def test_verify_password_empty_returns_false(self):
        """Should reject empty password"""
        # Arrange
        hashed = hash_password("SomePassword")
        
        # Act
        result = verify_password("", hashed)
        
        # Assert
        assert result is False


@pytest.mark.unit
class TestJWTTokens:
    """JWT token tests"""
    
    def test_create_tokens_returns_both_tokens(self):
        """Should create access and refresh tokens"""
        # Arrange
        user_id = "user-123"
        email = "test@example.com"
        rol = "admin"
        
        # Act
        tokens = create_tokens(user_id, email, rol)
        
        # Assert
        assert tokens.access_token is not None
        assert tokens.refresh_token is not None
        assert tokens.token_type == "bearer"
        assert isinstance(tokens.access_token, str)
        assert isinstance(tokens.refresh_token, str)
    
    def test_decode_token_valid(self):
        """Should decode valid token"""
        # Arrange
        user_id = "user-123"
        email = "test@example.com"
        rol = "admin"
        tokens = create_tokens(user_id, email, rol)
        
        # Act
        payload = decode_token(tokens.access_token)
        
        # Assert
        assert payload["sub"] == user_id
        assert payload["email"] == email
        assert payload["rol"] == rol
        assert "exp" in payload
    
    def test_verify_token_valid(self):
        """Should verify valid token and return TokenData"""
        # Arrange
        user_id = "user-123"
        email = "test@example.com"
        rol = "member"
        tokens = create_tokens(user_id, email, rol)
        
        # Act
        token_data = verify_token(tokens.access_token)
        
        # Assert
        assert isinstance(token_data, TokenData)
        assert token_data.user_id == user_id
        assert token_data.email == email
        assert token_data.rol == rol
    
    def test_verify_token_expired_raises_error(self):
        """Should raise error for expired token"""
        # Arrange - Create token that expires immediately
        payload = {
            "sub": "user-123",
            "email": "test@example.com",
            "rol": "member",
            "exp": datetime.utcnow() - timedelta(minutes=1)  # Already expired
        }
        expired_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        # Act & Assert
        with pytest.raises(Exception):  # JWT expired error
            verify_token(expired_token)
    
    def test_verify_token_invalid_signature_raises_error(self):
        """Should raise error for invalid signature"""
        # Arrange
        payload = {
            "sub": "user-123",
            "email": "test@example.com",
            "rol": "member",
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        # Sign with wrong key
        invalid_token = jwt.encode(payload, "wrong-secret-key", algorithm=ALGORITHM)
        
        # Act & Assert
        with pytest.raises(Exception):  # Invalid signature error
            verify_token(invalid_token)
    
    def test_verify_token_malformed_raises_error(self):
        """Should raise error for malformed token"""
        # Arrange
        malformed_token = "not.a.valid.jwt.token"
        
        # Act & Assert
        with pytest.raises(Exception):
            verify_token(malformed_token)
    
    def test_access_token_expires_in_30_minutes(self):
        """Should set access token expiration to 30 minutes"""
        # Arrange
        tokens = create_tokens("user-123", "test@example.com", "member")
        
        # Act
        payload = decode_token(tokens.access_token)
        exp_time = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()
        
        # Assert
        time_diff = (exp_time - now).total_seconds()
        assert 1790 < time_diff < 1810  # ~30 minutes (1800s ± 10s)
    
    def test_refresh_token_expires_in_7_days(self):
        """Should set refresh token expiration to 7 days"""
        # Arrange
        tokens = create_tokens("user-123", "test@example.com", "member")
        
        # Act
        payload = decode_token(tokens.refresh_token)
        exp_time = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()
        
        # Assert
        time_diff = (exp_time - now).total_seconds()
        expected = 7 * 24 * 60 * 60  # 7 days in seconds
        assert expected - 10 < time_diff < expected + 10


@pytest.mark.unit
class TestTokenData:
    """TokenData model tests"""
    
    def test_token_data_creation(self):
        """Should create TokenData instance"""
        # Arrange & Act
        token_data = TokenData(
            user_id="user-123",
            email="test@example.com",
            rol="admin"
        )
        
        # Assert
        assert token_data.user_id == "user-123"
        assert token_data.email == "test@example.com"
        assert token_data.rol == "admin"
