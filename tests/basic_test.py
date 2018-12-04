import CostumePy
import time

def nose_press_function(msg):
    print("You pressed my nose %s!" % msg["data"])


CostumePy.listen_to("nose_press", nose_press_function)

CostumePy.broadcast("nose_press", data="hard")

time.sleep(1)
CostumePy.stop()