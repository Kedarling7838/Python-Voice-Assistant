
import os
import re
import ssl
import smtplib
import threading
import requests

from datetime import datetime
from email.message import EmailMessage
from urllib.parse import quote_plus


def get_weather(city):
    """Fetch current weather using OpenWeatherMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "Weather API key is missing. Configure your .env file."

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            },
            timeout=10
        )
        data = response.json()

        if response.status_code != 200:
            return data.get("message", "Unable to fetch weather.")

        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        return (
            f"Weather in {city}: {description}. "
            f"Temperature {temperature} degrees Celsius. "
            f"Feels like {feels_like} degrees. "
            f"Humidity {humidity} percent."
        )

    except requests.RequestException:
        return "Unable to connect to the weather service."


def set_reminder(seconds, message, speak):
    """Schedule an audible reminder without blocking the assistant."""
    if seconds <= 0 or seconds > 30 * 24 * 60 * 60:
        return "Please choose a duration between one second and 30 days."

    def alert():
        speak(f"Reminder! {message}")

    timer = threading.Timer(seconds, alert)
    timer.daemon = True
    timer.start()

    return f"Reminder set for {seconds} seconds from now."


def parse_duration(text):
    """Convert phrases such as '5 minutes' into seconds."""
    units = {
        "second": 1, "seconds": 1, "sec": 1, "secs": 1,
        "minute": 60, "minutes": 60, "min": 60, "mins": 60,
        "hour": 3600, "hours": 3600,
        "day": 86400, "days": 86400
    }

    match = re.search(
        r"(\d+)\s*(seconds?|secs?|minutes?|mins?|hours?|days?)",
        text.lower()
    )

    if not match:
        return None

    return int(match.group(1)) * units[match.group(2)]


def send_email(recipient, subject, body):
    """Send email using explicitly configured SMTP credentials."""
    sender = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_APP_PASSWORD")

    if not sender or not password:
        return "Email credentials are missing from your .env file."

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context, timeout=20
        ) as server:
            server.login(sender, password)
            server.send_message(message)

        return "Email sent successfully."

    except (smtplib.SMTPException, OSError):
        return "Unable to send email. Check your settings and connection."


def get_knowledge_answer(question):
    """Retrieve a short introductory answer from Wikipedia."""
    try:
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": question,
                "gsrlimit": 1,
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "exchars": 900,
                "format": "json"
            },
            headers={"User-Agent": "PythonVoiceAssistant/1.0"},
            timeout=10
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})

        if not pages:
            return "I could not find an answer. Please try another question."

        page = next(iter(pages.values()))
        answer = page.get("extract", "").strip()

        if not answer:
            return "I could not find a useful answer to that question."

        return answer

    except (requests.RequestException, ValueError):
        return "I could not access the knowledge service."
