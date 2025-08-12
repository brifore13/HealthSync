import pytest
from fastapi import status
from app.core.security import hash_password, create_access_token

def test_register_user(client, test_user_data):
    """Test user registration endpoint"""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data

def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email fails"""
    # Register first user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try to register same email again
    response = client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registers" in response.json()["detail"]

def test_login_user(client, test_user_data):
    """Test user login endpoint"""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_email(client):
    """Test login with invalid email"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid email or password" in response.json()["detail"]

def test_login_invalid_password(client, test_user_data):
    """Test login with invalid password"""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login with wrong password
    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid email or password" in response.json()["detail"]

def test_get_current_user(client, test_user_data):
    """Test get current user endpoint"""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post("/api/v1/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user_data["email"]

def test_get_current_user_invalid_token(client):
    """Test get current user with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED