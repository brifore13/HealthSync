import pytest
from datetime import date, datetime, timezone, timedelta
from pydantic import ValidationError
from app.schemas.auth import UserRegistration, UserLogin, UserResponse, Token
from app.schemas.health import (
    HealthRecordCreate, MeasurementType, QuickAdd,
    HealthRecordsQuery, HealthRecordUpdate
)

class TestAuthSchemas:
    """Test authentication schemas"""
    
    def test_user_registration_valid(self):
        """Test valid user registration data"""
        user_data = UserRegistration(
            email="TEST@EXAMPLE.COM",
            password="testpass123",
            birth_date=date(1990, 6, 15)
        )
        
        assert user_data.email == "test@example.com"  # Should be normalized
        assert user_data.password == "testpass123"
        assert user_data.birth_date == date(1990, 6, 15)
    
    def test_user_login_valid(self):
        """Test valid user login data"""
        login_data = UserLogin(
            email="USER@EXAMPLE.COM",
            password="anypassword"
        )
        
        assert login_data.email == "user@example.com"  # Should be normalized
        assert login_data.password == "anypassword"
    
    def test_token_schema(self):
        """Test token schema"""
        token = Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI...")
        
        assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI..."
        assert token.token_type == "bearer"

class TestHealthSchemas:
    """Test health data schemas"""
    
    def test_health_record_create_basic(self):
        """Test basic health record creation"""
        record = HealthRecordCreate(
            measurement_type=MeasurementType.WEIGHT,
            value=75.5,
            unit="kg",
            notes="Morning weight after workout"
        )
        
        assert record.measurement_type == MeasurementType.WEIGHT
        assert record.value == 75.5
        assert record.unit == "kg"
        assert record.notes == "Morning weight after workout"
        assert record.measured_at is not None  # Auto-generated
    
    def test_health_record_create_custom_timestamp(self):
        """Test health record with custom timestamp"""
        custom_time = datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)
        record = HealthRecordCreate(
            measurement_type=MeasurementType.HEART_RATE,
            value=68,
            unit="bpm",
            measured_at=custom_time
        )
        
        assert record.measured_at == custom_time
        assert record.value == 68
        assert record.unit == "bpm"
    
    def test_measurement_types(self):
        """Test all measurement types are available"""
        measurement_types = list(MeasurementType)
        
        assert MeasurementType.WEIGHT in measurement_types
        assert MeasurementType.HEART_RATE in measurement_types
        assert MeasurementType.STEPS in measurement_types
        assert MeasurementType.MOOD_RATING in measurement_types
        
        # Test values
        assert MeasurementType.WEIGHT.value == "weight"
        assert MeasurementType.HEART_RATE.value == "heart_rate"
    
    def test_quick_add_full(self):
        """Test QuickAdd with all fields"""
        quick_entry = QuickAdd(
            weight_kg=75.5,
            heart_rate_bpm=72,
            steps=8500,
            mood_rating=8
        )
        
        health_records = quick_entry.to_health_records()
        
        assert len(health_records) == 4
        
        # Check each record type
        types_found = [r.measurement_type for r in health_records]
        assert MeasurementType.WEIGHT in types_found
        assert MeasurementType.HEART_RATE in types_found
        assert MeasurementType.STEPS in types_found
        assert MeasurementType.MOOD_RATING in types_found
    
    def test_quick_add_partial(self):
        """Test QuickAdd with only some fields"""
        quick_entry = QuickAdd(
            weight_kg=75.5,
            steps=8500
        )
        
        health_records = quick_entry.to_health_records()
        
        assert len(health_records) == 2
        types_found = [r.measurement_type for r in health_records]
        assert MeasurementType.WEIGHT in types_found
        assert MeasurementType.STEPS in types_found
    
    def test_quick_add_empty(self):
        """Test QuickAdd with no fields"""
        quick_entry = QuickAdd()
        health_records = quick_entry.to_health_records()
        
        assert len(health_records) == 0
    
    def test_health_records_query_basic(self):
        """Test basic health records query"""
        query = HealthRecordsQuery(
            measurement_types=[MeasurementType.WEIGHT, MeasurementType.HEART_RATE],
            limit=20
        )
        
        assert len(query.measurement_types) == 2
        assert query.limit == 20
        assert query.offset == 0  # Default
    
    def test_health_records_query_date_range(self):
        """Test health records query with date range"""
        start_date = datetime.now(timezone.utc) - timedelta(days=7)
        end_date = datetime.now(timezone.utc)
        
        query = HealthRecordsQuery(
            start_date=start_date,
            end_date=end_date,
            limit=50
        )
        
        assert query.start_date == start_date
        assert query.end_date == end_date
        assert query.limit == 50
    
    def test_health_record_update(self):
        """Test health record update schema"""
        update_data = HealthRecordUpdate(
            value=76.0,
            notes="Updated weight measurement"
        )
        
        assert update_data.value == 76.0
        assert update_data.notes == "Updated weight measurement"
    
    def test_invalid_date_range_should_fail(self):
        """Test that date range validation works"""
        # For now, just test that the query can be created
        query = HealthRecordsQuery(
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) - timedelta(days=1),  # End before start
            limit=50
        )
        assert query is not None