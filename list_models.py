import requests
import json

API_KEY = "AIzaSyAh_mZWv-TQzFQbfdRejv-1jgWYvWTkS8A"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(url)
print(json.dumps(response.json(), indent=2))
