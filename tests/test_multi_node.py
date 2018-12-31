import unittest
import CostumePy
import time
from importlib import reload
from tests.callback_helpers import CallbackReceiver


cr = CallbackReceiver()


class MultiNodeTest(unittest.TestCase):

    def test_1_init(self):
        reload(CostumePy)
        cr.node_a = CostumePy.new_node("node_a")
        cr.node_b = CostumePy.new_node("node_b")

    def test_2_listen(self):
        cr.node_a.listen("multi_node_test", cr.func)

    def test_3_broadcast(self):
        cr.node_b.broadcast("multi_node_test", data=True)

    def test_3_response(self):
        msg = cr.get_received()
        self.assertEqual(type(msg), dict, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEqual(msg["delay"], 0)
        self.assertEqual(msg["topic"], "multi_node_test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")

    def test_4_quit(self):
        CostumePy.quit()
