import logging
import time
from CostumePy.system.event_manager import EventManager

def set_logging():

    logging_format = '%(asctime)s [%(levelname)-5s] %(processName)-10.10s -> %(module)-15.15s  %(message)s'

    logging.basicConfig(level=logging.INFO, format=logging_format)

    file_handler = logging.FileHandler("costume.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(logging_format))

    logging.getLogger().addHandler(file_handler)


def launch_costume(suit_config):

    start = time.time()

    set_logging()

    event_manager = EventManager()

    suitFile = open(suit_config, "r")

    lines = suitFile.read().split("\n")

    for line in lines:
        parts = line.split(" -> ")
        if len(parts) == 2:
            path, moduleName = parts
            exec("from %s import %s" % (path, moduleName))
            module = eval(moduleName)
            event_manager.add_module(module)

    event_manager.start_modules()
    event_manager.start()
    logging.info("%s launched in %0.2f seconds!" % (suit_config, time.time()-start))

    return event_manager