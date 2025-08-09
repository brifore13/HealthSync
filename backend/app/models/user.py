from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import date


class User(Base):
    """
    User model for storing user accounts
    """
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile info
    birth_date = Column(Date, nullable=True)

    # System fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    timezone = Column(String(50), default="UTC")

    health_records = relationship("HealthRecord", back_populates="user")

    @property
    def age(self) -> int:
        """Calculate age from birthdate"""
        if not self.birth_date:
            return None
        
        today = date.today()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
