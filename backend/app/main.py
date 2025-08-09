"""CORE API METHODS"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api.auth import router as auth_router
from .api.health import router as health_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HealthSync API",
    description="Health and wellness optimization platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for debugging"""
    return {
        "error": "Internal server error",
        "detail": str(exc) if app.debug else "Something went wrong"
    }

app.get("/")
def read_root():
    return {"message": "HealthSync API is running"}