import pywhatkit
import os
import random
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')

KEYWORDS = ["موزیک", "آهنگ", "اهنگ", "ترانه", "موسیقی"]

PRIORITY = 4


def run(command, iom, profile, mapper):
    musicName = "any"
    source = "myMusic"
    print(command.split(' '))
    if "خارج" in command:
        source = "youtube"
    musicName = command.split(' ')[1]
    iom.getSpeaker().say(f"پخش آهنگ")

    if source == "youtube":
        pywhatkit.playonyt(topic=musicName, open_video=True)

    elif source == "myMusic":
        path = mapper.getNasMusicPath()
        musics = os.listdir(path)
        print('musics:', musics)
        if len(musics) == 0:
            iom.getSpeaker().say("هیچ آهنگی پیدانشد !")
            return
        music = musics[random.randint(0, len(musics)-1)]
        os.system(f'mpg321 {path}/{music}')
