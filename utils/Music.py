import pywhatkit
import os
import random

WORDS = ["play", "music"]  # format: play ? music from ?

PRIORITY = 1


def run(command, speaker, profile, mapper):
    musicName = "any"
    source = "myMusic"
    print(command.split(' '))
    if "from" in command:
        source = command.split(" ")[-1]
    musicName = command.split(' ')[1]
    speaker.say(f"playing {musicName} music")

    if source == "youtube":
        pywhatkit.playonyt(topic=musicName, open_video=True)

    elif source == "myMusic":
        path = mapper.getNasMusic()
        musics = os. listdir(path)
        music = musics[random.randint(1, len(musics))]
        os.system(f'mpg321 {path}/{music}')


def isValid(command):
    return bool(all(word in command for word in WORDS))
