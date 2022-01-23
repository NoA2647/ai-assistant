import re
import pywhatkit

WORDS = ["play", "music"]  # format: play ? music from ?

PRIORITY = 1


def run(command, speaker, profile):
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
        # create dir for music
        # get from path and play musicName from it with library in rasp pi 4
        pass


def isValid(command):
    return bool(all(word in command for word in WORDS))
