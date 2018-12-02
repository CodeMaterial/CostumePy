import sys
from CostumePy.system.cospy_node import CospyNode
from CostumePy.system.message import Message


def listen_to(topic, callback):
    node.listen_to(topic, callback)

def broadcast(topic, data=None, delay=0, source=None):
    msg = Message(topic, data=data, delay=float(delay), source=source)
    node.broadcast_message(msg)


def broadcast_message(msg):
    node.broadcast_message(msg)

def set_logging_level(level):
    node.set_logging_level(level)

def set_node_name(new_name):
    node.name = new_name

node = CospyNode(sys.argv[0])

