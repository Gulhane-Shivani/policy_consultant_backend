from app.auth import hash_password, verify_password

password = "test_password"
hashed = hash_password(password)
print(f"Hashed: {hashed}")

match = verify_password(password, hashed)
print(f"Match: {match}")

if match:
    print("Auth logic working correctly")
else:
    print("Auth logic FAILED")
