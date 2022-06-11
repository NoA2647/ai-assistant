from APIs.repo import Namava
import os
from hazm import *

KEYWORDS = ["فیلم", "سریال", "مستند","سینما"]

PRIORITY = 2


class Movie:
    def __init__(self, map):
        self.name = "",  # actor_name, movie_name, compony_name
        self.type = "all"
        self.score = None,
        self.genre = None,
        self.language = 'فارسی',
        self.title_group = None,
        self.start_date = None,
        self.end_date = None,
        self.length = None,
        self.episodes = None,
        self.seasons = None,
        self.country_name = None,
        self.source = "namava"

        self.tagger_model = os.path.join(map.getDataPath(), 'hazm_data/postagger.model')
        self.chunk_model = os.path.join(map.getDataPath(), 'hazm_data/chunker.model')

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_score(self):
        return self.score

    def get_genre(self):
        return self.genre

    def get_language(self):
        return self.language

    def get_title_group(self):
        return self.title_group

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_length(self):
        return self.length

    def get_episodes(self):
        return self.episodes

    def get_seasons(self):
        return self.seasons

    def get_country_name(self):
        return self.country_name

    def get_source(self):
        return self.source

    def getAll(self):
        return {
            "name": self.name,
            "score": self.score,
            "type": self.type,
            "genre": self.genre,
            "language": self.language,
            "title_group": self.title_group,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "length": self.length,
            "episodes": self.episodes,
            "seasons": self.seasons,
            "country_name": self.country_name,
            "source": self.source
        }

    def slot_filling(self, text):

        normalizer = Normalizer()
        text = normalizer.normalize(text)

        stemmer = Stemmer()
        tet = stemmer.stem(text)

        tagger = POSTagger(model=self.tagger_model)
        chunker = Chunker(model=self.chunk_model)

        rate = "امتیاز"
        films = ["فیلم", "مستند", "سریال"]
        hour = ["ساعت", "دقیقه"]
        year = "سال"
        az = "از"
        ta = "تا"
        best = ["برتر", "بهترین", "برترین"]
        newest = ["جدیدترین", "جدید", "تازه", "تازه ترین", "تازهترین"]
        season = "فصل"
        episode = "قسمت"
        countries = ["ایران", "آمریکا", "کانادا", "ژاپن", "ترکیه", "هند", "چین", "کره", "آلمان", "فرانسه", "ایتالیا",
                     "انگلستان", "انگلیس", "اسپانیا", "دانمارک", "سوئد", "روسیه", "مکزیک", "برزیل", "استرالیا"]
        numbers = ["یک", "دو", "سه", "چهار", "پنج", "شش", "شیش", "هفت", "هشت", "نه", "ده", "یازده", "دوازده", "سیزده",
                   "چهارده", "پانزده", "شانزده", "شونزده", "هقتده", "هجده", "نوزده", "بیست", "سی", "چهل", "پنجاه",
                   "شصت", "هفتاد", "هشتاد", "نود", "صد"]
        genre = ["هیجانی", "اجتماعی", "فانتزی", "علمی تخیلی", "عاشقانه", "جنگی", "خانوادگی", "درام", "اکشن", "تاریخی",
                 "ترسناک", "جنایی", "رازآلود", "کمدی", "کلاسیک", "ماجراجویی", "مستند", "موزیکال", "مهیج", "وسترن",
                 "ورزشی"]
        language = "زبان"
        doble = "دوبله"
        source = ["آپارات", "نماوا", "یوتوب", "اپارات", "فیلیمو"]

        words = word_tokenize(text)
        temp_words = words.copy()
        del_i = []

        for i in range(len(words)):

            if words[i] in genre:
                if genre != (None,):
                    self.genre.append(words[i])
                else:
                    self.genre = []
                    self.genre.append(words[i])
                del_i.append(i)
                continue

            if rate in words[i]:
                for j in range(i + 1, i + 5):
                    if words[j].isdigit():
                        self.score = words[j]
                        for z in range(i + 1, j + 1):
                            del_i.append(z)
                        break
                del_i.append(i)
                continue

            if words[i] in hour:
                self.length = words[i - 1]
                del_i.append(i)
                del_i.append(i - 1)
                continue

            if language in words[i] or doble in words[i]:
                self.language = words[i + 1]
                del_i.append(i)
                del_i.append(i + 1)
                i += 1
                continue

            if words[i] in source:
                self.source = words[i]
                del_i.append(i)
                continue

            if season in words[i]:
                if words[i + 1] in numbers or words[i + 1].isdigit():
                    self.seasons = words[i + 1]
                    del_i.append(i)
                    del_i.append(i + 1)
                    i += 1
                    continue
                else:
                    self.seasons = words[i - 1]
                    del_i.append(i)
                    del_i.append(i - 1)
                    continue

            if episode in words[i]:
                if words[i + 1] in numbers or words[i + 1].isdigit():
                    self.episodes = words[i + 1]
                    del_i.append(i)
                    del_i.append(i + 1)
                    i += 1
                    continue
                else:
                    self.episodes = words[i - 1]
                    del_i.append(i)
                    del_i.append(i - 1)
                    continue

            if words[i] in best or words[i] in newest:
                if words[i] in best:
                    self.title_group = "برتر"
                else:
                    self.title_group = "تازه"
                del_i.append(i)
                continue

            if year in words[i]:
                if words[i + 1] in numbers or words[i + 1].isdigit():
                    self.start_date = words[i + 1]
                    del_i.append(i)
                    del_i.append(i + 1)
                    i += 1
                    if ta in words[i + 1]:
                        self.end_date = words[i + 2]
                        del_i.append(i + 1)
                        del_i.append(i + 2)
                        i += 2
                        continue
                elif words[i - 1] in numbers or words[i - 1].isdigit():
                    self.start_date = words[i - 1]
                    del_i.append(i)
                    del_i.append(i - 1)
                    continue

                else:
                    self.start_date = "2022"
                    del_i.append(i)
                    continue

            for country in countries:
                if country in words[i]:
                    self.country_name = words[i]
                    del_i.append(i)
                    continue

        del_i.sort(reverse=True)
        for i in del_i:
            temp_words.pop(i)

        tags = tagger.tag(temp_words)
        chunc = tree2brackets(chunker.parse(tags))

        chuncs_split = (''.join(chunc.split('['))).split(']')

        name = []
        for chun_split in chuncs_split:
            for film in films:
                if film in chun_split and "NP" in chun_split:
                    self.type = film
                    for w in chun_split.split(" "):
                        if film not in w and "هایی" not in w and "یک" != w and "یه" != w and "NP" not in w:
                            if w.isdigit():
                                self.start_date = w
                            else:
                                name.append(w)
        self.name = " ".join(name)


def run(command, iom, profile, map):
    movie = Movie(map)
    movie.slot_filling(command)

    if movie.get_source() == "namava":
        namava = Namava()
        print(movie.getAll())
        converted = namava.convertor(movie.getAll(), map)
        print(converted)
        films = namava.search(converted)
        print(films)
        films_detail = []
        for film in films:
            m = namava.videoInfo(film['id'], film['type'])
            if m is not None:
                if movie.get_length() is not None and m['duration'] is not None:
                    if m['duration'] > int(movie.get_length()) + 20 or m['duration'] < max(int(movie.get_length()) - 20, 0):
                        continue
                if movie.get_score() != (None,) and m['score'] is not None:
                    if movie.get_score() < m['score']:
                        continue
                films_detail.append(m)

        for film in films_detail:
            print(film['name'])