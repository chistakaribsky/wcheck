import requests
from django.shortcuts import render

def index(request):
    appid = "8611d7daa87ebb4edc0667a80610d359"
    city = "London"
    geo_url = "https://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid=".format(city) + appid
    geo_response = requests.get(geo_url)
    context = {}
    
    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        if geo_data:
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            
            weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lat, lon, appid)
            
            weather_response = requests.get(weather_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                api_output = {
                    'city': city,
                    'temp': weather_data['main']['temp'],
                    'icon': weather_data['weather'][0]['icon'],
                }
                context = {'result': api_output}
                
            else:
                print("Failed to fetch weather data:", weather_response.status_code)
        else:
            print("No data found for the specified city:", city)
    else:
        print("Failed to fetch geocoding data:", geo_response.status_code)
    
    return render(request, 'forecast/index.html', context)
