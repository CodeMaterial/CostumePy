import threading
import logging
import zmq
from CostumePy.system.message import message

class CospyNode:

    def __init__(self, name):
        self.name = name
        self.listening_to = {}

        self.set_logging_level(logging.INFO)
        self.zmq_context = zmq.Context()

        self.manager_sock = self.zmq_context.socket(zmq.PAIR)
        self.manager_sock.connect(self.request_ip())

        self._callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self._callback_listener.start()

    def request_ip(self):
        socket = self.zmq_context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5556")
        socket.send_string(self.name)
        return socket.recv().decode('UTF-8')


    def set_logging_level(self, logging_level):
        logging_format = '%(asctime)s [%(levelname)-5s]  %(message)s'
        logging.basicConfig(level=logging_level, format=logging_format)


    def listen_to(self, topic, callback):
        logging.info("Setting up listening callbacks for %s" % topic)

        if topic not in self.listening_to:
            logging.info("Topic %s is not currently being listened to by this node, initialising." % topic)
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        listen_msg = message("_listen_for", data=topic)
        self.broadcast_message(listen_msg)

    def _listen_for_callbacks(self):

        logging.info("Listening for callbacks")
        while True:
            try:
                msg = self.manager_sock.recv_json(flags=zmq.NOBLOCK)
                if msg["topic"] in self.listening_to:
                    callbacks = self.listening_to[msg["topic"]]
                    for callback in callbacks:
                        callback(msg)

            except zmq.Again:
                pass


    def broadcast_message(self, msg):
        if msg["source"] is None:
            msg["source"] = self.name

        logging.debug("Broadcasting message %r" % msg)
        self.manager_sock.send_json(msg)
