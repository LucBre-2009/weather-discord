import os
import requests


WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
API_KEY = os.environ["OPENWEATHER_API_KEY"]
MESSAGE_ID = os.environ.get("MESSAGE_ID")


def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},DE&appid={API_KEY}&units=metric&lang=de"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("OpenWeather Fehler:")
        print(response.text)
        exit(1)

    data = response.json()

    return {
        "description": data["weather"][0]["description"].capitalize(),
        "temp": round(data["main"]["temp"], 1),
        "humidity": data["main"]["humidity"],
        "wind": round(data["wind"]["speed"] * 3.6, 1)
    }


def get_time():
    try:
        url = "https://worldtimeapi.org/api/timezone/Europe/Berlin"

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        datetime_value = data["datetime"]

        return f"{datetime_value[8:10]}.{datetime_value[5:7]}.{datetime_value[:4]} - {datetime_value[11:16]} Uhr"

    except Exception as e:
        print("WorldTimeAPI nicht erreichbar:")
        print(e)

        # Fallback UTC+2
        from datetime import datetime, timezone, timedelta

        berlin_time = datetime.now(
            timezone.utc
        ) + timedelta(hours=2)

        return berlin_time.strftime(
            "%d.%m.%Y - %H:%M Uhr"
        )


def create_embed():

    rheinbach = get_weather("Rheinbach")
    euskirchen = get_weather("Euskirchen")

    current_time = get_time()

    return {
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


embed = create_embed()


# Nachricht bearbeiten
if MESSAGE_ID:

    url = f"{WEBHOOK_URL}/messages/{MESSAGE_ID}"

    response = requests.patch(
        url,
        json={
            "embeds": [embed]
        }
    )

    if response.status_code == 200:
        print("✅ Wetter-Nachricht aktualisiert")
    else:
        print("❌ Fehler beim Aktualisieren")
        print(response.text)


# Neue Nachricht erstellen
else:

    response = requests.post(
        WEBHOOK_URL,
        params={
            "wait": "true"
        },
        json={
            "username": "🌦 Wetter",
            "embeds": [embed]
        }
    )

    if response.status_code == 200:

        message = response.json()

        print("✅ Neue Nachricht erstellt")
        print("Neue MESSAGE_ID:")
        print(message["id"])

    else:
        print("❌ Fehler beim Erstellen")
        print(response.text)
