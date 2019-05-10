import threading
import logging
import zmq
import CostumePy
from CostumePy.UI import UI
import socket
import time


class CospyNode:

    def __init__(self, name):
        self.name = name
        self.listening_to = {"_success": [self._success]}
        self.running = True
        self.last_success = None
        self.ui = UI(self)

        self._zmq_context = zmq.Context()

        self.manager_sock = self._zmq_context.socket(zmq.PAIR)

        try:
            address = self._request_socket_ip()
            self.manager_sock.connect(address)
        except ConnectionRefusedError:
            raise

        self._callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self._callback_listener.start()

    def _request_socket_ip(self, retries=0):

        if retries > 5:
            raise ConnectionRefusedError("Cannot contact manager, has it been started?")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        manager_available = sock.connect_ex(('', 55556)) == 0
        sock.close()
        if not manager_available:
            logging.info("Cannot connect to manager, retrying...")
            time.sleep(1)
            return self._request_socket_ip(retries=retries+1)

        ip_socket = self._zmq_context.socket(zmq.REQ)
        ip_socket.connect("tcp://localhost:55556")
        ip_socket.send_string(self.name)

        ip_address = ip_socket.recv().decode('UTF-8')

        ip_socket.close()

        return ip_address

    def quit(self):
        self.running = False
        self._callback_listener.join()
        quit()  # WARNING. If there are multiple nodes per file this will kill all of them. TODO

    def listen(self, topic, callback):
        logging.info("Setting up listening callbacks for %s" % topic)

        if topic not in self.listening_to:
            logging.info("Topic %s is not currently being listened to by this node, initialising." % topic)
            self.listening_to[topic] = []

        self.listening_to[topic].append(callback)
        listen_msg = CostumePy.message("_listen_for", data=topic)
        self.broadcast_message(listen_msg)
        self.wait_for_success(listen_msg)

    def _success(self, msg):
        orig_msg = msg["data"]
        self.last_success = orig_msg

    def wait_for_success(self, msg, timeout=5):
        logging.info("Waiting on response")
        start = time.time()
        while (self.last_success != msg) and (time.time() - start <= timeout):
            time.sleep(.1)

        if self.last_success != msg:
            raise ConnectionAbortedError("Timeout reached whilst waiting for message %r" % msg)
        else:
            logging.info("Response recieved")

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
        msg["source"] = self.name
        logging.debug("Broadcasting message %r" % msg)
        self.manager_sock.send_json(msg)

    def broadcast(self, topic, data=None, delay=0):
        msg = CostumePy.message(topic, data=data, delay=delay)
        self.broadcast_message(msg)
