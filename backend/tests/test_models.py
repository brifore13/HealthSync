import pytest
from datetime import date, datetime, timezone
from app.models.user import User
from app.models.health_record import HealthRecord

def test_user_model_creation():
    """Test User model creation and properties"""
    user = User(
        email="test@healthsync.com",
        hashed_password="hashedpassword123",
        birth_date=date(1990, 6, 15),
        is_active=True,
        timezone="UTC"
    )
    
    assert user.email == "test@healthsync.com"
    assert user.hashed_password == "hashedpassword123"
    assert user.birth_date == date(1990, 6, 15)
    assert user.is_active is True
    assert user.timezone == "UTC"

def test_user_age_calculation():
    """Test user age calculation property"""
    # Test with known date
    user = User(
        email="test@example.com",
        hashed_password="hash",
        birth_date=date(1990, 1, 1)
    )
    
    age = user.age
    current_year = date.today().year
    expected_age = current_year - 1990
    
    # Age might be off by 1 depending on current date vs birthday
    assert age in [expected_age - 1, expected_age]

def test_user_age_none_when_no_birthdate():
    """Test user age is None when no birth date"""
    user = User(
        email="test@example.com",
        hashed_password="hash"
    )
    
    assert user.age is None

def test_health_record_creation():
    """Test HealthRecord model creation"""
    measured_time = datetime.now(timezone.utc)
    record = HealthRecord(
        user_id=1,
        measurement_type="weight",
        value=75.5,
        unit="kg",
        notes="Morning weight",
        measured_at=measured_time
    )
    
    assert record.user_id == 1
    assert record.measurement_type == "weight"
    assert record.value == 75.5
    assert record.unit == "kg"
    assert record.notes == "Morning weight"
    assert record.measured_at == measured_time

def test_user_health_record_relationship(db_session):
    """Test relationship between User and HealthRecord"""
    # Create user
    user = User(
        email="test@example.com",
        hashed_password="hash",
        birth_date=date(1990, 1, 1)
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Create health record
    record = HealthRecord(
        user_id=user.id,
        measurement_type="weight",
        value=75.5,
        unit="kg",
        measured_at=datetime.now(timezone.utc)
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    
    # Test relationship
    assert record.user == user
    assert user.health_records[0] == record

def test_multiple_health_records_for_user(db_session):
    """Test user can have multiple health records"""
    # Create user
    user = User(
        email="test@example.com",
        hashed_password="hash"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Create multiple health records
    records_data = [
        ("weight", 75.5, "kg"),
        ("heart_rate", 72, "bpm"),
        ("steps", 8500, "steps")
    ]
    
    for measurement_type, value, unit in records_data:
        record = HealthRecord(
            user_id=user.id,
            measurement_type=measurement_type,
            value=value,
            unit=unit,
            measured_at=datetime.now(timezone.utc)
        )
        db_session.add(record)
    
    db_session.commit()
    
    # Refresh user to load relationships
    db_session.refresh(user)
    
    assert len(user.health_records) == 3
    measurement_types = [r.measurement_type for r in user.health_records]
    assert "weight" in measurement_types
    assert "heart_rate" in measurement_types
    assert "steps" in measurement_types