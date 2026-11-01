# Weather API 🌤️

A RESTful Weather API built using **Python and FastAPI** that retrieves real-time weather information using the WeatherAPI service.

## Features

- Get current weather information for any supported city.
- Display temperature in Celsius.
- Display feels-like temperature.
- Retrieve humidity and weather conditions.
- Validate city-name input.
- Handle API errors and request timeouts.
- Secure API credentials using environment variables.
- Validate API responses using Pydantic.
- Automated tests using Pytest.

## Technologies Used

- Python
- FastAPI
- Requests
- Pydantic
- WeatherAPI
- Python-dotenv
- Pytest

## Project Structure

```text
Weather API/
│
├── main.py
├── weather_test.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sadiqqmohdd/weather-api-fastapi.git
cd weather-api-fastapi
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project directory:

```env
WEATHER_API_KEY=your_api_key_here
```

Get an API key from [WeatherAPI](https://www.weatherapi.com/).

### 5. Run the application

```bash
uvicorn main:app --reload
```

The application will be available at:

`http://127.0.0.1:8000`

## API Endpoint

### Get Current Weather

**Endpoint:** `/weather`

**Method:** `GET`

**Query Parameter:**

| Parameter | Type | Description |
|---|---|---|
| cityname | String | Name of the city |

**Example Request:**

```text
http://127.0.0.1:8000/weather?cityname=Bengaluru
```

**Example Response:**

```json
{
  "city": "Bengaluru",
  "country": "India",
  "temperature_c": 24.0,
  "feels_like_c": 23.0,
  "humidity": 60,
  "condition": "Cloudy"
}
```

## Error Handling

The API handles several error scenarios:

| Status Code | Description |
|---|---|
| 400 | Empty city name |
| 404 | City not found |
| 422 | Invalid query parameter |
| 500 | Missing API key |
| 502 | Weather service or response error |
| 504 | Weather service timeout |

## Running Tests

Run the automated test suite:

```bash
pytest -v
```

## API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Author

**Mohammed Sadiq**

GitHub: [sadiqqmohdd](https://github.com/sadiqqmohdd)