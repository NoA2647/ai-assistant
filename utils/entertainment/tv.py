from hazm import *
import os
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s',
                    encoding="utf-8")

KEYWORDS = ["شبکه", "تلویزیون", "برنامه"]

PRIORITY = 5


class TV:
    def __init__(self, map):
        self.show_name = "",
        self.channel_name = "",
        self.type = None,
        self.episode = None,
        self.start_time = None,
        self.start_date = None,
        self.source = "telewebion"

        self.tagger_model = os.path.join(map.getDataPath(), 'hazm_data/postagger.model')
        self.chunk_model = os.path.join(map.getDataPath(), 'hazm_data/chunker.model')

    def getAll(self):
        return {
            "show_name": self.show_name,
            "channel_name": self.channel_name,
            "type": self.type,
            "episode": self.episode,
            "start_time": self.start_time,
            "start_date": self.start_date,
            "source": self.source
        }

    def get_show_name(self):
        return self.show_name

    def get_channel_name(self):
        return self.channel_name

    def get_type(self):
        return self.type

    def get_episode(self):
        return self.episode

    def get_start_time(self):
        return self.start_time

    def get_start_date(self):
        return self.start_date

    def get_source(self):
        return self.source

    def slot_filling(self, text):

        normalizer = Normalizer()
        text = normalizer.normalize(text)

        stemmer = Stemmer()
        text = stemmer.stem(text)

        tagger = POSTagger(model=self.tagger_model)
        chunker = Chunker(model=self.chunk_model)

        films = ["فیلم", "سریال", "برنامه", "مستند"]
        tables = ["لیست", "زمان‌بندی", "زمانبندی"]
        hour = "ساعت"
        channels = ["شبکه", "کانال"]
        infos = ["مواقع", "زمان", "کی", "موقع"]
        episode = "قسمت"
        numbers = ["یک", "دو", "سه", "چهار", "پنج", "شش", "شیش", "هفت", "هشت", "نه", "ده", "یازده", "دوازده", "سیزده",
                   "چهارده", "پانزده", "شانزده", "شونزده", "هفتده", "هجده", "نوزده", "بیست", "سی", "چهل", "پنجاه",
                   "شصت", "هفتاد", "هشتاد", "نود", "صد"]
        source = ["تلوبیون"]

        words = word_tokenize(text)
        temp_words = words.copy()
        del_i = set()

        for i in range(len(words)):
            f = False

            for channel in channels:
                if channel in words[i]:
                    self.channel_name = words[i + 1]
                    del_i.add(i)
                    del_i.add(i + 1)
                    i += 1
                    f = True
                    break
            if f:
                continue

            if hour in words[i]:
                if words[i + 1].isdigit() or words[i + 1] in numbers:
                    self.type = "schedule"
                    self.start_time = words[i + 1]
                else:
                    self.type = "info"

                del_i.add(i)
                del_i.add(i + 1)
                i += 1
                continue

            for table in tables:
                if table in words[i]:
                    self.type = "list"
                    del_i.add(i)
                    del_i.add(i + 1)
                    i += 1
                    f = True
                    break
            if f:
                continue

            if "زمان" == words[i] and "بندی" == words[i + 1]:
                self.type = "list"
                del_i.add(i)
                del_i.add(i + 1)
                del_i.add(i + 2)
                i += 2
                continue

            for info in infos:
                if info in words[i]:
                    self.type = "info"
                    del_i.add(i)
                    f = True
                    break
            if f:
                continue

            if words[i] in source:
                self.source = words[i]
                del_i.add(i)
                continue

            if episode in words[i]:
                if words[i + 1] in numbers or words[i + 1].isdigit():
                    self.episode = words[i + 1]
                    del_i.add(i)
                    del_i.add(i + 1)
                    i += 1
                    continue
                else:
                    self.episode = "0" + words[i + 1]
                    del_i.add(i)
                    del_i.add(i + 1)
                    i += 1
                    continue

        for i in sorted(del_i, reverse=True):
            temp_words.pop(i)

        tags = tagger.tag(temp_words)
        chunc = tree2brackets(chunker.parse(tags))

        chuncs_split = (''.join(chunc.split('['))).split(']')

        if self.type == (None,):
            self.type = "show"

        name = []
        for i in range(len(chuncs_split)):
            for film in films:
                if film in chuncs_split[i] and "NP" in chuncs_split[i]:
                    if len(chuncs_split[i].split(" ")) == 2:
                        if "NP" in chuncs_split[i + 1]:
                            for w in chuncs_split[i + 1].split(" "):
                                if "NP" not in w:
                                    name.append(w)
                    else:
                        for w in chuncs_split[i].split(" "):
                            if film not in w and "NP" not in w:
                                name.append(w)
        self.show_name = " ".join(name)


def run(command, iom, profile, map):
    tv = TV(map)
    tv.slot_filling(command)
    logging.debug(f"result of slot filling: \ncommand: {command}\nslot filling: {tv.getAll()}")
    if tv.get_source() == "telewebion":
        pass
        # tele api
        # tele convertor
        # if type
