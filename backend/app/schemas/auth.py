from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, date


class UserRegistration(BaseModel):
    """Schema for user registration data"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    birth_date: Optional[date] = None
    timezone: str = Field("UTC", max_length=50)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Ensure password meets security requirements"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        return v


class UserLogin(BaseModel):
    """Schema for user login data"""
    email: EmailStr
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower()



class UserResponse(BaseModel):
    """Schema for user data returned by API"""
    id: int
    email: EmailStr
    age: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"