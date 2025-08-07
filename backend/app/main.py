"""CORE API METHODS"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

# Add Routes

app.get("/")
def read_root():
    return {"message": "HealthSync API is running"}