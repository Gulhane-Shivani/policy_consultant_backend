import requests

url = "http://localhost:10000/register"
payload = {
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "mobile": "1234567890"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
