import re
import pywhatkit

WORDS = ["music"]  # format: play ? music from ?

PRIORITY = 1


def run(command, speaker, profile):
    musicName = "music"
    source = "myMusic"
    print(command.split(' '))
    if "from" in command:
        source = command.split(" ")[-1]
    musicName = command.split(' ')[1]
    speaker.say(f"playing {musicName} music")

    if source == "youtube":
        pywhatkit.playonyt(topic=musicName, open_video=True)

    if source == "myMusic":
        pass


def isValid(command):
    return bool(re.search(r'\bmusic\b', command, re.IGNORECASE))
