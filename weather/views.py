import requests
from django.shortcuts import render

API_KEY = "88d8359c0ecc615aed402d8a8bcfe015"

def weather_home(request):
    weather = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        # check API success
        if res.get("cod") != 200:
            error = res.get("message", "City not found")
        else:
            weather = {
                "city": city.title(),
                "temperature": res["main"]["temp"],
                "description": res["weather"][0]["description"],
                "humidity": res["main"]["humidity"],
                "wind": res["wind"]["speed"],
            }

    return render(request, "weather/home.html", {
        "weather": weather,
        "error": error
    })
