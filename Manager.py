import pkgutil


class Manager:

    def __init__(self, profile, speaker, mapper):
        self.profile = profile
        self.speaker = speaker
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
                print("Error:", e)
                print(f"Skipped module \'{name}\' due to an error.")
            else:
                print(f"Found module '{name}' with words: {mod.WORDS}")
                utils.append(mod)
        utils.sort(key=lambda mod: mod.PRIORITY, reverse=True)
        self._utils = utils

    def query(self, command):
        for utils in self._utils:
            if utils.isValid(command):
                print(f"util '{utils.__name__}' validated")
                try:
                    utils.run(command, self.speaker, self.profile)
                except Exception as e:
                    print(e)
                    print('Failed to execute util')
                    self.speaker.say("I'm sorry. I had some trouble with " +
                                     "that operation. Please try again later.")
                finally:
                    return
        print(f"No util was able to run this command:\n \"{command}\"")
