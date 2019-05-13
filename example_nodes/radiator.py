import CostumePy
import time


class Radiator:

    def __init__(self):

        self.node = CostumePy.new_node("radiator")

        self.power = False

        self.node.listen("POWER_RAD", self.set_power)

        self.node.ui.add_button("power_button", text="Power: Off", topic="POWER_RAD", data=True, button_class="btn-danger",
                                order=0)

        self.node.ui.update()

    def set_power(self, msg):

        if msg["data"] != self.power:

            self.power = msg["data"]

            pb = self.node.ui.get("power_button")

            pb["text"] = "Power: On" if self.power else "Power: Off"
            pb["button_class"] = "btn-success" if self.power else "btn-danger"
            pb["data"] = not self.power

            self.node.ui.update()

    def run(self):

        while self.node.running:
            time.sleep(1)
            if self.power:
                self.node.broadcast("HEAT", data=True)


if __name__ == "__main__":

    r = Radiator()

    r.run()