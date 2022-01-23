import re

import pyjokes

WORDS = ["joke"]

PRIORITY = 1


def run(command, speaker, profile):
    joke = pyjokes.get_joke(language='en', category='all')
    speaker.say(joke)


def isValid(command):
    return bool(re.search(r'\bjoke\b', command, re.IGNORECASE))
