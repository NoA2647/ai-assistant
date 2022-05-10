from iom.Speaker import Speaker
from iom.screen.Screen import Screen
from iom.listener.GoogleListener import Listener
from iom.Camera import Camera


class IOM:
    def __init__(self, mapper):
        self.listener = Listener()
        self.speaker = Speaker(mapper)
        self.screen = Screen(mapper)
        self.camera = Camera()

    def getListener(self):
        return self.listener

    def getSpeaker(self):
        return self.speaker

    def getScreen(self):
        return self.screen

    def getCamera(self):
        return self.camera


# test camera
# iom = iom('')
# camera = iom.getCamera()
# img = camera.phoneCamera('192.168.213.36')
