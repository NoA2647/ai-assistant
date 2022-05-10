import speech_recognition as sr


class Listener:
    _engine = None

    def __init__(self):
        self._engine = sr.Recognizer()

    def listenSilence(self, lang='fa-IR'):
        command = ""
        try:
            with sr.Microphone() as source:
                voice = self._engine.listen(source)
                command = self._engine.recognize_google(voice, language=lang)
        except Exception as e:
            print("Problem from speechRecognizer(Start)")
            print(e)
            print("Problem from speechRecognizer(Finish)")
        return command.lower()

    def listenFile(self, path):
        command = ""
        try:
            with sr.AudioFile(path) as source:
                voice = self._engine.record(source)
                command = self._engine.recognize_google(voice, language='fa-IR')
                print(command)
        except Exception as e:
            print("Problem from speechRecognizer(Start)")
            print(e)
            print("Problem from speechRecognizer(Finish)")

        return command
