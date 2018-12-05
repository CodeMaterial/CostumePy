import CostumePy
import time
import random
import sys
from callback_helpers import CallbackReceiver

cr = CallbackReceiver()
if len(sys.argv) != 3:
	print("Please enter the number of random float values per message and the total number of messages as arguments")
	quit()

items = int(sys.argv[1])
loops = int(sys.argv[2])

test_data = [random.random() for _ in range(items)]

CostumePy.listen_to("ping", cr.func)
total = 0
for _ in range(loops):
    CostumePy.broadcast("ping", data=test_data)
    msg = cr.get_received()
    total += (time.time() - msg["created"])

print("Round trip time to server and back per message of %i float values: %f seconds (%i fps)" % (items, total/loops, int(loops/total)))

CostumePy.stop()
