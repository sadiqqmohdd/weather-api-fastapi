from fastapi import FastAPI,HTTPException
import os
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

url = "https://api.weatherapi.com/v1/current.json"

app = FastAPI()

@app.get("/weather")
def citys(cityname:str):
    try:
        response = requests.get(url,params={"key" : api_key,"q":cityname},timeout=15)
        if response.status_code != 200:
            print(response.status_code)
            print(response.json())
            raise HTTPException(status_code=404,detail="city not found")

        data = response.json()
        data1 = data["location"]["name"] 
        data2 = data["current"]["temp_c"] 
        data3 = data["current"]["condition"]["text"]
        return {"City":data1,
                "temperature_c":data2,
                "condition":data3}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504,detail="Timeout")

