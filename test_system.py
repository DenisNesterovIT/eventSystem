import requests

url = "http://localhost:5050/send"
data = {"user": "professor", "message": "Hello, this is a test message!"}
response = requests.post(url, json=data)

print(f"Response status code: {response.status_code}")
print(f"Response text: {response.text}")