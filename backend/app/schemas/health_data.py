from pydantic import BaseModel, Email, Field
from typing import Optional
from datetime import datetime, timezone

class SimpleHealthRecord(BaseModel):
    """Schema for manual health data entry"""
    measurement_type: str = Field(..., description="Type of measurement (weight, heart rate, etc)")
    value: float = Field(..., description="Measurement value")
    unit: str = Field(..., description="Unit (kg, bpm, etc.)")
    notes: Optional[str] = Field(None, max_length=500)
    measured_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class BulkHealthRecord(BaseModel):
    """Upload multiple records"""
    pass

class HealthRecordFilter(BaseModel):
    """Query health data"""
    pass