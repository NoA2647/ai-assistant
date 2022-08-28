import re

import wikipedia
import webbrowser
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')

KEYWORDS = ["ویکی", "ویکی پدیا"]

PRIORITY = 6

EXCLUDED_IMAGES = [
    'https://upload.wikimedia.org/wikipedia/commons/7/73/Blue_pencil.svg'
]


def wiki_image(page):
    images = [i for i in page.images if i not in EXCLUDED_IMAGES]
    if len(images) > 0:
        return images[0]
    else:
        return ''


def wiki_page_summary(topic, auto_suggest):
    lines = 2
    summary = wikipedia.summary(topic, lines, auto_suggest=auto_suggest)

    if "==" in summary or len(summary) > 250:
        # We hit the end of the article summary or hit a really long
        # one.  Reduce to first line.
        lines = 1
        summary = wikipedia.summary(topic, lines, auto_suggest=auto_suggest)

    # Clean text to make it more speakable
    return re.sub(r'\([^)]*\)|/[^/]*/', '', summary), lines


class WIKI:
    def __init__(self, lang_code='fa'):
        self._lang_code = lang_code
        self._page = None
        wikipedia.set_lang(self._lang_code)

    class Page:
        def __init__(self, topic=None, auto_suggest=True):
            self.summary, self.lines = wiki_page_summary(topic, auto_suggest)

            self.image = wiki_image(wikipedia.page(topic, auto_suggest=auto_suggest))
            self.auto_suggest = auto_suggest
            self.topic = topic

    def wiki_lookup(self, search, auto_suggest=True):
        try:
            topics = wikipedia.search(search, 5)
            print(topics)
            if len(topics) == 0:
                return None

            self._page = self.Page(topics[0], auto_suggest)
            return True

        except wikipedia.PageError:
            return None
        except Exception as e:
            logging.error(e)
            return None

    def random(self):
        try:
            topics = wikipedia.random(3)

            self._page = self.Page(topics[0])
            return True

        except wikipedia.PageError:
            return None
        except Exception as e:
            logging.error(e)
            return None

    def more(self):
        page = wikipedia.page(self._page.topic)
        return page.content

    def show_image(self):
        return self._page.image

    def summary(self):
        return self._page.summary

    def open_page(self):
        return webbrowser.open(self._page.url)


def run(command, iom, profile, map):
    wiki = WIKI()
    wiki.wiki_lookup(command)
    summary = wiki.summary()
    print(summary)
    iom.speaker.say(summary)
    url = wiki.show_image()
    webbrowser.open(url)
    # if user wants more detail
    # print(wiki.more())

