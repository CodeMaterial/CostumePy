class UI:

    def __init__(self, commands, state):  # commands = {"do something":acceptable response}, State = {"item":state}
        self.commands = commands
        self.state = state
