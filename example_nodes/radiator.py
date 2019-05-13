import CostumePy

class Radiator:

    def __init__(self):

        self.node = CostumePy.new_node("radiator")

        self.power = False

        self.node.listen("POWER_RAD", self.set_power)

        self.node.ui.add_button("power_button", "Power: Off", "POWER_RAD", data=True, button_class="btn-danger",
                                order=0)
        self.node.ui.add_button("power_button2", "Power: Off", "POWER_RAD", data=True, button_class="btn-danger",
                                order=0)
        self.node.ui.add_button("power_button3", "Power: Off", "POWER_RAD", data=True, button_class="btn-danger",
                                order=0)

        self.node.ui.add_break("some_break", order=50)

        self.node.ui.add_text("happyness", "I am happy")
        self.node.ui.update()

        self.node.listen("increment_lamp", self.lamp_activity)

    def lamp_activity(self, _):
        self.set_power({"data": True})

    def set_power(self, msg):

        if msg["data"] == True:
            self.power = True
            self.node.ui.get("happyness")["text"] = "I am happy"

            pb = self.node.ui.get("power_button")
            pb["text"] = "Power: On"
            pb["data"] = False
            pb["button_class"] = "btn-success"

            self.node.ui.update()

        elif msg["data"] == False:
            self.power = False
            self.node.ui.get("happyness")["text"] = "I am sad"

            pb = self.node.ui.get("power_button")
            pb["text"] = "Power: Off"
            pb["data"] = True
            pb["button_class"] = "btn-danger"

            self.node.ui.update()


if __name__ == "__main__":

    import time

    radiator = Radiator()

    while radiator.node.running:
        time.sleep(10)
        radiator.set_power({"data": False})
