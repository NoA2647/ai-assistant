import os


class Map:

    def __init__(self):
        self._APP_PATH = os.path.dirname(os.path.abspath(__file__))

        self._AUDIO_PATH = os.path.join(self._APP_PATH, "audios")
        self._UTILS_PATH = os.path.join(self._APP_PATH, "utils")
        self._DATA_PATH = None

        self._PROFILE_PATH = os.path.join(self._APP_PATH, ".profile")

        self._NAS_PATH = None
        self._NAS_DATA_PATH = None
        self._NAS_DATA_MUSIC_PATH = None

    def updateNas(self):
        if self._NAS_PATH is None:
            self._NAS_PATH = "/NasServer"

    def update(self):
        if self._DATA_PATH is None:
            self._DATA_PATH = os.path.join(self._APP_PATH, "data")
            os.mkdir(self._DATA_PATH)
        if self._NAS_PATH is not None:
            self._NAS_DATA_PATH = os.path.join(self._NAS_PATH, ".NoA_DATA")
            if not os.path.isdir(self._NAS_DATA_PATH):
                os.mkdir(self._NAS_DATA_PATH)
            self._NAS_DATA_PATH = os.path.join(self._NAS_DATA_PATH, "Music")
            if not os.path.isdir(self._NAS_DATA_MUSIC_PATH):
                os.mkdir(self._NAS_DATA_MUSIC_PATH)

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

    def getNasPath(self):
        return self._NAS_PATH

    def getNasDataPath(self):
        return self._NAS_DATA_PATH

    def getNasMusicPath(self):
        return self._NAS_DATA_MUSIC_PATH

    def setNasPath(self, path):
        self._NAS_PATH = path
