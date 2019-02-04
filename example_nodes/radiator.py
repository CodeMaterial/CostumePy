import CostumePy

from CostumePy.UI import Button, Slider, Dropdown


class Radiator:

    def __init__(self, number):

        self.node = CostumePy.new_node("radiator_%i" % number)
        self.ui = self.node.ui

        self.power = False
        self.mode = "Constant"
        self.target_temp = 20

    def set_listeners(self):

        self.node.listen("POWER", self.set_power)
        self.node.listen("MODE", self.set_mode)
        self.node.listen("TEMP_TARGET", self.set_target_temp)

    def setup_ui(self):

        on_button = Button("Power On", "POWER", data=True)

        off_button = Button("Power Off", "POWER", data=False)
        mode_dropdown = Dropdown("Mode", "MODE", data_options=["Constant", "Pulsing", "Energy Saving"])
        thermostat_slider = Slider("Temperature", "TEMP_TARGET", data_min=10, data_max=30)

        self.ui.add_elements(on_button, off_button, mode_dropdown, thermostat_slider)

    def set_power(self, msg):

        if msg["data"] == True:
            print("Turning on radiator")
            self.power = True

        elif msg["data"] == False:
            print("Turning off radiator")
            self.power = False

        print("the radiator is now %s" % ("on" if self.power else "off"))

    def set_mode(self, msg):
        print("Setting the radiator mode to %s" % msg.data)
        self.mode = msg.data

    def set_target_temp(self, msg):
        print("Setting the radiator mode to %s" % msg.data)
        self.target_temp = msg.data


if __name__ == "__main__":

    for i in range(1):
        radiator = Radiator(i)
        radiator.set_listeners()
        radiator.setup_ui()