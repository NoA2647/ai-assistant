import wikipedia

WORDS = ["ویکی", "ویکی پدیا"]  # format: ؟ را در ویکی پدیا سرچ کن

PRIORITY = 3


def run(command, iom, profile, mapper):
    sent = command.split(" ")
    dar_loc = sent.index("در", -5, -1)
    title = sent[:dar_loc-1]
    wikipedia.set_lang('fa')
    result = wikipedia.summary(title, sentences=3)
    print(result)
    iom.getSpeaker().say(result)


def isValid(command):
    return bool(any(word in command for word in WORDS))
