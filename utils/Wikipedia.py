import wikipedia

WORDS = ["wiki", "wikipedia"]  # format: search ? in wiki/wikipedia

PRIORITY = 3


def run(command, speaker, profile, mapper):
    title = command.split(" ")[1:-2]
    wikipedia.set_lang('en')
    result = wikipedia.summary(title, sentences=3)
    speaker.say(result)


def isValid(command):
    return bool(any(word in command for word in WORDS))
