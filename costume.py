import logging
from CostumePy.system.event_manager import EventManager

def launch_costume(suit_config):

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)-5s] %(module)-20.20s %(processName)-15.15s %(message)s')

    eventManager = EventManager()

    suitFile = open(suit_config, "r")

    lines = suitFile.read().split("\n")

    for line in lines:
        parts = line.split(" -> ")
        if len(parts) == 2:
            path, moduleName = parts
            exec("from %s import %s" % (path, moduleName))
            module = eval(moduleName)
            eventManager.add_module(module)

    eventManager.start_modules()
    eventManager.start()
    logging.info("%s Launched!" % suit_config)

    return eventManager