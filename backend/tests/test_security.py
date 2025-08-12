import pytest
from app.core.security import hash_password, verify_password, create_access_token, verify_token

def test_password_hashing():
    """Test password hashing functionality"""
    plain_password = "mypassword123"
    hashed = hash_password(plain_password)
    
    assert hashed != plain_password
    assert len(hashed) > 50  # bcrypt hashes are typically 60 chars
    assert hashed.startswith("$2b$")  # bcrypt format

def test_password_verification():
    """Test password verification"""
    plain_password = "mypassword123"
    wrong_password = "wrongpassword"
    hashed = hash_password(plain_password)
    
    # Correct password should verify
    assert verify_password(plain_password, hashed) is True
    
    # Wrong password should not verify
    assert verify_password(wrong_password, hashed) is False

def test_jwt_token_creation():
    """Test JWT token creation"""
    user_id = "123"
    token = create_access_token(subject=user_id)
    
    assert token is not None
    assert len(token) > 100  # JWT tokens are typically long
    assert "." in token  # JWT format has dots

def test_jwt_token_verification():
    """Test JWT token verification"""
    user_id = "123"
    token = create_access_token(subject=user_id)
    
    # Valid token should decode correctly
    decoded_user_id = verify_token(token)
    assert decoded_user_id == user_id
    
    # Invalid token should return None
    invalid_token = "invalid.jwt.token"
    decoded_invalid = verify_token(invalid_token)
    assert decoded_invalid is None

def test_complete_auth_flow():
    """Test complete authentication flow"""
    user_id = "456"
    password = "testpassword"
    
    # Hash password
    hashed = hash_password(password)
    
    # Verify password
    assert verify_password(password, hashed) is True
    
    # Create token
    token = create_access_token(subject=user_id)
    
    # Verify token
    decoded_id = verify_token(token)
    assert decoded_id == user_id

def test_different_passwords_different_hashes():
    """Test that different passwords produce different hashes"""
    password1 = "password1"
    password2 = "password2"
    
    hash1 = hash_password(password1)
    hash2 = hash_password(password2)
    
    assert hash1 != hash2

def test_same_password_different_hashes():
    """Test that same password produces different hashes (salt)"""
    password = "samepassword"
    
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Different hashes due to salt
    assert hash1 != hash2
    
    # But both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True