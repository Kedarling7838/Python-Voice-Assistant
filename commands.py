
import json
import os
import re
import webbrowser

from datetime import datetime
from urllib.parse import quote_plus

from advanced_features import (
    get_weather,
    set_reminder,
    parse_duration,
    send_email,
    get_knowledge_answer
)


def load_custom_commands():
    try:
        with open("commands.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}


def handle_command(command, voice):
    text = command.lower().strip()
    if not text:
        return True

    # Exit
    if re.search(r"\b(exit|quit|stop assistant|goodbye)\b", text):
        voice.speak("Goodbye! Have a nice day.")
        return False

    # Greeting
    if re.search(r"\b(hello|hi|hey)\b", text):
        voice.speak("Hello! How can I help you?")
        return True

    # Date and time
    if re.search(r"\b(time|clock)\b", text):
        voice.speak("The time is " + datetime.now().strftime("%I:%M %p"))
        return True

    if re.search(r"\b(date|today's date|what day is it)\b", text):
        voice.speak(datetime.now().strftime("Today is %A, %d %B %Y"))
        return True

    # Web search
    match = re.search(r"\b(?:search(?: the web)? for|google)\s+(.+)", text)
    if match:
        topic = match.group(1).strip()
        voice.speak(f"Searching the web for {topic}")
        webbrowser.open(
            "https://www.google.com/search?q=" + quote_plus(topic)
        )
        return True

    # Weather
    match = re.search(
        r"(?:weather in|weather for|temperature in|temperature for)\s+(.+)",
        text
    )
    if match:
        voice.speak(get_weather(match.group(1).strip()))
        return True

    # Reminder, e.g. "remind me in 5 minutes to take a break"
    if "remind me" in text or text.startswith("set a reminder"):
        duration = parse_duration(text)
        if duration is None:
            voice.speak(
                "Please say a duration, for example, remind me in "
                "five minutes to take a break."
            )
            return True

        message_match = re.search(
            r"\bto\s+(.+)$", text
        )
        reminder_message = (
            message_match.group(1).strip()
            if message_match else "Your scheduled task"
        )

        result = set_reminder(duration, reminder_message, voice.speak)
        voice.speak(result)
        return True

    # Email: request details through voice, then ask confirmation.
    if "send email" in text or "send an email" in text:
        voice.speak("Please say the recipient email address.")
        recipient = voice.listen().replace(" ", "").strip()

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recipient):
            voice.speak("That email address does not appear valid.")
            return True

        voice.speak("Please say the email subject.")
        subject = voice.listen().strip()

        voice.speak("Please dictate the email message.")
        body = voice.listen().strip()

        if not subject or not body:
            voice.speak("The subject or message was empty. Email cancelled.")
            return True

        voice.speak(
            f"Recipient {recipient}. Subject {subject}. "
            "Say confirm send email to send it."
        )
        confirmation = voice.listen().lower()

        if "confirm send email" not in confirmation:
            voice.speak("Email cancelled.")
            return True

        voice.speak(send_email(recipient, subject, body))
        return True

    # General knowledge
    match = re.search(
        r"(?:what is|who is|tell me about|explain)\s+(.+)",
        text
    )
    if match:
        voice.speak(get_knowledge_answer(match.group(1).strip()))
        return True

    # User-defined commands
    custom = load_custom_commands()

    for phrase, action in custom.items():
        if phrase.lower() in text:
            action_type = action.get("type")

            if action_type == "say":
                voice.speak(action.get("value", ""))
            elif action_type == "open_url":
                url = action.get("value", "")
                if url.startswith(("https://", "http://")):
                    webbrowser.open(url)
                    voice.speak("Opening your custom website.")
                else:
                    voice.speak("That custom URL is not allowed.")
            elif action_type == "search":
                query = action.get("value", "")
                voice.speak(f"Searching for {query}")
                webbrowser.open(
                    "https://www.google.com/search?q=" + quote_plus(query)
                )
            else:
                voice.speak("That custom action is not supported.")

            return True

    voice.speak(
        "Sorry, I don't understand that command. "
        "Try saying help or repeat your request."
    )
    return True
