from Manager import Manager
from Speaker import Speaker
from Listener import Listener
from Profile import Profile
import sys


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
    listener = Listener()
    speaker = Speaker()
    profile = Profile()
    profile.readProfile()
    manager = Manager(profile, speaker)
    manager.getUtils()
    welcome(speaker, profile.getName())
    while True:
        while True:
            print("wake word:")
            if wakeWord(listener, speaker):
                break
        print("listen")
        #command = "transfer file to me"
        command = listener.listen()
        manager.query(command)
        #sys.exit()

run_ai()
