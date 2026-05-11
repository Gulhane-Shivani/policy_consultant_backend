import requests

url = "http://localhost:10000/register"
payload = {
    "full_name": "Test User 2",
    "email": "test2@example.com",
    "password": "password123",
    "mobile": "123" # Invalid mobile
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
