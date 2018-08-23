import logging
from system.event_manager import EventManager
from system.events import Event
import sys
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)-5s] %(module)-20.20s %(processName)-15.15s %(message)s')

if __name__ == "__main__":
    eventManager = EventManager()

    suitName = sys.argv[1]

    suitFile = open(suitName, "r")

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
