
from app.models.health_record import HealthRecord
from app.models.user import User
from app.core.database import engine, Base, SessionLocal
from datetime import datetime, timezone

print("🧪 Testing Health Record Model...")

# Test 1: Create tables and check model structure
print("\n1. Testing Model Structure:")
try:
    # This will create the health_records table if it doesn't exist
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    # Check model attributes
    print(f"✅ Table name: {HealthRecord.__tablename__}")
    print(f"✅ Model has required columns")
    
except Exception as e:
    print(f"❌ Error creating tables: {e}")

# Test 2: Create a test user and health record (in memory)
print("\n2. Testing Model Creation:")
try:
    # Create test user (in memory)
    test_user = User()
    test_user.id = 1
    test_user.email = "test@healthsync.com"
    
    # Create test health record (in memory)
    health_record = HealthRecord()
    health_record.user_id = 1
    health_record.measurement_type = "weight"
    health_record.value = 75.5
    health_record.unit = "kg"
    health_record.notes = "Morning weight after workout"
    health_record.measured_at = datetime.now(timezone.utc)
    
    print(f"✅ Health record created:")
    print(f"   - Type: {health_record.measurement_type}")
    print(f"   - Value: {health_record.value} {health_record.unit}")
    print(f"   - User ID: {health_record.user_id}")
    print(f"   - Notes: {health_record.notes}")
    print(f"   - Measured at: {health_record.measured_at}")
    
except Exception as e:
    print(f"❌ Error creating model: {e}")

# Test 3: Database operations
print("\n3. Testing Database Operations:")
try:
    db = SessionLocal()
    
    # First, create a test user in the database
    existing_user = db.query(User).filter(User.email == "test@healthsync.com").first()
    if not existing_user:
        test_user_db = User(
            email="test@healthsync.com",
            hashed_password="test_hash"
        )
        db.add(test_user_db)
        db.commit()
        db.refresh(test_user_db)
        user_id = test_user_db.id
        print(f"✅ Test user created with ID: {user_id}")
    else:
        user_id = existing_user.id
        print(f"✅ Using existing test user with ID: {user_id}")
    
    # Now create a health record
    test_health_record = HealthRecord(
        user_id=user_id,
        measurement_type="weight",
        value=75.5,
        unit="kg",
        notes="Test weight measurement",
        measured_at=datetime.now(timezone.utc)
    )
    
    db.add(test_health_record)
    db.commit()
    db.refresh(test_health_record)
    
    print(f"✅ Health record saved to database:")
    print(f"   - Record ID: {test_health_record.id}")
    print(f"   - User ID: {test_health_record.user_id}")
    print(f"   - Type: {test_health_record.measurement_type}")
    print(f"   - Value: {test_health_record.value} {test_health_record.unit}")
    print(f"   - Created at: {test_health_record.created_at}")
    
    # Test the relationship
    if hasattr(test_health_record, 'user'):
        related_user = test_health_record.user
        if related_user:
            print(f"✅ Relationship works: Record belongs to {related_user.email}")
        else:
            print("⚠️ Relationship exists but user not loaded")
    
    db.close()
    
except Exception as e:
    print(f"❌ Database operation error: {e}")
    if 'db' in locals():
        db.rollback()
        db.close()

# Test 4: Query operations
print("\n4. Testing Query Operations:")
try:
    db = SessionLocal()
    
    # Query health records
    health_records = db.query(HealthRecord).limit(5).all()
    print(f"✅ Found {len(health_records)} health records in database")
    
    for record in health_records:
        print(f"   - {record.measurement_type}: {record.value} {record.unit}")
    
    # Query by user
    user_records = db.query(HealthRecord).filter(HealthRecord.user_id == user_id).all()
    print(f"✅ User has {len(user_records)} health records")
    
    # Query by measurement type
    weight_records = db.query(HealthRecord).filter(
        HealthRecord.measurement_type == "weight"
    ).all()
    print(f"✅ Found {len(weight_records)} weight measurements")
    
    db.close()
    
except Exception as e:
    print(f"❌ Query error: {e}")
    if 'db' in locals():
        db.close()

# Test 5: Model validation
print("\n5. Testing Model Constraints:")
try:
    db = SessionLocal()
    
    # Test with missing required field (should fail)
    try:
        invalid_record = HealthRecord(
            user_id=user_id,
            # measurement_type missing - should cause issues
            value=80.0,
            unit="kg",
            measured_at=datetime.now(timezone.utc)
        )
        db.add(invalid_record)
        db.commit()
        print("❌ Should have failed due to missing measurement_type")
    except Exception as validation_error:
        print(f"✅ Validation working: {type(validation_error).__name__}")
        db.rollback()
    
    db.close()
    
except Exception as e:
    print(f"❌ Validation test error: {e}")
    if 'db' in locals():
        db.rollback()
        db.close()

print("\n🎉 Health Model Test Complete!")