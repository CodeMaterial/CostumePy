import CostumePy

from CostumePy.UI import Button, Text


class Radiator:

    def __init__(self):

        self.node = CostumePy.new_node("radiator")

        self.power = False

        self.node.listen("POWER_RAD", self.set_power)

        self.on_button = Button("power_button", "Power: Off", "POWER_RAD", data=True, button_class="btn-danger")
        self.off_button = Button("power_button", "Power: On", "POWER_RAD", data=False, button_class="btn-success")

        self.node.ui.add_elements(self.on_button, Text("happyness", "I am happy"))

    def set_power(self, msg):

        if msg["data"] == True:
            self.power = True
            self.node.ui.elements["happyness"].text = "I am happy"
            self.node.ui.replace("power_button", self.off_button)

        elif msg["data"] == False:
            self.power = False
            self.node.ui.elements["happyness"].text = "I am sad"
            self.node.ui.replace("power_button", self.on_button)


if __name__ == "__main__":

    import time

    radiator = Radiator()

    while radiator.node.running:
        time.sleep(10)
        radiator.set_power({"data": False})
