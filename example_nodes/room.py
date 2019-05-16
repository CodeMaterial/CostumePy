import CostumePy
import time


class Room:

    def __init__(self):

        self.node = CostumePy.new_node("room")

        self.temperature = 20

        self.node.listen("HEAT", self.heat)

        self.node.ui.add_text("temp", order=0)
        self.node.ui.add_break("break", order=1)
        self.node.ui.add_button("fan_room", text="Fan Room", topic="HEAT", data=False)

        self.node.ui.update()

    def heat(self, msg):

        self.temperature += 1 if msg["data"] else -1

        self.node.broadcast("ENVIRONMENT", data={"temperature": self.temperature})

        self.node.ui.elements["temp"]["text"] = "Current temperature: %i" % self.temperature
        self.node.ui.update()


class Window:

    def __init__(self):

        self.node = CostumePy.new_node("window")

        self.window_open = False

        self.node.listen("TOGGLE_WINDOW", self.toggle_window)

        self.node.ui.add_button("open_window", text="Open Window", topic="TOGGLE_WINDOW")
        self.node.ui.update()

    def toggle_window(self, _):

        self.window_open = not self.window_open

        self.node.ui.get("open_window")["text"] = "Close Window" if self.window_open else "Open Window"
        self.node.ui.update()

    def run(self):

        while self.node.running:
            if self.window_open:
                self.node.broadcast("HEAT", data=False)
            time.sleep(1)

if __name__ == "__main__":

    r = Room()

    w = Window()

    w.run()