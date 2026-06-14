# Weather App

A Django weather app that shows current weather and city images.

## Live Website

🌐 [https://arsayeem.pythonanywhere.com](https://arsayeem.pythonanywhere.com)

> ⚠️ **Personal Reminder:** Log in to [PythonAnywhere](https://www.pythonanywhere.com) once every month and click **"Run until 1 month from today"** to keep the site alive. They will send an email reminder a week before it expires.

## Features

- Current temperature, humidity, wind speed, feels like
- City background images via Unsplash
- Search any city worldwide
- Responsive design

## Tech Stack

- Python / Django
- OpenWeatherMap API
- Unsplash API

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `.\venv\Scripts\activate`
4. Install requirements: `pip install -r requirements.txt`
5. Create `.env` file with your API keys:

```env
SECRET_KEY=your_django_secret_key
WEATHER_API_KEY=your_openweathermap_key
UNSPLASH_ACCESS_KEY=your_unsplash_key
```

6. Run migrations: `python manage.py migrate`
7. Run server: `python manage.py runserver`

## How to Update the Live Website

### Step 1: Push changes to GitHub (Local)

```powershell
cd C:\GitHub\ar-sayeem\weather
git add .
git commit -m "your update message"
git push
```

### Step 2: Pull changes on PythonAnywhere (Bash console)

🖥️ [Open PythonAnywhere Console](https://www.pythonanywhere.com/user/arsayeem/consoles/47145826/)

```bash
cd ~/weather-app-django
git pull
cd weatherproject
python manage.py collectstatic
```

### Step 3: Reload the website

- Go to [PythonAnywhere Web tab](https://www.pythonanywhere.com/user/arsayeem/webapps/)
- Click the green **Reload** button

That's it — your live site is updated! ✅