import pkgutil
import pandas as pd
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')


def saveData(text, label, path):
    logging.info('writing into csv ...')
    df = pd.read_csv(f'{path}/data.csv', index_col=0)
    temp = pd.DataFrame({'text': [text], 'intent': [label]})
    df = pd.concat([df, temp], ignore_index=True, axis=0)
    df.to_csv(f'{path}/data.csv', index=False)


class Manager:

    def __init__(self, profile, iom, mapper):
        self.profile = profile
        self.iom = iom
        self.map = mapper
        self._utils = None

    def updateMap(self):
        if self.profile.getNas():
            self.map.updateNas()
        self.map.update()

    def getUtils(self):
        locations = [self.map.getUtilsPath()]
        print(f"Looking for modules in: {locations[0]}")
        utils = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except Exception as e:
                logging.exception(e)
                print(f"Skipped module \'{name}\' due to an error.")
            else:
                print(f"Found module '{name}' with words: {mod.WORDS}")
                utils.append(mod)
        utils.sort(key=lambda mod: mod.PRIORITY, reverse=True)
        self._utils = utils

    def query(self, command):
        for util in self._utils:
            if util.isValid(command):
                print(f"util '{util.__name__}' validated")
                # confirm
                ok = input(f"do you want to use '{util.__name__}' util? (y/*) ")
                if ok != 'y' and ok != 'Y':
                    continue
                saveData(command, util.__name__, self.map.getDataPath())
                try:
                    return util.run(command, self.iom, self.profile, self.map)
                except Exception as e:
                    logging.exception(e)
                    self.iom.getSpeaker().say("عملیات با شکست مواجه شد!")
                finally:
                    return
        print(f"No util was able to run this command:\n \"{command}\"")
