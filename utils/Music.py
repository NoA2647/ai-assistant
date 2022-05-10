import pywhatkit
import os
import random

WORDS = ["play", "music"]  # format: play ? music from ?

PRIORITY = 1


def run(command, iom, profile, mapper):
    musicName = "any"
    source = "myMusic"
    print(command.split(' '))
    if "from" in command:
        source = command.split(" ")[-1]
    musicName = command.split(' ')[1]
    iom.getSpeaker().say(f"playing {musicName} music")

    if source == "youtube":
        pywhatkit.playonyt(topic=musicName, open_video=True)

    elif source == "myMusic":
        path = mapper.getNasMusicPath()
        musics = os.listdir(path)
        print(musics)
        if len(musics) == 0:
            iom.getSpeaker().say("no music founded !")
            return
        music = musics[random.randint(0, len(musics)-1)]
        os.system(f'mpg321 {path}/{music}')


def isValid(command):
    return bool(all(word in command for word in WORDS))
