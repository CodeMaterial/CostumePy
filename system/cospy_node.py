from multiprocessing.managers import BaseManager
import threading
# from message import Message
from CostumePy.system.message import Message


class QueueManager(BaseManager):
    pass


class CustomManager:

    def __init__(self, name):
        self.name = name
        self.listening_to = {}

        self._central_manager = self._get_central_manager()

        self.main_queue = self._central_manager.get_main_queue()
        self.module_queue = None

        self.callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self.callback_listener.start()


    def get_module_queue(self):
        return self._central_manager.get_module_queue(self.name)

    def _get_central_manager(self):

        central_manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'costume')
        central_manager.register('get_module_queue')
        central_manager.register('get_main_queue')
        central_manager.connect()
        return central_manager

    def listen_to(self, topic, callback):

        if self.module_queue is None:
            self.module_queue = self.get_module_queue()

        if topic not in self.listening_to:
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        self.broadcast("_listen_to", data={"topic": topic, "module_name": self.name})

    def _listen_for_callbacks(self):

        while True:
            if self.module_queue is not None:
                message = self.module_queue.get()
                topic = message.name
                callbacks = self.listening_to[topic]
                for callback in callbacks:
                    callback(message)

    def broadcast(self, topic, data=None):
        msg = Message(topic, data=data)
        print("broadcasting %r" % msg)
        self.main_queue.put(msg)
