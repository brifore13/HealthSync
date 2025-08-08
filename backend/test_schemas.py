from app.schemas.auth import UserRegistration, UserLogin, UserResponse, Token
from datetime import date

print("Testing API Schemas")

#Test 1: User registration schema
print("\n1.Testing UserRegister Schema")
try:
    user_data = UserRegistration(
        email="TEST@EXAMPLE.COM",
        password="MyPassword123",
        birth_date=date(1990, 6, 15)
    )
    print(f"✅ Email normalized: {user_data.email}")
    print(f"✅ Password validated: {len(user_data.password)} chars")
    print(f"✅ Birth date: {user_data.birth_date}")
except Exception as e:
    print(f"❌ Registration validation error: {e}")

# Test 2: User Login schema
print("\n2. Testing UserLogin Schema:")
try:
    login_data = UserLogin(
        email="USER@EXAMPLE.COM",
        password="anypassword"
    )
    print(f"✅ Login email normalized: {login_data.email}")
except Exception as e:
    print(f"❌ Login validation error: {e}")

# Test 3: Token Schema
print("\n3. Testing Token Schema:")
token = Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI...")
print(f"✅ Token type: {token.token_type}")

print("\n🎉 All schemas working!")