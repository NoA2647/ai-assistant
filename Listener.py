import speech_recognition as sr


class Listener:

    _engine = None

    def __init__(self):
        self._engine = sr.Recognizer()

    def listen(self):
        command = ""
        try:
            with sr.Microphone() as source:
                voice = self._engine.listen(source)
                command = self._engine.recognize_google(voice)
        except:
            pass
        return command.lower()
