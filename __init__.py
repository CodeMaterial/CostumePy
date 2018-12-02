import sys
from CostumePy.system.cospy_node import CospyNode
from CostumePy.system.message import message

node = None
node_name = sys.argv[0]


def get_node():
    global node
    if node is None:
        node = CospyNode(node_name)

    return node


def listen_to(topic, callback):
    get_node().listen_to(topic, callback)


def broadcast(topic, data=None, delay=0, source=None):
    msg = message(topic, data=data, delay=float(delay), source=source)
    get_node().broadcast_message(msg)


def broadcast_message(msg):
    get_node().broadcast_message(msg)


def set_logging_level(level):
    get_node().set_logging_level(level)


def set_node_name(new_name):
    global node_name
    node_name = new_name


