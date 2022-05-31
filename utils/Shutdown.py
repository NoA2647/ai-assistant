import os

WORDS = ["خاموش"]

PRIORITY = 0


def run(command, iom, profile, mapper):
    iom.getSpeaker().say("خدانگهدار")
    # say predefined dialog
    return os._exit(0)


def isValid(command):
    return bool(any(word in command for word in WORDS))
