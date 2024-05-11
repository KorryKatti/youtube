from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('OPENWEATHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']

    # OpenWeatherMap API endpoint
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        # Fetching weather data
        response = requests.get(url)
        data = response.json()

        # Extracting relevant weather information
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }

        return render_template('weather.html', weather=weather)

    except Exception as e:
        error_message = f"Error fetching weather data: {str(e)}"
        return render_template('error.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
