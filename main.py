from Manager import Manager
from iom.IOM import IOM
from Profile import Profile
from Map import Map


def run_ai():
    mapper = Map()
    iom = IOM(mapper)
    profile = Profile(mapper)
    profile.readProfile()
    manager = Manager(profile, iom, mapper)
    manager.updateMap()
    manager.getUtils()
    while True:
        # command = "transfer file to me"
        path = iom.getScreen().record()
        command = iom.getListener().listenFile(path)
        manager.query(command)
        # sys.exit()


run_ai()
