from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..core.database import get_db
from ..models.user import User
from ..core.deps import get_current_user
from ..models.health_record import HealthRecord
from ..schemas.health import (
    HealthRecordCreate, 
    HealthRecordResponse,
    QuickAdd,
    MeasurementType,
    HealthSummary,
    HealthRecordsQuery
)

router = APIRouter(prefix="/health", tags=["health"])

@router.post("/records", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED)
def create_health_record(
    record_data: HealthRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new health measurement"""
    
    # Create health record from schema data
    health_record = HealthRecord(
        user_id=current_user.id,
        measurement_type=record_data.measurement_type.value,
        value=record_data.value,
        unit=record_data.unit,
        notes=record_data.notes,
        measured_at=record_data.measured_at
    )

    # Save to DB
    db.add(health_record)
    db.commit()
    db.refresh(health_record)

    return health_record

@router.post("/quick-add", response_model=List[HealthRecordResponse], status_code=status.HTTP_201_CREATED)
def quick_add_health_records(
    quick_data: QuickAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add multiple health measurements at once"""

    # Convert QuickAdd to HealthRecord object
    health_record_schema = quick_data.to_health_records()

    # Create database objecst
    created_records = []
    for record_schema in health_record_schema:
        health_record = HealthRecord(
            user_id=current_user.id,
            measurement_type=record_schema.measurement_type.value,
            value=record_schema.value,
            unit=record_schema.unit,
            notes=record_schema.notes,
            measured_at=record_schema.measured_at
        )
        created_records.append(health_record)

    # Save to DB
    for record in created_records:
        db.add(record)

    db.commit()

    for record in created_records:
        db.refresh(record)

    return created_records

@router.get("/records", response_model=List[HealthRecordResponse])
def get_health_records(
    measurement_types: Optional[List[MeasurementType]] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's health records with filtering"""

    # Start with base query for current user
    query = db.query(HealthRecord).filter(HealthRecord.user_id == current_user.id)

    if measurement_types:
        type_values = [mt.value for mt in measurement_types]
        query = query.filter(HealthRecord.measurement_type.in_(type_values))
    
    if start_date:
        query = query.filter(HealthRecord.measured_at >= start_date)
    
    if end_date:
        query = query.filter(HealthRecord.measured_at <= end_date)

    records = query.offset(offset).limit(limit).all()

    return records

@router.get("/summary", response_model=HealthSummary)
def get_health_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    """Get health data summary for dashboard"""

    # get all user's health records
    all_records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    ).all()

    # Calculate summary statistics
    total_records = len(all_records)
    measurement_types_count = len(set(record.measurement_type for record in all_records))

    # Calculate date range
    date_range = None
    if all_records:
        dates = [record.measured_at for record in all_records]
        date_range = {
            "earliest": min(dates).isoformat(),
            "latest": max(dates).isoformat()
        }

    # Get latest 5 measurements
    latest_records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    ).order_by(HealthRecord.measured_at.desc()).limit(5).all()

    return HealthSummary(
        total_records=total_records,
        measurement_types_count=measurement_types_count,
        date_range=date_range,
        latest_measurement=latest_records
    )

