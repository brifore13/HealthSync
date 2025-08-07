from app.core.config import settings

print(f"App Name:{settings.APP_NAME}")
print(f"App version: {settings.APP_VERSION}")
print(f"Secret key length: {len(settings.SECRET_KEY)}")
print(f"Debug mode: {settings.DEBUG}")
print(f"Database: {settings.DATABASE_URL}")