from gtts import gTTS
import os
import playsound
import map


class Speaker:

    def say(self, audio):
        tts = gTTS(text=audio, lang='en', tld="com")
        filename = "abc.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)

    def play(self, name):
        audioPath = map.getAudioPath()
        playsound.playsound(audioPath + '/' + name)
