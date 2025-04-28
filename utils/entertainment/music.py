import pywhatkit
import os
import random
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s',
                    encoding="utf-8")


class MusicManager:
    KEYWORDS = ["موزیک", "آهنگ", "اهنگ", "ترانه", "موسیقی"]
    PRIORITY = 4

    MOOD_PLAYLISTS = {
        "ورزشی": ["Eye of the Tiger", "Stronger Kanye West", "Can't Hold Us Macklemore"],
        "آرامش": ["Weightless Marconi Union", "Clair de Lune Debussy", "River Flows in You"],
        "غمگین": ["Someone Like You Adele", "Fix You Coldplay", "Yesterday Beatles"],
        "شاد": ["Happy Pharrell Williams", "Uptown Funk Bruno Mars", "Shake It Off Taylor Swift"],
    }

    def __init__(self, iom, profile, mapper):
        self.iom = iom
        self.profile = profile
        self.mapper = mapper

    def search_music(self, query):
        self.iom.getSpeaker().say(f"در حال جستجوی آهنگ در یوتیوب...")
        pywhatkit.playonyt(topic=query, open_video=True)

    def play_local_music(self):
        path = self.mapper.getNasMusicPath()
        musics = os.listdir(path)
        if len(musics) == 0:
            self.iom.getSpeaker().say("هیچ آهنگی پیدا نشد!")
            return
        music = random.choice(musics)
        os.system(f'mpg321 "{path}/{music}"')

    def play_mood_music(self, mood):
        if mood not in self.MOOD_PLAYLISTS:
            self.iom.getSpeaker().say(f"متاسفم، پلی‌لیست '{mood}' موجود نیست.")
            return

        song = random.choice(self.MOOD_PLAYLISTS[mood])
        self.iom.getSpeaker().say(f"در حال پخش آهنگ مناسب برای {mood}.")
        self.search_music(song)

    def run(self, command):
        command_words = command.split(' ')
        music_name = "any"
        source = "myMusic"

        if "خارج" in command:
            source = "youtube"

        if len(command_words) > 1:
            music_name = command_words[1]

        self.iom.getSpeaker().say(f"در حال پردازش درخواست شما...")

        # بررسی مودهای خاص
        if "ورزشی" in command:
            self.play_mood_music("ورزشی")
        elif "آرامش" in command or "آرامش‌بخش" in command:
            self.play_mood_music("آرامش")
        elif "غمگین" in command:
            self.play_mood_music("غمگین")
        elif "شاد" in command:
            self.play_mood_music("شاد")
        else:
            # حالت معمولی
            if source == "youtube":
                self.search_music(music_name)
            elif source == "myMusic":
                self.play_local_music()
