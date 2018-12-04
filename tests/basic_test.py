import unittest
import CostumePy
import time


class CallbackReceiver:

    def __init__(self):
        self.received = None

    def func(self, msg):
        self.received = msg

    def get_received(self, timeout=1):
        start = time.time()
        while (time.time() - start < timeout) and self.received is None:
            time.sleep(0.1)

        return self.received


cr = CallbackReceiver()


class SendReceiveTest(unittest.TestCase):

    def test_name(self):
        self.assertIn('unittest', CostumePy.node_name)

    def test_listen(self):
        CostumePy.listen_to("test", cr.func)

    def test_init(self):
        self.assertIn('unittest', CostumePy.get_node().name)

    def test_broadcast(self):
        CostumePy.broadcast("test", data=True)

    def test_response(self):
        msg = cr.get_received()
        self.assertNotEqual(msg, None, msg="Message timeout reached. No messages received")
        self.assertTrue(msg["data"], msg="Message data has been modified")
        self.assertEquals(msg["delay"], 0)
        self.assertEquals(msg["topic"], "test", msg="Incorrect topic: %s" % msg["topic"])
        self.assertLessEqual(msg["action_at"], time.time(), msg="Message was actioned too early")
        self.assertIn("unittest", msg["source"], msg="Incorrect message source: %s" % msg["source"])

    def test_stop(self):
        CostumePy.stop()


if __name__ == '__main__':

    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing(None)
    suite = loader.loadTestsFromTestCase(SendReceiveTest)
    unittest.TextTestRunner().run(suite)
