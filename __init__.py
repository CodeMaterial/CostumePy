from CostumePy.system.cospy_node import CospyNode

node = CospyNode(__file__)

def listen_to(topic, callback):
    node.listen_to(topic, callback)


def broadcast(topic, data=None):
    node.broadcast(topic, data=data)


def broadcast_message(msg):
    node.broadcast_message(msg)