from system.events import Event
from modules.example_button import Button
from system.unit_test import UnitTest


class ButtonTest(UnitTest):

    def __init__(self):
        super().__init__(Button)

    def test_blush(self):

        self.send_input(Event("NOSE_PRESS", data=True))
        self.check_output(Event("BLUSH"))

    def test_blush_shutdown(self):

        self.send_input(Event("NOSE_PRESS", data=True))
        self.check_output(Event("BLUSH", data=True))
        self.check_output(Event("BLUSH", data=False, delay=5))
