
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ValidationError

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"
REQUEST_TIMEOUT = 15

app = FastAPI(
    title="Weather API",
    description="A weather API built using Python and FastAPI.",
    version="1.0.0"
)


class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    condition: str


@app.get("/weather", response_model=WeatherResponse)
def get_weather(
    cityname: str = Query(min_length=2, max_length=50)
):
    cityname = cityname.strip()

    if not cityname:
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )

    if not WEATHER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Weather API key is missing"
        )

    try:
        response = requests.get(
            WEATHER_API_URL,
            params={
                "key": WEATHER_API_KEY,
                "q": cityname
            },
            timeout=REQUEST_TIMEOUT
        )

        data = response.json()

        if not isinstance(data, dict):
            raise HTTPException(
                status_code=502,
                detail="Unexpected response structure from weather service"
            )

        if response.status_code != 200:
            error = data.get("error", {})
            error_code = (
                error.get("code")
                if isinstance(error, dict)
                else None
            )

            if error_code == 1006:
                raise HTTPException(
                    status_code=404,
                    detail="City not found"
                )

            if error_code == 2006:
                raise HTTPException(
                    status_code=502,
                    detail="Weather service authentication failed"
                )

            raise HTTPException(
                status_code=502,
                detail="Weather service error"
            )

        location = data.get("location")
        current = data.get("current")

        if not isinstance(location, dict) or not isinstance(current, dict):
            raise HTTPException(
                status_code=502,
                detail="Unexpected response structure from weather service"
            )

        if not location.get("name") or not location.get("country"):
            raise HTTPException(
                status_code=502,
                detail="Unexpected response structure from weather service"
            )

        if (
            current.get("temp_c") is None
            or current.get("feelslike_c") is None
            or current.get("humidity") is None
        ):
            raise HTTPException(
                status_code=502,
                detail="Unexpected response structure from weather service"
            )

        condition = current.get("condition")

        if not isinstance(condition, dict) or not condition.get("text"):
            raise HTTPException(
                status_code=502,
                detail="Unexpected response structure from weather service"
            )

        return WeatherResponse(
            city=location["name"],
            country=location["country"],
            temperature_c=current["temp_c"],
            feels_like_c=current["feelslike_c"],
            humidity=current["humidity"],
            condition=condition["text"]
        )

    except requests.exceptions.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="Invalid response from weather service"
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Weather service timeout"
        )

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to weather service"
        )

    except (KeyError, ValidationError):
        raise HTTPException(
            status_code=502,
            detail="Unexpected response structure from weather service"
        )
