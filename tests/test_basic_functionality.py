import unittest
import CostumePy
import time
from importlib import reload
from tests.callback_helpers import CallbackReceiver

cr = CallbackReceiver()


class SendReceiveTest(unittest.TestCase):

    def test_1_listen(self):
        reload(CostumePy)
        CostumePy.listen("test", cr.func)

    def test_2_broadcast(self):
        CostumePy.broadcast("test", data=True)

    def test_3_response(self):
        msg = cr.get_received()
        self.assertEqual(type(msg), dict, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEqual(msg["delay"], 0)
        self.assertEqual(msg["topic"], "test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")

    def test_4_quit(self):
        CostumePy.quit()


class DelayTest(unittest.TestCase):

    def test_1_listen(self):
        reload(CostumePy)
        CostumePy.listen("test", cr.func)

    def test_2_broadcast(self):
        CostumePy.broadcast("test", data=True, delay=3)

    def test_3_response(self):
        msg = cr.get_received(timeout=5)
        self.assertEqual(type(msg), dict, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEqual(msg["delay"], 3)
        self.assertEqual(msg["topic"], "test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")

    def test_4_quit(self):
        CostumePy.quit()


class BulkTest(unittest.TestCase):

    def test_1_listen(self):
        reload(CostumePy)
        CostumePy.listen("test", cr.func)

    def test_2_broadcast(self):
        for _ in range(100):
            CostumePy.broadcast("test", data=True)

    def test_3_response(self):
        msg = cr.get_received(timeout=5, count=100)
        self.assertEqual(type(msg), list, msg="Message timeout reached. No messages received")
        self.assertEqual(len(msg), 100)

    def test_4_quit(self):
        CostumePy.quit()
