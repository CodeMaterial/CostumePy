import unittest
import CostumePy

class ServerConnectionTest(unittest.TestCase):

    def test_1_init(self):
        CostumePy.new_node("node_a")

    def test_2_quit(self):
        CostumePy.quit()