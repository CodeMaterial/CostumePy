import threading
from CostumePy.system.message import Message
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


class CospyNode:

    def __init__(self, name):
        self.name = name
        self.listening_to = {}

        self._cospy_manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'costume')

        self._cospy_manager.register('get_node_queue')
        self._cospy_manager.register('get_main_queue')
        self._cospy_manager.connect()

        self._main_queue = self._cospy_manager.get_main_queue()
        self._node_queue = None

        self._callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self._callback_listener.start()


    def _get_node_queue(self):
        return self._cospy_manager.get_node_queue(self.name)

    def listen_to(self, topic, callback):

        if self._node_queue is None:
            self._node_queue = self._get_node_queue()

        if topic not in self.listening_to:
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        self.broadcast("_listen_for", data={"topic": topic, "node_name": self.name})

    def _listen_for_callbacks(self):

        while True:
            if self._node_queue is not None:
                if not self._node_queue.empty():
                    msg = self._node_queue.get()
                    if msg.topic in self.listening_to:
                        callbacks = self.listening_to[msg.topic]
                        for callback in callbacks:
                            callback(msg)

    def broadcast(self, topic, data=None):
        msg = Message(topic, data=data)
        self._main_queue.put(msg)
