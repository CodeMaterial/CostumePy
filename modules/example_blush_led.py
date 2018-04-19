import logging
from system.costume_modules import CostumeModule


class BlushLED(CostumeModule):

    def __init__(self):
        super().__init__(refresh_rate=1/30.0)
        self.listeners["BLUSH"] = self.blush
        self.blush_status = False
        self.actions = {"blush": self.blush}

    def blush(self, event):

        if event.data == self.blush_status:
            logging.info("Requested state change invalid as state is already achieved")
            return

        if event.data:
            self.blush_status = True
            self.broadcast("NOTIFY", data="Blushing!")
            logging.info("blushing on")
        else:
            self.blush_status = False
            self.broadcast("NOTIFY", data="Not blushing.")
            logging.info("blushing off")