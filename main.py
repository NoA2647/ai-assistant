from Manager import Manager
from iom.IOM import IOM
from Profile import Profile
from Map import Map
import logging

logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')

def run_ai():
    mapper = Map()
    logging.info('Mapper init ...')
    iom = IOM(mapper)
    logging.info('IOM init ...')
    profile = Profile(mapper)
    profile.readProfile()
    logging.info('Profile init ...')
    manager = Manager(profile, iom, mapper)
    manager.updateMap()
    logging.info('manager init ...')
    manager.getUtils()
    logging.info('utils init ...')
    while True:
        # command = "transfer file to me"
        # path = iom.getScreen().record()
        command = iom.getListener().listenSilence()
        manager.query(command)
        # sys.exit()


run_ai()
