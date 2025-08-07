from app.core.database import engine, SessionLocal, Base

print("Testing Database")

print(f"Database URL: {engine.url}")
db = SessionLocal()
print(f"Session created: {type(db)}")
db.close()
print("Session closed")