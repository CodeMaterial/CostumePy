import CostumePy

from CostumePy.UI import Button


class Radiator:

    def __init__(self, number):

        self.node = CostumePy.new_node("radiator_%i" % number)
        self.ui = self.node.ui

        self.power = False
        self.mode = "Constant"
        self.target_temp = 20

        topic = "POWER_RAD_%i" % number

        self.node.listen(topic, self.set_power)

        on_button = Button("Power On", topic, data=True)
        off_button = Button("Power Off", topic, data=False)

        self.ui.add_elements(on_button, off_button)

    def set_power(self, msg):

        if msg["data"] == True:
            print("Turning on radiator")
            self.power = True

        elif msg["data"] == False:
            print("Turning off radiator")
            self.power = False

        print("the radiator %s is now %s" % (self.node.name, ("on" if self.power else "off")))



if __name__ == "__main__":

    for i in range(4):
        radiator = Radiator(i)