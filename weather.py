import os
import requests
from datetime import datetime


WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
API_KEY = os.environ["OPENWEATHER_API_KEY"]


def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},DE&appid={API_KEY}&units=metric&lang=de"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("OpenWeather Antwort:")
        print(response.text)
        exit(1)

    data = response.json()

    return {
        "description": data["weather"][0]["description"].capitalize(),
        "temp": round(data["main"]["temp"], 1),
        "humidity": data["main"]["humidity"],
        "wind": round(data["wind"]["speed"] * 3.6, 1)
    }


rheinbach = get_weather("Rheinbach")
euskirchen = get_weather("Euskirchen")


current_time = datetime.now().strftime("%d.%m.%Y - %H:%M Uhr")


embed = {
    "title": "🌦 Wetter",
    "color": 3447003,
    "fields": [
        {
            "name": "📍 Rheinbach",
            "value": (
                f"🌤 {rheinbach['description']}\n"
                f"🌡 {rheinbach['temp']} °C\n"
                f"💨 {rheinbach['wind']} km/h\n"
                f"💧 {rheinbach['humidity']} %"
            ),
            "inline": True
        },
        {
            "name": "📍 Euskirchen",
            "value": (
                f"🌤 {euskirchen['description']}\n"
                f"🌡 {euskirchen['temp']} °C\n"
                f"💨 {euskirchen['wind']} km/h\n"
                f"💧 {euskirchen['humidity']} %"
            ),
            "inline": True
        }
    ],
    "footer": {
        "text": f"Zuletzt aktualisiert: {current_time}"
    }
}


payload = {
    "username": "🌦 Wetter",
    "embeds": [embed]
}


response = requests.post(
    WEBHOOK_URL,
    json=payload
)


if response.status_code == 204:
    print("✅ Wetter erfolgreich an Discord gesendet")
else:
    print("❌ Discord Fehler:")
    print(response.text)
