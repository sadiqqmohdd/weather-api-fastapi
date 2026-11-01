
import requests
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def mock_weather_api(monkeypatch, status_code, data=None, exception=None):
    class FakeResponse:
        def json(self):
            if exception:
                raise exception
            return data

    def fake_get(*args, **kwargs):
        if exception and isinstance(exception, requests.exceptions.RequestException):
            raise exception

        response = FakeResponse()
        response.status_code = status_code
        return response

    monkeypatch.setattr("main.requests.get", fake_get)


def test_get_weather(monkeypatch):
    mock_weather_api(
        monkeypatch,
        200,
        {
            "location": {
                "name": "Bengaluru",
                "country": "India"
            },
            "current": {
                "temp_c": 24.0,
                "feelslike_c": 23.0,
                "humidity": 60,
                "condition": {
                    "text": "Cloudy"
                }
            }
        }
    )

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "city": "Bengaluru",
        "country": "India",
        "temperature_c": 24.0,
        "feels_like_c": 23.0,
        "humidity": 60,
        "condition": "Cloudy"
    }


def test_city_name_too_short():
    response = client.get("/weather?cityname=A")
    assert response.status_code == 422


def test_city_name_only_spaces():
    response = client.get("/weather?cityname=%20%20%20")

    assert response.status_code == 400
    assert response.json()["detail"] == "City name cannot be empty"


def test_city_not_found(monkeypatch):
    mock_weather_api(
        monkeypatch,
        400,
        {"error": {"code": 1006, "message": "No location found"}}
    )

    response = client.get("/weather?cityname=UnknownCity")

    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"


def test_weather_api_timeout(monkeypatch):
    mock_weather_api(
        monkeypatch,
        200,
        exception=requests.exceptions.Timeout("Request timed out")
    )

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 504
    assert response.json()["detail"] == "Weather service timeout"


def test_weather_api_request_exception(monkeypatch):
    mock_weather_api(
        monkeypatch,
        200,
        exception=requests.exceptions.RequestException("Request failed")
    )

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 502
    assert response.json()["detail"] == "Unable to connect to weather service"


def test_weather_api_authentication(monkeypatch):
    mock_weather_api(
        monkeypatch,
        400,
        {"error": {"code": 2006, "message": "Invalid API key"}}
    )

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 502
    assert response.json()["detail"] == "Weather service authentication failed"


def test_weather_api_missing_key(monkeypatch):
    monkeypatch.setattr("main.WEATHER_API_KEY", None)

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 500
    assert response.json()["detail"] == "Weather API key is missing"


def test_weather_api_invalid_json(monkeypatch):
    mock_weather_api(
        monkeypatch,
        200,
        exception=requests.exceptions.JSONDecodeError(
            "Expecting value", "", 0
        )
    )

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 502
    assert response.json()["detail"] == "Invalid response from weather service"


def test_weather_api_missing_current_data(monkeypatch):
    mock_weather_api(
        monkeypatch,
        200,
        {
            "location": {
                "name": "Bengaluru",
                "country": "India"
            }
        }
    )

    response = client.get("/weather?cityname=Bengaluru")

    assert response.status_code == 502
    assert response.json()["detail"] == "Unexpected response structure from weather service"
