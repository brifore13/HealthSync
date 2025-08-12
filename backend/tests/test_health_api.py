import pytest
from fastapi import status
from datetime import datetime, timezone

def get_auth_headers(client, test_user_data):
    """Helper function to get authorization headers"""
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post("/api/v1/auth/login", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_health_record(client, test_user_data, test_health_record_data):
    """Test creating a health record"""
    headers = get_auth_headers(client, test_user_data)
    
    response = client.post("/api/v1/health/records", json=test_health_record_data, headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["measurement_type"] == test_health_record_data["measurement_type"]
    assert data["value"] == test_health_record_data["value"]
    assert data["unit"] == test_health_record_data["unit"]
    assert "id" in data

def test_create_health_record_unauthorized(client, test_health_record_data):
    """Test creating health record without authentication fails"""
    response = client.post("/api/v1/health/records", json=test_health_record_data)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_quick_add_health_records(client, test_user_data):
    """Test quick-add multiple health records"""
    headers = get_auth_headers(client, test_user_data)
    
    quick_data = {
        "weight_kg": 75.5,
        "heart_rate_bpm": 72,
        "steps": 8500,
        "mood_rating": 8
    }
    
    response = client.post("/api/v1/health/quick-add", json=quick_data, headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert len(data) == 4  # 4 different measurements
    
    # Check all measurement types are present
    measurement_types = [record["measurement_type"] for record in data]
    assert "weight" in measurement_types
    assert "heart_rate" in measurement_types
    assert "steps" in measurement_types
    assert "mood_rating" in measurement_types

def test_get_health_records(client, test_user_data, test_health_record_data):
    """Test getting health records"""
    headers = get_auth_headers(client, test_user_data)
    
    # Create a health record first
    client.post("/api/v1/health/records", json=test_health_record_data, headers=headers)
    
    # Get health records
    response = client.get("/api/v1/health/records", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert data[0]["measurement_type"] == test_health_record_data["measurement_type"]

def test_get_health_records_with_filters(client, test_user_data):
    """Test getting health records with filters"""
    headers = get_auth_headers(client, test_user_data)
    
    # Create multiple health records
    records = [
        {"measurement_type": "weight", "value": 75.5, "unit": "kg"},
        {"measurement_type": "heart_rate", "value": 72, "unit": "bpm"},
        {"measurement_type": "weight", "value": 76.0, "unit": "kg"}
    ]
    
    for record in records:
        client.post("/api/v1/health/records", json=record, headers=headers)
    
    # Filter by measurement type
    response = client.get("/api/v1/health/records", params={"measurement_types": ["weight"]}, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Count weight records
    weight_records = [r for r in data if r["measurement_type"] == "weight"]
    assert len(weight_records) == 2  # Only weight measurements

def test_get_health_records_unauthorized(client):
    """Test getting health records without authentication fails"""
    response = client.get("/api/v1/health/records")
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_health_summary(client, test_user_data, test_health_record_data):
    """Test getting health summary"""
    headers = get_auth_headers(client, test_user_data)
    
    # Create some health records first
    records = [
        {"measurement_type": "weight", "value": 75.5, "unit": "kg"},
        {"measurement_type": "heart_rate", "value": 72, "unit": "bpm"},
        {"measurement_type": "weight", "value": 76.0, "unit": "kg"}
    ]
    
    for record in records:
        client.post("/api/v1/health/records", json=record, headers=headers)
    
    # Get summary
    response = client.get("/api/v1/health/summary", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_records"] == 3
    assert data["measurement_types_count"] == 2  # weight and heart_rate
    assert "date_range" in data
    assert "latest_measurement" in data

def test_get_health_summary_empty(client, test_user_data):
    """Test getting health summary with no records"""
    headers = get_auth_headers(client, test_user_data)
    
    response = client.get("/api/v1/health/summary", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_records"] == 0
    assert data["measurement_types_count"] == 0
    assert data["date_range"] is None

def test_get_health_summary_unauthorized(client):
    """Test getting health summary without authentication fails"""
    response = client.get("/api/v1/health/summary")
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_user_can_only_see_own_records(client):
    """Test that users can only see their own health records"""
    # Create two users
    user1_data = {"email": "user1@test.com", "password": "testpass123"}
    user2_data = {"email": "user2@test.com", "password": "testpass123"}
    
    # Register both users
    client.post("/api/v1/auth/register", json=user1_data)
    client.post("/api/v1/auth/register", json=user2_data)
    
    # Login user1 and create a record
    user1_headers = get_auth_headers(client, user1_data)
    client.post("/api/v1/health/records", json={
        "measurement_type": "weight",
        "value": 75.5,
        "unit": "kg"
    }, headers=user1_headers)
    
    # Login user2 and check they can't see user1's records
    user2_headers = get_auth_headers(client, user2_data)
    response = client.get("/api/v1/health/records", headers=user2_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0  # User2 should see no records