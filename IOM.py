from Speaker import Speaker
from Screen import Screen
from Text import Text
from GoogleListener import Listener
from Camera import Camera


class IOM:
    def __init__(self, mapper):
        self.listener = Listener()
        self.speaker = Speaker(mapper)
        self.text = Text()
        self.screen = Screen()
        self.camera = Camera()

    def getListener(self):
        return self.listener

    def getSpeaker(self):
        return self.speaker

    def getTextReader(self):
        return self.text

    def getScreen(self):
        return self.screen

    def getCamera(self):
        return self.camera


# test
# iom = IOM('')
# camera = iom.getCamera()
# img = camera.phoneCamera('192.168.213.36')