
import speech_recognition as sr
import pyttsx3


class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 170)
        self.tts.setProperty("volume", 1.0)

    def speak(self, text):
        print(f"\nAssistant: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("\nListening...")
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
                )
                audio = self.recognizer.listen(
                    source, timeout=5, phrase_time_limit=15
                )

            text = self.recognizer.recognize_google(
                audio, language="en-IN"
            )
            print(f"You: {text}")
            return text.strip()

        except sr.WaitTimeoutError:
            self.speak("I did not hear anything. Please try again.")
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand. Please repeat.")
        except sr.RequestError:
            self.speak("The speech recognition service is unavailable.")
        except OSError:
            self.speak("Microphone error. Please check your microphone.")

        return ""
