import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    appid = "8611d7daa87ebb4edc0667a80610d359"
    
    if(request.method == "POST"):
        form = CityForm(request.POST)
        form.save()
        
    form = CityForm()
    
    cities = City.objects.all()
    all_cities = []
    
    for city in cities:
        
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city.name}&limit=1&appid=" + appid
        geo_response = requests.get(geo_url)
        
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            
            if geo_data:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={appid}"
                open_weather_api_response = requests.get(weather_url)
                
                if open_weather_api_response.status_code == 200:
                    api_output = open_weather_api_response.json()
                    weather_data = {
                        'city': city.name,
                        'temp': api_output['main']['temp'],
                        'icon': api_output['weather'][0]['icon'],
                    }
                    all_cities.append(weather_data)
                else:
                    print("Failed to fetch weather data:", open_weather_api_response.status_code)
            else:
                print("No data found for the specified city:", city.name)
        else:
            print("Failed to fetch geocoding data:", geo_response.status_code)
    
    context = {"results": all_cities, "form": form}
            
    return render(request, 'forecast/index.html', context)
