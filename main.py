from Manager import Manager
from Speaker import Speaker
from Listener import Listener


def wakeWord(listener, speaker):
    command = listener.listen()
    if 'alex' in command:
        speaker.play("yes_sir.mp3")
        return True
    else:
        return False


def welcome(speaker):
    speaker.say("Hello Amir, welcome back.")


def run_ai():
    listener = Listener()
    speaker = Speaker()
    manager = Manager(None, speaker)
    manager.getUtils()
    welcome(speaker)
    while True:
        while True:
            print("wake word:")
            if wakeWord(listener, speaker):
                break
        print("listen")
        command = listener.listen()
        manager.query(command)


run_ai()
