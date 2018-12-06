import threading
import logging
import zmq
import CostumePy
import socket
import time


class CospyNode:

    def __init__(self, name):
        self.name = name
        self.listening_to = {"_success": [self._success], "_new_node": self.new_broadcast_receiver}
        self.broadcasting = {}  # topics : [ip]
        self.sockets = {}  # {ip:sock}
        self.running = True
        self.last_success = None

        self._zmq_context = zmq.Context()

        self.manager_sock = self._zmq_context.socket(zmq.PAIR)

        try:
            address = self._request_socket_ip()
            self.manager_sock.connect(address)
        except ConnectionRefusedError:
            raise

        self._callback_listener = threading.Thread(target=self._listen_for_callbacks)
        self._callback_listener.start()

    def new_broadcast_receiver(self, msg):
        ip_address = msg["data"]["address"]
        topic = msg["data"]["topic"]
        self.broadcasting[topic].append(ip_address)
        if ip_address not in self.sockets:
            self.sockets[ip_address] = self._zmq_context.socket(zmq.PAIR)
            self.sockets[ip_address].connect(ip_address)

    def server_request(self, msg):
        msg["source"] = self.name
        self.manager_sock.send_json(msg)
        self.wait_for_success()

    def broadcast(self, msg):
        if msg["topic"] in self.broadcasting:
            pass
        else:
            msg["topic"] = []
            msg = CostumePy.message("new_broadcast", data=msg["topic"])
            self.server_request(msg)

    def listen_to(self, topic, callback):
        logging.info("Setting up listening callbacks for %s" % topic)

        if topic not in self.listening_to:
            logging.info("Topic %s is not currently being listened to by this node, initialising." % topic)
            self.listening_to[topic] = []
            msg = CostumePy.message("_listen_request", data=)
            self.server_request(msg)

        self.listening_to[topic].append(callback)
        listen_msg = CostumePy.message("_listen_for", data=topic)
        self.broadcast_message(listen_msg)
        self.wait_for_success(listen_msg)

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

        with self._zmq_context.socket(zmq.REQ) as ip_socket:
            ip_socket.connect("tcp://localhost:55556")
            ip_socket.send_string(self.name)

            ip_address = ip_socket.recv().decode('UTF-8')

            return ip_address

    def stop(self):
        self.running = False
        self._callback_listener.join()



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