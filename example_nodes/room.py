import CostumePy
import time


class Room:

    def __init__(self):

        self.node = CostumePy.new_node("room")

        self.temperature = 20

        self.node.listen("HEAT", self.heat)

        self.node.ui.add_text("temp")

        self.node.ui.add_button("fan_room", text="Fan Room", topic="HEAT", data=False)

        self.node.ui.update()

    def heat(self, msg):
        self.temperature += 1 if msg["data"] else -1
        self.node.broadcast("ENVIRONMENT", data={"temperature": self.temperature})
        self.node.ui.elements["temp"]["text"] = "Current temperature: %i" % self.temperature
        self.node.ui.update()


if __name__ == "__main__":

    r = Room()