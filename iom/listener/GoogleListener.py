import speech_recognition as sr
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')


class Listener:
    _engine = None

    def __init__(self):
        self._engine = sr.Recognizer()

    def listenSilence(self, lang='fa-IR'):
        command = ""
        try:
            with sr.Microphone() as source:
                self._engine.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate
                print("Say something!")
                voice = self._engine.listen(source)
                command = self._engine.recognize_google(voice, language=lang)
        except Exception as e:
            print("something went wrong")
            logging.exception(e)
        return command.lower()

    def listenFile(self, path):
        command = ""
        try:
            with sr.AudioFile(path) as source:
                voice = self._engine.record(source)
                command = self._engine.recognize_google(voice, language='fa-IR')
                print(command)
        except Exception as e:
            print("something went wrong")
            logging.exception(e)

        return command
