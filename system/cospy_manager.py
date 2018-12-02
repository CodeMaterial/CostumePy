import time
import logging
import zmq
import threading
import CostumePy

class CospyManager:

    def __init__(self):
        self._node_sockets = {}
        self._listeners = {}
        CostumePy.set_logging_level(logging.DEBUG)

        self.request_socket = zmq.Context().socket(zmq.REP)
        self.request_socket.bind("tcp://*:5556")

        self.avaliable_ip = 5557

        ip_address_manager = threading.Thread(target=self.manage_ip_requests)
        ip_address_manager.start()

    def manage_ip_requests(self):

        while True:
            node_name = self.request_socket.recv_string()
            address = "tcp://localhost:%i" % self.avaliable_ip
            self.request_socket.send_string(address)
            soc = zmq.Context().socket(zmq.PAIR)
            soc.bind("tcp://*:%i" % self.avaliable_ip)
            self._node_sockets[node_name] = soc
            self.avaliable_ip += 1

    def register_node(self, node_name, topic_to_listen):
        logging.info("Registering  %s for %s" % (node_name, topic_to_listen))

        if topic_to_listen not in self._listeners:
            self._listeners[topic_to_listen] = []

        if node_name not in self._listeners[topic_to_listen]:
            self._listeners[topic_to_listen].append(node_name)

    def run(self):

        logging.info("Starting queue management")

        msg_backlog = []

        while True:
            messages = msg_backlog
            msg_backlog = []
            for node_name in list(self._node_sockets):
                try:
                    soc = self._node_sockets[node_name]
                    msg = soc.recv_json(flags=zmq.NOBLOCK)
                    if msg["source"] is None:
                        msg["source"] = node_name
                    messages.append(msg)
                except zmq.Again:
                    pass

            for msg in messages:

                if msg["action_at"] > time.time():
                    msg_backlog.append(msg)
                else:
                    logging.info("Received message %r" % msg)

                    if msg["topic"] == "_listen_for":
                        self.register_node(msg["source"], msg["data"])
                    else:
                        if msg["topic"] in self._listeners:
                            for node_name in self._listeners[msg["topic"]]:
                                logging.info("Sending %r to %s" % (msg, node_name))
                                self._node_sockets[node_name].send_json(msg)
                        else:
                            logging.info("No one listening to %s" % msg)


if __name__ == "__main__":
    cm = CospyManager()
    cm.run()
