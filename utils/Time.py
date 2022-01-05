import datetime
import re

WORDS = ["time"]

PRIORITY = 1


def run(command, speaker, profile):
    time = datetime.datetime.now().strftime("%I:%M %p")
    result = f"current time is {time}"
    speaker.say(result)


def isValid(command):
    return bool(re.search(r'\btime\b', command, re.IGNORECASE))
