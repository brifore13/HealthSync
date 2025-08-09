from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class MeasurementType(str, Enum):
    """Common health measurement types"""
    # Body measurement
    WEIGHT = "weight"
    HEIGHT = "height"
    BODY_FAT = "body_fat"

    # Vital Signs
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE_SYSTOLIC = "blood_pressure_systolic"
    BLOOD_PRESSURE_DIASTOLIC = "blood_pressure_diastolic"
    BODY_TEMPERATURE = "body_temperature"

    # Activity & Fitness
    STEPS = "steps"
    CALORIES_BURNED = "calories_burned"
    EXERCISE_MINUTES = "exercise_minutes"

    # Sleep
    SLEEP_HOURS = "sleep_hours"

    # Mental Health
    MOOD_RATING = "mood_rating"
    STRESS_LEVEL = "stress_level"

    # Blood Word
    BLOOD_GLUCOSE = "blood_glucose"


class HealthRecordCreate(BaseModel):
    """Simple schema for creating health records"""
    measurement_type: MeasurementType = Field(..., description="Type of measurement")
    value: float = Field(..., description="Measurement value")
    unit: str = Field(..., description="Unit of measurement (kg, bpm, etc.)")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")
    measured_at: Optional[datetime] = Field(
        default=None,
        description="When measurement was taken(default to now)"
    )

    @validator('measured_at', pre=True, always=True)
    def set_measured_at(cls, v):
        """Set measured_at to current time if not provided"""
        return v or datetime.now(timezone.utc)
    
    @validator('value')
    def validate_value_range(cls, v, values):
        """Validate measurement values are reasonable"""
        measurement_type = values.get('measurement_type')

        # Reasonable ranges for safety
        valid_ranges = {
            MeasurementType.WEIGHT: (20, 500),  # kg
            MeasurementType.HEIGHT: (50, 250),  # cm
            MeasurementType.HEART_RATE: (30, 220),  # bpm
            MeasurementType.BLOOD_PRESSURE_SYSTOLIC: (70, 250),  # mmHg
            MeasurementType.BLOOD_PRESSURE_DIASTOLIC: (40, 150),  # mmHg
            MeasurementType.BODY_TEMPERATURE: (35.0, 42.0),  # °C
            MeasurementType.STEPS: (0, 100000),  # steps/day
            MeasurementType.SLEEP_HOURS: (0, 24),  # hours
            MeasurementType.MOOD_RATING: (0, 10),  # scale
            MeasurementType.STRESS_LEVEL: (0, 10)  # scale
        }

        if measurement_type in valid_ranges:
            min_val, max_val = valid_ranges[measurement_type]
            if not (min_val <= v <= max_val):
                raise ValueError(
                    f'{measurement_type} must be between {min_val} and {max_val}'
                )

        return v


class HealthRecordResponse(BaseModel):
    """Schema for health record responses"""
    id: int
    measurement_type: MeasurementType
    value: float
    unit: str
    notes: Optional[str] = None
    measured_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class HealthRecordUpdate(BaseModel):
    """Schema for updating health records"""
    value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    measured_at: Optional[datetime] = None


class HealthRecordsQuery(BaseModel):
    """Schema for querying health records"""
    measurement_types: Optional[List[MeasurementType]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(50, ge=1, le=1000, description="Number of records to return")
    offset: int = Field(0, ge=0, description="Number of records to skip")

    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Ensure end_date is after start_date"""
        start_date = values.get('start_date')
        if start_date and v and v <= start_date:
            raise ValueError('end_date must be after start_date')
        return v
    

class HealthSummary(BaseModel):
    """Schema for health data summary/dashboard"""
    total_records: int
    measurement_types_count: int
    date_range: Optional[dict] = None
    latest_measurement: List[HealthRecordResponse] = []


class QuickAdd(BaseModel):
    """Schema for quick measurement entry(common patterns)"""
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    heart_rate_bpm: Optional[int] = Field(None, ge=30, le=220)
    steps: Optional[int] = Field(None, ge=0, le=100000)
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    mood_rating: Optional[int] = Field(None, ge=1, le=10)

    def to_health_records(self) -> List[HealthRecordCreate]:
        """Convert to individual health records"""
        records = []

        if self.weight_kg is not None:
            records.append(HealthRecordCreate(
                measurement_type=MeasurementType.WEIGHT,
                value=self.weight_kg,
                unit="kg"
            ))
        
        if self.heart_rate_bpm is not None:
            records.append(HealthRecordCreate(
                measurement_type=MeasurementType.HEART_RATE,
                value=float(self.heart_rate_bpm),
                unit="bpm"
            ))
        
        if self.steps is not None:
            records.append(HealthRecordCreate(
                measurement_type=MeasurementType.STEPS,
                value=float(self.steps),
                unit="steps"
            ))
        
        if self.sleep_hours is not None:
            records.append(HealthRecordCreate(
                measurement_type=MeasurementType.SLEEP_HOURS,
                value=self.sleep_hours,
                unit="hours"
            ))
        
        if self.mood_rating is not None:
            records.append(HealthRecordCreate(
                measurement_type=MeasurementType.MOOD_RATING,
                value=float(self.mood_rating),
                unit="scale"
            ))

        return records