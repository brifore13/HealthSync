from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a pasword using bcrypt"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify plain text password against it's hash"""
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """ 
    Create a JWT access token for user login
    JWT: user id, expiration time, signature
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # token payload
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    # create and sign the token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt


def verify_token(token: str) -> str:
    """
    Verify and decode JWT token
    Returns the user ID if valid, None if invalid
    """
    try:
        # Decode
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        return user_id

    except JWTError:
        # token invalid or expired
        return None