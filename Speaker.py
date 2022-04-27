from gtts import gTTS
import os


class Speaker:

    def __init__(self, mapper):
        self.map = mapper

    def sayGoogle(self, text):
        tts = gTTS(text=text, lang='en', tld="com")
        filename = "abc.mp3"
        tts.save(filename)
        os.system(f'mpg321 {filename}')
        os.remove(filename)

    def say(self, text):
        # api
        pass

    def play(self, name):
        audioPath = self.map.getAudioPath()
        print(f"audioPath: {audioPath}/{name}")
        os.system(f'mpg321 {audioPath}/{name}')