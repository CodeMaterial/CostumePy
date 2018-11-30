from CostumePy.system.cospy_node import CustomManager

cm = CustomManager(__file__)

def listen_to(topic, callback):
    cm.listen_to(topic, callback)


def broadcast(topic, data=None):
    cm.broadcast(topic, data=data)