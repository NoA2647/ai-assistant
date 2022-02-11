import json
import os


def createProfile(path):
    print("fill your profile")
    name = input("name: ")
    userName = input("userName(what you wanna AI call you): ")
    ipAddress = input(
        "static local ip address of your ai(if you don't have static ip address just press Enter): ")
    email = input("email(it uses to read & send emails): ")
    nas = input("create home server(yes/no): ")
    nas = nas.lower()
    if nas is "yes" or nas is "y":
        nas = True
    else:
        nas = False

    profile = {
        "name": name,
        "userName": userName,
        "ipAddress": ipAddress,
        "email": email,
        "nas": nas
    }

    json_object = json.dumps(profile)

    with open(path, "w") as outfile:
        outfile.write(json_object)
        outfile.close()


class Profile:

    def __init__(self, mapper):
        self.map = mapper
        self._name = ""
        self._userName = ""
        self._ipAddress = ""
        self._email = ""
        self._nas = False

        if not os.path.isfile(self.map.getProfilePath):
            createProfile(self.map.getProfilePath())

    def readProfile(self):
        path = self.map.getProfilePath()
        file = open(path)
        profile = json.load(file)
        self._name = profile["name"]
        self._userName = profile["userName"]
        self._ipAddress = profile["ipAddress"]
        self._email = profile["email"]
        self._nas = profile["nas"]
        file.close()

    def getName(self):
        return self._name

    def getUserName(self):
        return self._userName

    def getIpAddress(self):
        return self._ipAddress

    def getEmail(self):
        return self._email

    def getNas(self):
        return self._nas
