from Manager import Manager
from Speaker import Speaker
from GoogleListener import Listener
from Profile import Profile
from Map import Map


def wakeWord(listener, speaker):
    command = listener.listen()
    if 'alex' in command:
        speaker.say("hi")
        return True
    else:
        return False


def welcome(speaker, name):
    speaker.say(f"Hello {name}, welcome back.")


def run_ai():
    mapper = Map()
    listener = Listener()
    speaker = Speaker(mapper)
    profile = Profile(mapper)
    profile.readProfile()
    manager = Manager(profile, speaker, mapper)
    manager.updateMap()
    manager.getUtils()
    welcome(speaker, profile.getUserName())
    #command = "play music"
    #manager.query(command)
    while True:
        while True:
            print("wake word:")
            if wakeWord(listener, speaker):
                break
        print("listen")
        command = listener.listen()
        manager.query(command)

run_ai()
