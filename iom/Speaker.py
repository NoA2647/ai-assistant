from gtts import gTTS
import os
import requests
import io
from pydub import AudioSegment
from pydub.playback import play


class Speaker:

    def __init__(self, mapper):
        self.audioPath = mapper.getAudioPath()

    def sayGoogle(self, text, lang='eg'):
        tts = gTTS(text=text, lang=lang, tld="com")
        filename = os.path.join(self.audioPath, 'test.mp3')
        tts.save(filename)
        os.system(f'mpg321 {filename}')
        os.remove(filename)

    def say(self, text):
        API_KEY = "YSUJ7PGA3QV0N0N"
        url = 'http://api.farsireader.com/ArianaCloudService/ReadText'
        headers = {'Content-type': 'application/json'}
        json = {"Text": text,
                "Speaker": "Male2",
                "PitchLevel": "0",
                "PunctuationLevel": "0",
                "SpeechSpeedLevel": "0",
                "ToneLevel": "0",
                "GainLevel": "0",
                "BeginningSilence": "0",
                "EndingSilence": "0",
                "Format": "mp3",
                "Base64Encode": "0",
                "Quality": "normal",
                "APIKey": API_KEY
                }

        response = requests.post(url, json=json, headers=headers)
        if response.ok:
            filename = os.path.join(self.audioPath, 'test.mp3')
            recording = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
            recording.export(filename, format='mp3')
            play(recording)
            # os.system(f'mpg321 {filename}')
            # os.remove(filename)
        else:
            # say predefined dialog network error
            pass

    def play(self, name):
        print(f"audioPath: {self.audioPath}/{name}")
        os.system(f'mpg321 {self.audioPath}/{name}')