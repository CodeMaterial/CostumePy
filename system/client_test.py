from multiprocessing.managers import BaseManager
from message import Message

import threading

class QueueManager(BaseManager):
    pass


class CustomManager:

    def __init__(self, name):
        self.name = name

        self._central_manager = self._get_central_manager()

        self.main_queue = self._central_manager.get_main_queue()
        self.module_queue = self._central_manager.get_module_queue(self.name)

        self.callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self.callback_listener.start()

        self.listening_to = {}

    def _get_central_manager(self):

        central_manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'costume')
        central_manager.register('get_module_queue')
        central_manager.register('get_main_queue')
        central_manager.connect()
        return central_manager

    def listen_to(self, topic, callback):
        if topic not in self.listening_to:
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        self.broadcast("_listen_to", data={"topic": topic, "module_name": self.name})

    def _listen_for_callbacks(self):

        while True:
            msg = self.module_queue.get()
            topic = msg.name
            callbacks = self.listening_to[topic]
            for callback in callbacks:
                callback(msg)

    def broadcast(self, topic, data=None):
        msg = Message(topic, data=data)
        print("broadcasting %r" % msg)
        self.main_queue.put(msg)





def callback_fx(message):
    print("got the message! ", message)


cm = CustomManager("client_test")

cm.listen_to("greeting", callback_fx)

cm.broadcast("greeting", data="hello from client test new")

