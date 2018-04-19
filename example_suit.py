import logging
import time

from system.event_manager import EventManager
from modules.example_blush_led import BlushLED
from modules.example_emotions import Emotions
from modules.example_telegram import Telegram

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)-5s] %(module)-20.20s %(processName)-15.15s %(message)s')

if __name__ == "__main__":
    eventManager = EventManager()

    eventManager.add_module(Emotions)
    eventManager.add_module(BlushLED)
    eventManager.add_module(Telegram)

    eventManager.start_modules()
    eventManager.start()

    time.sleep(1)
    eventManager.broadcast("NOSE_PRESS", data=True)
