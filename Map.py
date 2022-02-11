import os


class Map:

    def __init__(self):
        self._APP_PATH = os.path.dirname(os.path.abspath(__file__))

        self._AUDIO_PATH = os.path.join(self._APP_PATH, "audios")
        self._UTILS_PATH = os.path.join(self._APP_PATH, "utils")
        self._DATA_PATH = os.path.join(self._APP_PATH, "data")

        self._PROFILE_PATH = os.path.join(self._APP_PATH, ".profile")

    def getProfilePath(self):
        return self._PROFILE_PATH

    def getAppPath(self):
        return self._APP_PATH

    def getAudioPath(self):
        return self._AUDIO_PATH

    def getUtilsPath(self):
        return self._UTILS_PATH

    def getDataPath(self):
        return self._DATA_PATH
