import sys
import re

WORDS = ["shut down", "turn off"]

PRIORITY = 0


def run(command, speaker, profile):
    speaker.say('good bye')
    sys.exit()


def isValid(command):
    return bool(re.search(r'\bshut down|turn off\b', command, re.IGNORECASE))
