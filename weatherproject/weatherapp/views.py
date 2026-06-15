from django.shortcuts import render
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def home(request):
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'dhaka'

    # Weather API
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'q': city,
        'appid': os.getenv('WEATHER_API_KEY'),
        'units': 'metric'
    }
    weather_data = requests.get(weather_url, params=weather_params).json()

    if weather_data.get('cod') != 200:
        return render(request, 'weatherapp/index.html', {
            'error': f"City '{city}' not found. Please try again."
        })

    # Unsplash Image API
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    image_url = None

    queries = [
        f'{city} city',
        f'{city} skyline',
        f'{city} landscape',
        'beautiful city skyline'
    ]

    for query in queries:
        try:
            unsplash_url = f'https://api.unsplash.com/search/photos?query={query}&per_page=1&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}'
            image_data = requests.get(unsplash_url).json()
            results = image_data.get('results', [])
            if results:
                image_url = results[0]['urls']['regular']
                break
        except Exception as e:
            print("ERROR:", e)
            continue

    description = weather_data['weather'][0]['description']
    icon = weather_data['weather'][0]['icon']
    temp = round(weather_data['main']['temp'])
    feels_like = round(weather_data['main']['feels_like'])
    humidity = weather_data['main']['humidity']
    wind_speed = round(weather_data['wind']['speed'])

    # City local time using timezone offset from API
    timezone_offset = weather_data['timezone']
    city_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=timezone_offset)
    day = city_time.strftime('%A, %B %d, %Y')

    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'feels_like': feels_like,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'day': day,
        'city': city.title(),
        'image_url': image_url,
    })