import CostumePy

from CostumePy.UI import Button


class Radiator:

    def __init__(self):

        self.node = CostumePy.new_node("radiator")

        self.power = False

        self.node.listen("POWER_RAD", self.set_power)

        self.on_button = Button("Power: On", "POWER_RAD", data=False, button_class="btn-success")
        self.off_button = Button("Power: Off", "POWER_RAD", data=True, button_class="btn-danger")

        self.node.ui.set_elements(self.off_button)

    def set_power(self, msg):

        if msg["data"] == True:
            print("Turning on radiator")
            self.power = True
            self.node.ui.set_elements(self.on_button)
            print("The radiator is now on")

        elif msg["data"] == False:
            print("Turning off radiator")
            self.power = False
            self.node.ui.set_elements(self.off_button)
            print("The radiator is now off")


if __name__ == "__main__":

    import time

    radiator = Radiator()

    while radiator.node.running:
        time.sleep(10)
        radiator.set_power({"data": False})

    print("radiator has stopped")
