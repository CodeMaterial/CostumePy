import logging
import time
from CostumePy.system.event_manager import EventManager


def _set_logging(suit_name):

    logging_format = '%(asctime)s [%(levelname)-5s] %(processName)-10.10s -> %(module)-15.15s  %(message)s'

    logging.basicConfig(level=logging.INFO, format=logging_format)

    file_handler = logging.FileHandler("%s.log" % suit_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(logging_format))

    logging.getLogger().addHandler(file_handler)

    logging.info("-"*10+" Starting Costume "+"-"*10)


def launch_costume(suit_config, unit_test = True):

    start = time.time()

    _set_logging(suit_config.replace(".suit", ""))

    event_manager = EventManager()

    try:
        suit_file = open(suit_config, "r")
    except:
        logging.error("Cannot load %s" % suit_config)
        return

    lines = suit_file.read().split("\n")

    for line in lines:
        if not line.startswith("#"):
            parts = line.split(" -> ")
            if len(parts) == 2:
                path, module_name = parts
                exec("from %s import %s" % (path, module_name))
                module = eval(module_name)
                event_manager.add_module(module, unit_test=unit_test)

    event_manager.start_modules()
    event_manager.start()
    logging.info("%s launched in %0.2f seconds!" % (suit_config, time.time()-start))

    return event_manager
