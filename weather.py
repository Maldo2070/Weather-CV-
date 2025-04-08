import requests
import sqlite3

API_KEY = '6396bb578b420b6a8cfd85509fa5b971'  # replace with your actual key
CITIES = ['London', 'New York', 'Tokyo']
API_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def kelvin_to_celsius(k): return k - 273.15
def kelvin_to_fahrenheit(k): return (k - 273.15) * 9/5 + 32

def fetch_weather(city):
    res = requests.get(API_URL.format(city, API_KEY)).json()
    main = res['main']
    wind = res['wind']
    return {
        'city': city,
        'temp_k': main['temp'],
        'humidity': main['humidity'],
        'wind_speed': wind['speed']
    }

def calculate_comfort_index(temp_c, humidity, wind_speed):
    norm_temp = (temp_c - 0) / 40
    return round(0.5 * norm_temp + 0.3 * (1 - humidity / 100) + 0.2 * (1 - min(wind_speed, 10) / 10), 2)

def save_to_sqlite(data):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather
                 (city TEXT, temp_c REAL, temp_f REAL, temp_diff REAL, humidity INTEGER, wind_speed REAL, comfort_index REAL)''')
    for row in data:
        c.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?)", tuple(row.values()))
    conn.commit()
    conn.close()

def main():
    weather_data = [fetch_weather(city) for city in CITIES]
    temps_c = [kelvin_to_celsius(d['temp_k']) for d in weather_data]
    avg_temp_c = sum(temps_c) / len(temps_c)

    processed = []
    for i, d in enumerate(weather_data):
        temp_c = temps_c[i]
        temp_f = kelvin_to_fahrenheit(d['temp_k'])
        temp_diff = temp_c - avg_temp_c
        comfort = calculate_comfort_index(temp_c, d['humidity'], d['wind_speed'])

        processed.append({
            'city': d['city'],
            'temp_c': round(temp_c, 2),
            'temp_f': round(temp_f, 2),
            'temp_diff': round(temp_diff, 2),
            'humidity': d['humidity'],
            'wind_speed': d['wind_speed'],
            'comfort_index': comfort
        })

    save_to_sqlite(processed)
    print("Data stored successfully in SQLite.")

if __name__ == "__main__":
    main()