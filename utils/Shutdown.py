import sys
import re

WORDS = ["خاموش", "turn off"]

PRIORITY = 0


def run(command, iom, profile, mapper):
    # خاموش کن دیالوگ
    return sys.exit()


def isValid(command):
    return bool(re.search(r'\bخاموش|turn off\b', command, re.IGNORECASE))
