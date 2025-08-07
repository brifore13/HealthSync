from app.core.security import hash_password, verify_password, create_access_token, verify_token

print("Testing Security Functions")

# Test 1: Password Hashing
print("\n1. Testing Password Hashing:")
plain_password = "mypassword123"
hashed = hash_password(plain_password)

print(f"Plain password: {plain_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

# Test 2: Password verification
print("\n2. Testing Password Verification:")
correct_password = "mypassword123"
wrong_password = "wrongpassword"

is_correct = verify_password(correct_password, hashed)
is_wrong = verify_password(wrong_password, hashed)

print(f"Correct password verification: {is_correct}")
print(f"Wrong password verification: {is_wrong}")

# Test 3: JWT toke creation
print("\n3. Testing JWT Token Creation")
user_id = "123"
token = create_access_token(subject=user_id)

print(f"User ID: {user_id}")
print(f"JWT Token: {token[:50]}...")
print(f"Token length: {len(token)} chars")

# Test 4 JWT Token verification
print("\n4. Testing JWT Token Verification:")
decode_user_id = verify_token(token)
invalid_token = "invalid.jwt.token"
decode_invalid = verify_token(invalid_token)

print(f"Decoded user ID from valid toke: {decode_user_id}")
print(f"Decoded user ID from invalid token: {decode_invalid}")

#Test 5: Complete Authentication Flow
print("\n5. Testing Complete Flow:")
if is_correct and decode_user_id == user_id and not is_wrong and not decode_invalid:
    print("All security functions passed")
else:
    print("Some tests failed")