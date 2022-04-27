import speech_recognition as sr


class Listener:

    _engine = None

    def __init__(self):
        self._engine = sr.Recognizer()

    def listenSilence(self):
        command = ""
        try:
            with sr.Microphone() as source:
                voice = self._engine.listen(source)
                command = self._engine.recognize_google(voice)
        except Exception as e:
            print("Problem from speechRecognizer(Start)")
            print(e)
            print("Problem from speechRecognizer(Finish)")
        return command.lower()

    def listen(self):
        # control with gui
        pass
