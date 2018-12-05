import time

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