import threading
import logging
import zmq
import CostumePy
import socket


class CospyNode:

    def __init__(self, name):
        self.name = name
        self.listening_to = {}
        self.running = True

        self._zmq_context = zmq.Context()

        self.manager_sock = self._zmq_context.socket(zmq.PAIR)

        try:
            address = self._request_socket_ip()
            self.manager_sock.connect(address)
        except ConnectionRefusedError:
            raise


        self._callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self._callback_listener.start()

    def _request_socket_ip(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        manager_available = sock.connect_ex(('', 5556)) == 0
        if not manager_available:
            raise ConnectionRefusedError("Cannot contact manager, has it been started?")

        ip_socket = self._zmq_context.socket(zmq.REQ)
        ip_socket.connect("tcp://localhost:5556")
        ip_socket.send_string(self.name)

        ip_address = ip_socket.recv().decode('UTF-8')

        return ip_address

    def stop(self):
        self.running = False
        self._callback_listener.join()

    def listen_to(self, topic, callback):
        logging.info("Setting up listening callbacks for %s" % topic)

        if topic not in self.listening_to:
            logging.info("Topic %s is not currently being listened to by this node, initialising." % topic)
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        listen_msg = CostumePy.message("_listen_for", data=topic)
        self.broadcast_message(listen_msg)

    def _listen_for_callbacks(self):

        logging.info("Listening for callbacks")
        while self.running:
            try:
                msg = self.manager_sock.recv_json(flags=zmq.NOBLOCK)
                if msg["topic"] in self.listening_to:
                    callbacks = self.listening_to[msg["topic"]]
                    for callback in callbacks:
                        callback(msg)

            except zmq.Again:
                pass

    def broadcast_message(self, msg):
        logging.debug("Broadcasting message %r" % msg)
        self.manager_sock.send_json(msg)
