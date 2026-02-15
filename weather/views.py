import requests
import os
from django.shortcuts import render
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  

def weather_home(request):
    weather = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        
        if not city:
            error = "Please enter a city name"
        else:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                res = requests.get(url, timeout=10).json()

                # check API success
                if res.get("cod") != 200:
                    error = res.get("message", "City not found").capitalize()
                else:
                    weather = {
                        "city": res["name"],  # Use API response for accurate city name
                        "country": res["sys"]["country"],
                        "temperature": round(res["main"]["temp"]),
                        "feels_like": round(res["main"]["feels_like"]),
                        "description": res["weather"][0]["description"].title(),
                        "icon": res["weather"][0]["icon"],
                        "humidity": res["main"]["humidity"],
                        "pressure": res["main"]["pressure"],
                        "wind_speed": round(res["wind"]["speed"], 1),
                        "wind_deg": res["wind"].get("deg", 0),
                        "clouds": res["clouds"]["all"],
                        "visibility": res.get("visibility", 0) // 1000,  # Convert to km
                    }
            except requests.exceptions.Timeout:
                error = "Request timed out. Please try again."
            except requests.exceptions.RequestException:
                error = "Network error. Please check your connection."
            except KeyError:
                error = "Unable to fetch weather data. Please try again."
            except Exception as e:
                error = "An unexpected error occurred."

    return render(request, "weather/home.html", {
        "weather": weather,
        "error": error
    })
