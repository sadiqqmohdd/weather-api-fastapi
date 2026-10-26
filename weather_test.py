
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

print("Key loaded:", bool(api_key))

url = "https://api.weatherapi.com/v1/current.json"

response = requests.get(
    url,
    params={"key": api_key, "q": "Bengaluru"},
    timeout=10
)

print("Status code:", response.status_code)
print(response.json())
