import logging

from system.costume_modules import CostumeModule


class Emotions(CostumeModule):

    def __init__(self):
        super().__init__(refresh_rate=1/30.0)
        self.listeners["NOSE_PRESS"] = self.cute_input
        self.description = "The emotion module, nothing much to say"
        self.actions = {"cute": self.cute_input}

    def cute_input(self, event):
        logging.info("Cute input detected")
        self.broadcast("BLUSH", data=True)
        self.broadcast("BLUSH", data=False, delay=5)

