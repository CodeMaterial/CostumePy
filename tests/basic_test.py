import unittest
import CostumePy
import time
from importlib import reload


class CallbackReceiver:

    def __init__(self):
        self.received = []

    def func(self, msg):
        self.received.append(msg)

    def get_received(self, timeout=5, count=1):
        start = time.time()
        while ((time.time() - start) < timeout) and (len(self.received) < count):
            time.sleep(0.01)

        r = self.received
        self.received = []

        if len(r) == 0:
            return None
        elif len(r) == 1:
            return r[0]
        else:
            return r


cr = CallbackReceiver()


class SendReceiveTest(unittest.TestCase):

    def test_1_listen(self):
        reload(CostumePy)
        CostumePy.listen_to("test", cr.func)

    def test_2_broadcast(self):
        CostumePy.broadcast("test", data=True)

    def test_3_response(self):
        msg = cr.get_received()
        self.assertEqual(type(msg), dict, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEqual(msg["delay"], 0)
        self.assertEqual(msg["topic"], "test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")

    def test_4_stop(self):
        CostumePy.stop()


class DelayTest(unittest.TestCase):

    def test_1_listen(self):
        reload(CostumePy)
        CostumePy.listen_to("test", cr.func)

    def test_2_broadcast(self):
        CostumePy.broadcast("test", data=True, delay=3)

    def test_3_response(self):
        msg = cr.get_received(timeout=5)
        self.assertEqual(type(msg), dict, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEqual(msg["delay"], 3)
        self.assertEqual(msg["topic"], "test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")

    def test_4_stop(self):
        CostumePy.stop()


class BulkTest(unittest.TestCase):

    def test_1_listen(self):
        reload(CostumePy)
        CostumePy.listen_to("test", cr.func)

    def test_2_broadcast(self):
        for _ in range(100):
            CostumePy.broadcast("test", data=True)

    def test_3_response(self):
        msg = cr.get_received(timeout=5, count=100)
        self.assertEqual(type(msg), list, msg="Message timeout reached. No messages received")
        self.assertEquals(len(msg), 100)

    def test_4_stop(self):
        CostumePy.stop()


if __name__ == '__main__':
    loader = unittest.TestLoader()
    send_receive_suite = loader.loadTestsFromTestCase(SendReceiveTest)
    delay_suite = loader.loadTestsFromTestCase(SendReceiveTest)
    bulk_suite = loader.loadTestsFromTestCase(BulkTest)
    unittest.TextTestRunner().run([send_receive_suite, delay_suite, bulk_suite])
