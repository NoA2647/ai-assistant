from Manager import Manager
from IOM import IOM
from Profile import Profile
from Map import Map


def wakeWord(iom):
    command = iom.getListener().listenSilence()
    if 'alex' in command:
        iom.getSpeaker().say("hi")
        return True
    else:
        return False


def welcome(speaker, name):
    speaker.say(f"Hello {name}, welcome back.")


def run_ai():
    mapper = Map()
    iom = IOM(mapper)
    profile = Profile(mapper)
    profile.readProfile()
    manager = Manager(profile, iom.getSpeaker(), mapper)
    manager.updateMap()
    manager.getUtils()
    welcome(iom.getSpeaker(), profile.getUserName())
    while True:
        while True:
            print("wake word:")
            if wakeWord(iom):
                break
        print("listen")
        # command = "transfer file to me"
        command = iom.getListener().listenSilence()
        manager.query(command)
        # sys.exit()


run_ai()
