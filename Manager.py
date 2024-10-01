import pkgutil
import pandas as pd
import logging
import os
import json
from hazm import *

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s',
                    encoding="utf-8")


def saveData(text, label, path):
    location = f'{path}/data.csv'
    if os.path.isfile(location):        
        logging.info('writing into csv ...')
        df = pd.read_csv(f'{path}/data.csv', index_col=0)
        temp = pd.DataFrame({'text': [text], 'intent': [label]})
        df = pd.concat([df, temp], ignore_index=True, axis=0)
        df.to_csv(f'{path}/data.csv', index=False)
    else:
        temp = pd.DataFrame({'text': [text], 'intent': [label]})
        temp.to_csv(location, index=False)


def find_intent(clean_text, intents):
    intents_score = {}
    keywords_set = set()

    # initialize intent_score
    for intent in intents:
        intents_score[intent['name']] = 0

    # scoring intents
    for intent in intents:
        for keyword in intent['keyWords']:
            if keyword in clean_text:
                intents_score[intent['name']] = intents_score[intent['name']] + 1
                keywords_set.add(keyword)

    logging.debug(f"intents score: {intents_score}")
    if max(intents_score.values()) != 0:
        return max(intents_score, key=intents_score.get), keywords_set
    else:
        return None


def find_subIntent(wordSet, modules):
    subIntents_score = {}

    # initialize subIntent_score
    for module in modules:
        subIntents_score[module.__name__] = 0

    # scoring subIntents
    for module in modules:
        for keyword in module.KEYWORDS:
            for word in wordSet:
                if keyword in word:
                    subIntents_score[module.__name__] = subIntents_score[module.__name__] + 1

    print(subIntents_score)
    # max(subIntents_score, key=subIntents_score.get)
    logging.debug(f"subIntents score: {subIntents_score}")
    if max(subIntents_score.values()) != 0:
        return [key for key in subIntents_score.keys() if subIntents_score[key] >= 1]
    else:
        return None


def preprocess_text(text, stopWords):
    word_tokens = word_tokenize(text)

    filtered_sentence = [w for w in word_tokens if w not in stopWords]

    return ' '.join(filtered_sentence)


class Manager:

    def __init__(self, profile, iom, mapper):
        self.profile = profile
        self.iom = iom
        self.map = mapper
        self._utils = None
        self.stopWords = []

        with open(os.path.join(mapper.getDataPath(), 'stopWords.txt'), 'r', encoding="utf8") as f:
            for lines in f.readlines():
                self.stopWords.append(lines[:-1])
        f.close()

        with open(os.path.join(mapper.getDataPath(), 'intents.json'), encoding="utf8") as f:
            file = json.load(f)

        logging.info("Reading stopwords and intent file ...")
        self.intents = file['intents']
        f.close()

    def updateMap(self):
        if self.profile.getNas():
            self.map.updateNas()
        self.map.update()

    def getUtils(self):
        root = self.map.getUtilsPath()
        print(f"Looking for modules in: {root}")
        logging.debug(f"looking for modules in {root}")
        utils = {}
        intentFiles = os.listdir(root)
        for intent in intentFiles:
            utils[intent] = []
        for intent in intentFiles:
            path = [os.path.join(root, intent)]
            for finder, name, ispkg in pkgutil.walk_packages(path):
                try:
                    loader = finder.find_module(name)
                    mod = loader.load_module(name)
                except Exception as e:
                    logging.exception(e)
                    print(f"Skipped module \'{intent}/{name}\' due to an error.")
                else:
                    print(f"Found module \'{intent}/{name}\'")
                    utils[intent].append(mod)
            utils[intent].sort(key=lambda mod: mod.PRIORITY, reverse=True)
        self._utils = utils
        print(utils)
        logging.info("Modules found ...")

    def query(self, command):
        clean_text = preprocess_text(command, self.stopWords)
        logging.debug(f"preprocess text: {clean_text}")
        result = find_intent(clean_text, self.intents)
        logging.debug(f"intents: {result}")
        if result is not None:
            tasks = find_subIntent(result[1], self._utils[result[0]])
            if tasks is not None:
                for task in tasks:
                    for util in self._utils[result[0]]:
                        if util.__name__ == task:
                            print(f"util '{util.__name__}' validated")
                            logging.debug(f"util '{util.__name__}' validated")
                            # confirm
                            ok = input(f"do you want to use '{util.__name__}' util? (y/*) ")
                            if ok != 'y' and ok != 'Y':
                                break
                            saveData(command, util.__name__, self.map.getDataPath())
                            try:
                                logging.debug(f"util '{util.__name__}' ran")
                                return util.run(command, self.iom, self.profile, self.map)
                            except Exception as e:
                                logging.exception(e)
                                self.iom.getSpeaker().say("عملیات با شکست مواجه شد!")

            print(f"No util was able to run this command:\n \"{command}\"")
            logging.debug(f"No util was able to run this command:\n \"{command}\"")

        else:
            print("No intent detected")
            logging.debug("No intent detected")
