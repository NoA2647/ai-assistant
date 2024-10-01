from gtts import gTTS
import os
import requests
import io
from pydub import AudioSegment
from pydub.playback import play
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s',
                    encoding="utf-8")


class Speaker:

    def __init__(self, mapper):
        self.audioPath = mapper.getAudioPath()

    def sayGoogle(self, text, lang='eg'):
        logging.info('saying with google API ...')
        tts = gTTS(text=text, lang=lang, tld="com")
        filename = os.path.join(self.audioPath, 'test.mp3')
        tts.save(filename)
        os.system(f'mpg321 {filename}')
        os.remove(filename)

    def say(self, text):
        logging.info('saying with aria API ...')
        API_KEY = "VA2Q1GEOAI57SB9"
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
            logging.info('Response ok')
            filename = os.path.join(self.audioPath, 'test.mp3')
            recording = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
            recording.export(filename, format='mp3')
            play(recording)
            # os.system(f'mpg321 {filename}')
            # os.remove(filename)
        else:
            logging.info("Response not ok")
            # say predefined dialog network error
            pass

    def play(self, name):
        logging.info('playing audio file ...')
        print(f"audioPath: {self.audioPath}/{name}")
        os.system(f'mpg321 {self.audioPath}/{name}')
