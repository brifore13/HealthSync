from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.user import User
from ..schemas.health import (
    HealthRecordCreate,
    HealthRecordResponse,
    HealthRecordsQuery,
    QuickAdd,
    HealthSummary
)

router = APIRouter(prefix="/health", tags=["health"])

