import re

import pyjokes

WORDS = ["joke"]

PRIORITY = 1


def run(command, iom, profile, mapper):
    joke = pyjokes.get_joke(language='en', category='all')
    iom.getSpeaker().say(joke)


def isValid(command):
    return bool(re.search(r'\bjoke\b', command, re.IGNORECASE))
