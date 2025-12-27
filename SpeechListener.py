import speech_recognition as sr
import pyttsx3


class SpeechListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text: str):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for(self, seconds: float) -> str | None:
        """
        Listen to the microphone for a fixed number of seconds.
        Returns recognized text (lowercase) or None if not understood.
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = self.recognizer.listen(source, phrase_time_limit=seconds)

        try:
            text = self.recognizer.recognize_google(audio)  # type: ignore[attr-defined]
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
