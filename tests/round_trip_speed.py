import CostumePy
import time
import random

from callback_helpers import CallbackReceiver

cr = CallbackReceiver()

test_data = [random.random() for _ in range(3*1000)]

CostumePy.listen_to("ping", cr.func)
total = 0
for _ in range(1000):
    CostumePy.broadcast("ping", data=test_data)
    msg = cr.get_received()
    total += (time.time() - msg["created"])

print("round trip time per message of 3000 float values: %f seconds" % total/1000.0)
