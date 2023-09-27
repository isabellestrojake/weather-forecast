from flask import Flask, render_template, request
import requests


app = Flask(__name__)


def fetch_weather_data(city_name, api_key):
    weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    try:
        response = requests.get(weather_api_url)
        response.raise_for_status()
        weather_data = response.json()

        if 'main' in weather_data and 'weather' in weather_data:
            temperature = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
        else:
            temperature = None
            weather_description = None

        return temperature, weather_description

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        return None, None
    except Exception as err:
        print(f"Error: {err}")
        return None, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city')
        api_key = 'ec35ed39a3809fbb9c82df1dd9c5c278'
        temperatura_kelvin, weather_description = fetch_weather_data(city_name, api_key)
        
        if temperatura_kelvin is not None:
            temperatura_celsius = temperatura_kelvin - 273.15
        else:
            temperatura_celsius = None
        
        return render_template('result.html', temperature=temperatura_celsius, description=weather_description)
    return render_template('index.html')