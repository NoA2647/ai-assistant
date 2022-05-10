import datetime
import re

WORDS = ["time"]

PRIORITY = 1


def run(command, iom, profile, mapper):
    time = datetime.datetime.now().strftime("%I:%M %p")
    result = f"current time is {time}"
    iom.getSpeaker().say(result)


def isValid(command):
    return bool(re.search(r'\btime\b', command, re.IGNORECASE))
