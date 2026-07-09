# 🌦 Weather Discord

A simple GitHub Actions project that automatically updates a Discord webhook embed with current weather data.

## Features

* 🌤 Weather information for:

  * Rheinbach, Germany
  * Euskirchen, Germany
* Temperature
* Wind speed
* Humidity
* Europe/Berlin timestamp
* Updates an existing Discord message
* Uses GitHub Secrets for sensitive data

## Technologies

* Python
* GitHub Actions
* OpenWeather API
* Discord Webhooks

## Project Structure

```
.github/
 └── workflows/
     └── weather.yml

weather.py
requirements.txt
README.md
```

## Configuration

The project uses GitHub Repository Secrets:

* `OPENWEATHER_API_KEY`
* `DISCORD_WEBHOOK_URL`
* `MESSAGE_ID`

These values are not stored in the repository.

## Known Issue

The project itself works correctly, including:

* Weather API requests
* Discord webhook updates
* Manual GitHub Actions runs

However, GitHub Actions scheduled workflows (`cron`) fails to start automatically, even though the workflow configuration is correct. Manual execution through `workflow_dispatch` continues to work.

The issue appears to be related to the GitHub Actions scheduler and not the Python script or APIs.
