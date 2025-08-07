from backend.app.models.user import User
from datetime import date

print("Testing user model")

# Test user creation
user = User()
user.email = "test@healthsync.com"
user.birth_date = date(1990, 6, 15)

print(f"Email: {user.email}")
print(f"Birth date: {user.birth_date}")
print(f"Age: {user.age}")
print(f"is active: {user.is_active}")
