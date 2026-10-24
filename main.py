
from voice_engine import VoiceEngine
from commands import handle_command


def main():
    voice = VoiceEngine()

    voice.speak(
        "Welcome to your Python Voice Assistant. "
        "Say hello, ask for the time, search the web, "
        "or ask for the weather. Say goodbye to exit."
    )

    running = True

    while running:
        command = voice.listen()

        if command:
            running = handle_command(command, voice)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant stopped.")
