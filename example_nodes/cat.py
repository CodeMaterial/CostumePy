import CostumePy


class Cat:

    def __init__(self):

        self.node = CostumePy.new_node("cat")

        self.node.ui.add_text("description", text="I am a cat")

        self.node.listen("ENVIRONMENT", self.env_change)

        self.node.ui.update()

    def env_change(self, msg):

        if msg["data"]["temperature"] > 30:
            self.node.quit()


if __name__ == "__main__":

    c = Cat()