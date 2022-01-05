import os

_APP_PATH = os.path.dirname(os.path.abspath(__file__))

_AUDIO_PATH = os.path.join(_APP_PATH, "audios")
_UTILS_PATH = os.path.join(_APP_PATH, "utils")

_PROFILE_PATH = os.path.expanduser(os.getenv('PROFILE_CONFIG', '~/.profile'))


def getProfilePath():
    return _PROFILE_PATH


def getAppPath():
    return _APP_PATH


def getAudioPath():
    return _AUDIO_PATH


def getUtilsPath():
    return _UTILS_PATH
