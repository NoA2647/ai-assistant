import wikipedia

WORDS = ["wiki", "wikipedia"]  # format: search ? in wiki/wikipedia

PRIORITY = 3


def run(command, iom, profile, mapper):
    title = command.split(" ")[1:-2]
    wikipedia.set_lang('fa')
    result = wikipedia.summary(title, sentences=3)
    iom.getSpeaker().say(result)


def isValid(command):
    return bool(any(word in command for word in WORDS))
