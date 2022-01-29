from gtts import gTTS
import os
import map


class Speaker:

    def say(self, audio):
        tts = gTTS(text=audio, lang='en', tld="com")
        filename = "abc.mp3"
        tts.save(filename)
        os.system(f'mpg321 {filename}')
        os.remove(filename)

    def play(self, name):
        audioPath = map.getAudioPath()
        print("audioPath:",audioPath)
        os.system(f'mpg321 {audioPath}/{name}')
