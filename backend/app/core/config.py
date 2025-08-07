from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application configuration settings
    """
    # App Info
    APP_NAME: str = "HealthSync API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    # Database
    DATABASE_URL: str = "sqlite:///./healthsync.db"

    class Config:
        env_file = ".env"


settings = Settings()