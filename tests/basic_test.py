import unittest
import CostumePy
import time


class CallbackReceiver:

    def __init__(self):
        self.received = None

    def func(self, msg):
        self.received = msg

    def get_received(self, timeout=5):
        start = time.time()
        while ((time.time() - start) < timeout) and (self.received is None):
            time.sleep(0.1)

        return self.received


cr = CallbackReceiver()


class SendReceiveTest(unittest.TestCase):

    def test_1_listen(self):
        CostumePy.listen_to("test", cr.func)

    def test_2_broadcast(self):
        CostumePy.broadcast("test", data=True)

    def test_3_response(self):
        msg = cr.get_received()
        self.assertNotEqual(msg, None, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEquals(msg["delay"], 0)
        self.assertEquals(msg["topic"], "test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")

    def test_4_stop(self):
        CostumePy.stop()


if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(SendReceiveTest)
    unittest.TextTestRunner().run(suite)
