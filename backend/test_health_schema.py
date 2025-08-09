from app.schemas.health import (
    HealthRecordCreate, MeasurementType, QuickAdd,
    HealthRecordsQuery, HealthRecordUpdate
    )
from datetime import datetime, timezone, timedelta

print("🧪 Testing Health Schema...")

# Test 1: Basic Health Record Creation
print("\n1. Testing HealthRecordCreate:")
try:
    weight_record = HealthRecordCreate(
        measurement_type=MeasurementType.WEIGHT,
        value=75.5,
        unit="kg",
        notes="Morning weight after workout"
    )
    print(f"✅ Weight record: {weight_record.value} {weight_record.unit}")
    print(f"✅ Measurement type: {weight_record.measurement_type}")
    print(f"✅ Auto timestamp: {weight_record.measured_at}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Custom Timestamp
print("\n2. Testing Custom Timestamp:")
try:
    custom_time = datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)
    heart_rate_record = HealthRecordCreate(
        measurement_type=MeasurementType.HEART_RATE,
        value=68,
        unit="bpm",
        measured_at=custom_time
    )
    print(f"✅ Custom timestamp: {heart_rate_record.measured_at}")
    print(f"✅ Heart rate: {heart_rate_record.value} {heart_rate_record.unit}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Validation - Valid Values
print("\n3. Testing Valid Value Ranges:")
test_cases = [
    (MeasurementType.WEIGHT, 75.5, "kg"),
    (MeasurementType.HEART_RATE, 72, "bpm"),
    (MeasurementType.STEPS, 8500, "steps"),
    (MeasurementType.MOOD_RATING, 8, "scale")
]

for measurement_type, value, unit in test_cases:
    try:
        record = HealthRecordCreate(
            measurement_type=measurement_type,
            value=value,
            unit=unit
        )
        print(f"✅ {measurement_type.value}: {value} {unit}")
    except Exception as e:
        print(f"❌ {measurement_type.value}: {e}")

# Test 4: Validation - Invalid Values (Should Fail)
print("\n4. Testing Invalid Value Ranges (Should Show Errors):")
invalid_cases = [
    (MeasurementType.WEIGHT, -5, "kg", "Negative weight"),
    (MeasurementType.HEART_RATE, 300, "bpm", "Impossible heart rate"),
    (MeasurementType.STEPS, 200000, "steps", "Too many steps"),
    (MeasurementType.MOOD_RATING, 15, "scale", "Mood rating too high")
]

for measurement_type, value, unit, description in invalid_cases:
    try:
        record = HealthRecordCreate(
            measurement_type=measurement_type,
            value=value,
            unit=unit
        )
        print(f"❌ {description}: Should have failed but didn't!")
    except ValueError as e:
        print(f"✅ {description}: Correctly rejected - {e}")
    except Exception as e:
        print(f"❌ {description}: Unexpected error - {e}")

# Test 5: QuickAdd Functionality
print("\n5. Testing QuickAdd:")
try:
    quick_entry = QuickAdd(
        weight_kg=75.5,
        heart_rate_bpm=72,
        steps=8500,
        mood_rating=8
    )
    
    health_records = quick_entry.to_health_records()
    print(f"✅ QuickAdd created {len(health_records)} health records:")
    
    for record in health_records:
        print(f"   - {record.measurement_type.value}: {record.value} {record.unit}")
        
except Exception as e:
    print(f"❌ QuickAdd error: {e}")

# Test 6: Query Schema
print("\n6. Testing HealthRecordsQuery:")
try:
    # Basic query
    query = HealthRecordsQuery(
        measurement_types=[MeasurementType.WEIGHT, MeasurementType.HEART_RATE],
        limit=20
    )
    print(f"✅ Query for specific types, limit: {query.limit}")
    
    # Date range query
    start_date = datetime.now(timezone.utc) - timedelta(days=7)
    end_date = datetime.now(timezone.utc)
    
    date_query = HealthRecordsQuery(
        start_date=start_date,
        end_date=end_date,
        limit=50
    )
    print(f"✅ Date range query: Last 7 days")
    
except Exception as e:
    print(f"❌ Query error: {e}")

# Test 7: Invalid Date Range (Should Fail)
print("\n7. Testing Invalid Date Range (Should Show Error):")
try:
    invalid_query = HealthRecordsQuery(
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) - timedelta(days=1),  # End before start
        limit=50
    )
    print(f"❌ Invalid date range: Should have failed!")
except ValueError as e:
    print(f"✅ Invalid date range correctly rejected: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

# Test 8: Update Schema
print("\n8. Testing HealthRecordUpdate:")
try:
    update_data = HealthRecordUpdate(
        value=76.0,
        notes="Updated weight measurement"
    )
    print(f"✅ Update schema: New value = {update_data.value}")
    print(f"✅ Update notes: {update_data.notes}")
except Exception as e:
    print(f"❌ Update error: {e}")

# Test 9: Edge Cases
print("\n9. Testing Edge Cases:")

# Test with all measurement types
print("✅ All measurement types available:")
for measurement_type in MeasurementType:
    print(f"   - {measurement_type.value}")

# Test empty QuickAdd
try:
    empty_quick = QuickAdd()
    records = empty_quick.to_health_records()
    print(f"✅ Empty QuickAdd creates {len(records)} records (should be 0)")
except Exception as e:
    print(f"❌ Empty QuickAdd error: {e}")

print("\n🎉 Health Schema Test Complete!")