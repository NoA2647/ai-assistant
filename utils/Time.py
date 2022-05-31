import jdatetime

WORDS = ["ساعت", "زمان"]

PRIORITY = 1


def run(command, iom, profile, mapper):
    jdatetime.set_locale('fa_IR')
    time = jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    print('امروز', time)
    result = f"امروز، {time} است "
    iom.getSpeaker().say(result)


def isValid(command):
    return bool(any(word in command for word in WORDS))
