import sys
import time
import logging
from CostumePy.cospy_node import CospyNode
from CostumePy.UI import Button


nodes = []
node_name = sys.argv[0]


def message(topic, data=None, delay=0):
    created = time.time()
    return {"source": None,
            "topic": topic,
            "data": data,
            "created": created,
            "delay": delay,
            "action_at": created + delay}


def get_node():
    global nodes
    if len(nodes) == 0:
        nodes.append(CospyNode(node_name))
    return nodes[-1]


def listen(topic, callback):
    get_node().listen(topic, callback)


def broadcast(topic, data=None, delay=0):
    get_node().broadcast(topic, data=data, delay=delay)


def broadcast_message(msg):
    get_node().broadcast_message(msg)


def set_logging_level(level):
    logging_format = '%(asctime)s [%(levelname)-5s]  %(message)s'
    logging.basicConfig(level=level, format=logging_format)


def set_node_name(new_name):
    global node_name
    node_name = new_name


def new_node(new_name):
    global nodes
    nodes.append(CospyNode(new_name))
    return get_node()


def quit():
    global nodes
    for node in nodes:
        node.quit()


def add_button(name, topic, data=None):

    button = Button(name, topic, data=data)

    get_node().ui.add_elements(button)


def add_state(name, topic):
    raise NotImplementedError


def add_slider(name, topic, min_val=0, max_val=1, data=None):
    raise NotImplementedError


def add_dropdown(name, topic, data=None):
    raise NotImplementedError



set_logging_level(logging.INFO)
