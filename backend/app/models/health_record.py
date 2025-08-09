from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class HealthRecord(Base):
    """Database model for health measurements"""
    __tablename__ = "health_records"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Key to users table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # health measurement data
    measurement_type = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    measured_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="health_records")
    