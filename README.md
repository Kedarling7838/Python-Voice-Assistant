
# Python Voice Assistant

## Project Overview
A Python-based voice assistant that recognizes spoken commands,
responds using text-to-speech, and performs useful tasks.

## Features
- Voice input through a microphone
- Text-to-speech responses
- Greeting and current date/time
- Google web search
- Live weather using OpenWeatherMap
- Timed audible reminders
- Email sending through SMTP with user confirmation
- Basic question answering using Wikipedia
- Custom commands using JSON configuration
- Error handling for microphone and recognition issues

## Technologies
- Python
- SpeechRecognition
- PyAudio
- pyttsx3
- Requests
- python-dotenv
- SMTP
- OpenWeatherMap API
- Wikipedia API

## Installation

1. Install Python 3.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.
4. Install dependencies:

   pip install -r requirements.txt

5. Copy .env.example to .env.
6. Configure the weather API key and test email credentials.
7. Connect a working microphone.

## Run the Project

python main.py

## Example Commands
- Hello
- What is the time?
- What is today's date?
- Search for Python interview questions
- Weather in Pune
- Remind me in 5 minutes to take a break
- Send an email
- Who is Albert Einstein?
- Open GitHub
- Goodbye

## Privacy Considerations

- Microphone audio is sent to Google's speech recognition
  service by the SpeechRecognition Google recognizer.
- Text-to-speech uses the local pyttsx3 engine.
- Weather queries are sent to OpenWeatherMap.
- Knowledge queries are sent to Wikipedia.
- Web searches are opened in the user's browser.
- Email addresses and message content are sent through the
  configured SMTP email provider when the user confirms sending.
- API keys and email credentials are stored in .env.
- Do not commit .env to version control.
- The application does not intentionally save audio recordings
  or maintain a persistent transcript.
- Reminder messages remain in application memory until triggered
  or the application exits. Reminders are not persistent across
  application restarts.

## Limitations
- Requires a working microphone.
- Online recognition, weather, and knowledge queries require
  internet connectivity.
- Intent detection uses rules and regular expressions, not a
  trained NLP model.
- Knowledge answers may be incomplete or inaccurate.
- Timed reminders work only while the application is running.

## Future Enhancements
- Machine-learning intent classification
- Graphical user interface
- Multiple languages
- Calendar integration
- Local speech recognition
- Smart home integration
