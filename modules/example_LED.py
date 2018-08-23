import logging
from system.costume_modules import CostumeModule


class SingleLED(CostumeModule):

    def __init__(self):
        super().__init__(refresh_rate=1/30.0)
        self.listeners["BLUSH"] = self.blush
        self.blush_status = False

    def blush(self, event):

        if event.data == self.blush_status:
            logging.info("Requested state change invalid as state is already achieved")
            return

        if event.data:
            self.blush_status = True
            logging.info("blushing on")
        else:
            self.blush_status = False
            logging.info("blushing off")
