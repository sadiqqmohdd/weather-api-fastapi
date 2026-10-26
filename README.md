# Weather API

A beginner-friendly weather API built with Python and FastAPI. It fetches real-time weather information from WeatherAPI and returns selected details in JSON format.

## Features

- Search weather by city name
- Retrieve temperature in Celsius
- Retrieve current weather conditions
- Handle failed requests
- Handle network timeouts

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Requests
- python-dotenv
- WeatherAPI

## Installation

1. Clone this repository.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your WeatherAPI key:

   ```text
   WEATHER_API_KEY=your_api_key_here
   ```

## Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

## API Usage

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

Use the `/weather` endpoint and provide a city name as the `cityname` query parameter.

Example request:

`http://127.0.0.1:8000/weather?cityname=Bengaluru`

## Example Response

```json
{
  "City": "Bengaluru",
  "temperature_c": 19.4,
  "condition": "Partly Cloudy"
}
```

*Note: Weather values change with current conditions.*