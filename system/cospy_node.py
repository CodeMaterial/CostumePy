import threading
import logging
from CostumePy.system.message import Message
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


class CospyNode:

    def __init__(self, name, manager_ip='127.0.0.1', manager_key='costume'):
        self.name = name
        self.listening_to = {}

        self.set_logging_level(logging.INFO)

        try:
            logging.info("Connecting to Cospy Manager")
            self._cospy_manager = QueueManager(address=(manager_ip, 50000), authkey=manager_key.encode('UTF-8'))

            self._cospy_manager.register('get_node_queue')
            self._cospy_manager.register('get_main_queue')
            self._cospy_manager.connect()
            self._main_queue = self._cospy_manager.get_main_queue()
            logging.info("Connected to Cospy Manager")

        except (ConnectionRefusedError, AssertionError) as e:
            logging.error("Cannot connect to CostumePy Manager. Has it been started?")
            quit()

        self._node_queue = None

        self._callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self._callback_listener.start()

    def set_logging_level(self, logging_level):
        logging_format = '%(asctime)s [%(levelname)-5s]  %(message)s'
        logging.basicConfig(level=logging_level, format=logging_format)

    def _get_node_queue(self):
        logging.info("Requesting dedicated node queue from Cospy manager")
        return self._cospy_manager.get_node_queue(self.name)

    def listen_to(self, topic, callback):
        logging.info("Setting up listening callbacks for %s" % topic)

        if self._node_queue is None:
            self._node_queue = self._get_node_queue()

        if topic not in self.listening_to:
            logging.info("Topic %s is not currently being listened to by this node, initialising." % topic)
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        listen_msg = Message("_listen_for", data={"topic": topic, "node_name": self.name})
        self.broadcast_message(listen_msg)

    def _listen_for_callbacks(self):

        logging.info("Listening for callbacks")
        while True:
            if self._node_queue is not None:
                if not self._node_queue.empty():
                    msg = self._node_queue.get()
                    if msg.topic in self.listening_to:
                        callbacks = self.listening_to[msg.topic]
                        for callback in callbacks:
                            callback(msg)

    def broadcast_message(self, msg):
        if msg.source is None:
            msg.source = self.name
        logging.info("Broadcasting message %r" % msg)
        self._main_queue.put(msg)
