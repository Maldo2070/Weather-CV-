# Weather Comfort Index App

This script fetches real-time weather data for a list of cities using the OpenWeatherMap API, computes a "comfort index", and saves the results to a CSV file.

## Features

- Fetches weather data (temperature, humidity, wind speed)
- Converts temperature from Kelvin to Celsius and Fahrenheit
- Calculates comfort index using a weighted formula
- Saves processed results to `weather_data.csv`
- Includes basic error handling for API issues

## Comfort Index Formula
comfort_index = 0.5 * normalized_temp + 0.3 * (1 - humidity/100) + 0.2 * (1 - min(wind_speed, 10)/10)

Where:
- `normalized_temp = (temp_c - 0) / 40` (assuming 0–40°C range)

## Setup Instructions

### 1. Clone the Repository or Save the Script

Place the `.py` file in a working directory.

### 2. Install Dependencies

pip install requests pandas

### 3. Set Your API Key
Replace the placeholder API key in the script with your own from OpenWeatherMap.
API_KEY = 'your_openweathermap_api_key'

4. Run the Script
python your_script_name.py

5. Output
A file named weather_data.csv will be created in your working directory containing:

City
Temperature in Celsius and Fahrenheit
Difference from average temp
Humidity
Wind speed
Comfort index

Notes
The script only uses 3 sample cities but you can add more in the CITIES list.
Invalid API key or city names will be caught and printed, and those entries will be skipped.
