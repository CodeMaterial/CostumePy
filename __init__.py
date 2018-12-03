import sys
import time
import logging
from CostumePy.system.cospy_node import CospyNode


def message(topic, data=None, delay=0, source=None):
    created = time.time()
    return {"source": source,
            "topic": topic,
            "data": data,
            "created": created,
            "delay": delay,
            "action_at": created + delay}


def get_node():
    global node
    if node is None:
        node = CospyNode(node_name)
    return node


def listen_to(topic, callback):
    get_node().listen_to(topic, callback)


def broadcast(topic, data=None, delay=0, source=None):
    msg = message(topic, data=data, delay=delay, source=source)
    get_node().broadcast_message(msg)


def broadcast_message(msg):
    get_node().broadcast_message(msg)


def set_logging_level(level):
    logging_format = '%(asctime)s [%(levelname)-5s]  %(message)s'
    logging.basicConfig(level=level, format=logging_format)


def set_node_name(new_name):
    global node_name
    node_name = new_name


def new_node(new_name):
    return CospyNode(new_name)

def stop():
    get_node().stop()

node = None
node_name = sys.argv[0]

set_logging_level(logging.INFO)
