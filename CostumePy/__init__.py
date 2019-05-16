import time
import logging
from CostumePy.cospy_node import CospyNode

nodes = []

def message(topic, data=None, delay=0):
    created = time.time()
    return {"source": None,
            "topic": topic,
            "data": data,
            "created": created,
            "delay": delay,
            "action_at": created + delay}


def set_logging_level(level):
    logging_format = '%(asctime)s [%(levelname)-5s]  %(message)s'
    logging.basicConfig(level=level, format=logging_format)


def new_node(new_name):
    global nodes
    n = CospyNode(new_name)
    nodes.append(n)
    return n


def quit():
    global nodes
    for node in nodes:
        node.quit()


set_logging_level(logging.ERROR)
