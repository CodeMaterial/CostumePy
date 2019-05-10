import CostumePy

from CostumePy.UI import Button


class Radiator:

    def __init__(self, number):

        self.node = CostumePy.new_node("radiator_%i" % number)

        self.power = False

        power_command = "POWER_RAD_%i" % number

        self.node.listen(power_command, self.set_power)

        self.off_button = Button("Power: On", power_command, data=True, button_class="success")
        self.on_button = Button("Power: Off", power_command, data=False, button_class="danger")

        self.node.ui.set_elements(self.on_button)

    def set_power(self, msg):

        if msg["data"] == True:
            print("Turning on radiator")
            self.power = True
            self.node.ui.set_elements(self.off_button)
            print("The radiator is now on")


        elif msg["data"] == False:
            print("Turning off radiator")
            self.power = False
            self.node.ui.set_elements(self.on_button)
            print("The radiator is now off")


if __name__ == "__main__":

    for i in range(4):
        radiator = Radiator(i)