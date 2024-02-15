import os
from dotenv import load_dotenv
import requests
from django.shortcuts import redirect, render
from .models import City
from .forms import CityForm

# Define Constants
BASE_URL = "https://api.openweathermap.org"
GEO_ENDPOINT = "/geo/1.0/direct"
WEATHER_ENDPOINT = "/data/2.5/weather"


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()


def fetch_weather_data(city_name):
    load_dotenv()
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    geo_url = f"{BASE_URL}{GEO_ENDPOINT}?q={
        city_name}&limit=1&appid={WEATHER_API_KEY}"
    geo_data = fetch_data(geo_url)

    if geo_data:
        latitude = geo_data[0]['lat']
        longitude = geo_data[0]['lon']
        weather_url = f"{BASE_URL}{WEATHER_ENDPOINT}?lat={latitude}&lon={
            longitude}&units=metric&appid={WEATHER_API_KEY}"
        return fetch_data(weather_url)


def save_city_if_not_exists(city_name):
    existing_city = City.objects.filter(name=city_name).first()
    if not existing_city:
        cities_count = City.objects.count()
        if cities_count >= 5:
            oldest_city = City.objects.order_by('id').first()
            oldest_city.delete()
        City.objects.create(name=city_name)


def get_weather_info(city_name):
    weather_data = fetch_weather_data(city_name)
    if weather_data:
        return {
            'city': city_name,
            'temp': weather_data['main']['temp'],
            'icon': weather_data['weather'][0]['icon'],
        }
    else:
        return {
            'city': city_name,
            'temp': 'інформація відсутня',
        }
        
def delete(request, city_name):
    City.objects.filter(name=city_name).delete()
    return redirect('index')


def index(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            save_city_if_not_exists(city_name)
    else:
        form = CityForm()

    cities = City.objects.all()
    all_cities = [get_weather_info(city.name) for city in reversed(cities)]

    context = {"results": all_cities[:5], "form": form}
    return render(request, 'forecast/index.html', context)
