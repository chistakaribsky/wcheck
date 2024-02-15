import os
from dotenv import load_dotenv
import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from", url, "Status Code:", response.status_code)
        return None

def fetch_weather_data(city_name):
    load_dotenv()
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid=" + WEATHER_API_KEY
    geo_data = fetch_data(geo_url)
    
    if geo_data:
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}"
        return fetch_data(weather_url)
    else:
        print("No data found for the specified city:", city_name)
        return None

def index(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CityForm()
    
    cities = City.objects.all()
    all_cities = []
    
    for city in cities:
        weather_data = fetch_weather_data(city.name)
        if weather_data:
            weather_info = {
                'city': city.name,
                'temp': weather_data['main']['temp'],
                'icon': weather_data['weather'][0]['icon'],
            }
            all_cities.append(weather_info)
    
    context = {"results": all_cities, "form": form}
            
    return render(request, 'forecast/index.html', context)
