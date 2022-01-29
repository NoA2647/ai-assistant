import map
import json

class Profile:

    _name = None
    _userName = None
    _ipAddress = None
    _email = None

    def readProfile(self):
        path = map.getProfilePath()
        file = open(path)
        profile = json.load(file)
        self._name = profile["name"]
        self._userName = profile["userName"]
        self._ipAddress = profile["ipAddress"]
        self._email = profile["email"]

    def getName(self):
        return self._name

    def getUserName(self):
        return self._userName

    def getIpAddress(self):
        return self._ipAddress

    def getEmail(self):
        return self._email
