from django.shortcuts import render
import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Full list of 195 recognized countries + common aliases
COUNTRY_NAMES = [
    'afghanistan', 'albania', 'algeria', 'andorra', 'angola',
    'antigua and barbuda', 'argentina', 'armenia', 'australia', 'austria',
    'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados',
    'belarus', 'belgium', 'belize', 'benin', 'bhutan',
    'bolivia', 'bosnia and herzegovina', 'botswana', 'brazil', 'brunei',
    'bulgaria', 'burkina faso', 'burundi', 'cabo verde', 'cambodia',
    'cameroon', 'canada', 'central african republic', 'chad', 'chile',
    'china', 'colombia', 'comoros', 'congo', 'costa rica',
    'croatia', 'cuba', 'cyprus', 'czech republic', 'denmark',
    'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt',
    'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'eswatini',
    'ethiopia', 'fiji', 'finland', 'france', 'gabon',
    'gambia', 'georgia', 'germany', 'ghana', 'greece',
    'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'guyana',
    'haiti', 'honduras', 'hungary', 'iceland', 'india',
    'indonesia', 'iran', 'iraq', 'ireland', 'israel',
    'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan',
    'kenya', 'kiribati', 'kosovo', 'kuwait', 'kyrgyzstan',
    'laos', 'latvia', 'lebanon', 'lesotho', 'liberia',
    'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'madagascar',
    'malawi', 'malaysia', 'maldives', 'mali', 'malta',
    'marshall islands', 'mauritania', 'mauritius', 'mexico', 'micronesia',
    'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco',
    'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal',
    'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria',
    'north korea', 'north macedonia', 'norway', 'oman', 'pakistan',
    'palau', 'palestine', 'panama', 'papua new guinea', 'paraguay',
    'peru', 'philippines', 'poland', 'portugal', 'qatar',
    'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia',
    'saint vincent and the grenadines', 'samoa', 'san marino',
    'sao tome and principe', 'saudi arabia', 'senegal', 'serbia',
    'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia',
    'solomon islands', 'somalia', 'south africa', 'south korea',
    'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname',
    'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan',
    'tanzania', 'thailand', 'timor-leste', 'togo', 'tonga',
    'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu',
    'uganda', 'ukraine', 'united arab emirates', 'united kingdom',
    'united states', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican city',
    'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe',
    # Common aliases
    'usa', 'uk', 'uae', 'burma', 'czech', 'ivory coast',
    'democratic republic of the congo', 'republic of the congo', 'east timor'
]

def home(request):
    # Get city from POST request, default to Dhaka
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'dhaka'

    # Reject country names before making API call
    if city.lower().strip() in COUNTRY_NAMES:
        return render(request, 'weatherapp/index.html', {
            'error': f"'{city.title()}' is a country name. Please enter a city name (e.g. London, Tokyo, Dhaka)."
        })

    # ─── Weather API ───────────────────────────────────────────────
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'q': city,
        'appid': os.getenv('WEATHER_API_KEY'),  # API key from .env
        'units': 'metric'                        # Temperature in Celsius
    }
    weather_data = requests.get(weather_url, params=weather_params).json()

    # If city not found or invalid, show error
    if weather_data.get('cod') != 200:
        return render(request, 'weatherapp/index.html', {
            'error': f"'{city}' not found. Please enter a valid city name (e.g. London, Tokyo, Dhaka)."
        })

    # ─── Unsplash Image API ────────────────────────────────────────
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')  # Key from .env
    image_url = None

    # Try multiple queries as fallbacks to find a city image
    queries = [
        f'{city} city',
        f'{city} skyline',
        f'{city} landscape',
        'beautiful city skyline'  # Last resort fallback
    ]

    for query in queries:
        try:
            unsplash_url = f'https://api.unsplash.com/search/photos?query={query}&per_page=1&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}'
            image_data = requests.get(unsplash_url).json()
            results = image_data.get('results', [])
            if results:
                image_url = results[0]['urls']['regular']  # Get image URL
                break  # Stop as soon as we find an image
        except Exception as e:
            print("ERROR:", e)
            continue  # Try next query if this one fails

    # ─── Weather Data ──────────────────────────────────────────────
    description = weather_data['weather'][0]['description']  # e.g. "clear sky"
    icon = weather_data['weather'][0]['icon']                # Icon code for image
    temp = round(weather_data['main']['temp'])               # Temperature in °C
    feels_like = round(weather_data['main']['feels_like'])   # Feels like in °C
    humidity = weather_data['main']['humidity']              # Humidity percentage
    wind_speed = round(weather_data['wind']['speed'])        # Wind speed in m/s

    # ─── City Local Time ───────────────────────────────────────────
    # OpenWeatherMap returns timezone as seconds offset from UTC
    timezone_offset = weather_data['timezone']

    # Calculate city's local time by adding offset to UTC
    city_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=timezone_offset)

    # Format date e.g. "Monday | June 15, 2026"
    day = city_time.strftime('%A | %B %d, %Y')

    # ─── GMT Offset ────────────────────────────────────────────────
    offset_hours = timezone_offset // 3600               # Convert seconds to hours
    offset_minutes = abs(timezone_offset % 3600) // 60  # Remaining minutes

    # Format GMT string e.g. "GMT+06:00" or "GMT-05:00"
    if offset_hours >= 0:
        gmt = f'GMT+{offset_hours:02d}:{offset_minutes:02d}'
    else:
        gmt = f'GMT-{abs(offset_hours):02d}:{offset_minutes:02d}'

    # Format time e.g. "09:56 AM (GMT+06:00)"
    time = f'{city_time.strftime("%I:%M %p")} ({gmt})'

    # ─── Render Template ───────────────────────────────────────────
    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'feels_like': feels_like,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'day': day,
        'time': time,
        'city': city.title(),
        'image_url': image_url,
    })