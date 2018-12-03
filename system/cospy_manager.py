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
        self._manager_listeners = {"_listen_for": self.register_listener}

        self.request_socket = zmq.Context().socket(zmq.REP)
        self.request_socket.bind("tcp://*:55556")

        self.available_ip = 55557

        ip_address_manager = threading.Thread(target=self.manage_ip_requests)
        ip_address_manager.start()

    def manage_ip_requests(self):

        while True:
            node_name = self.request_socket.recv_string()
            address = "tcp://localhost:%i" % self.available_ip
            self.request_socket.send_string(address)
            soc = zmq.Context().socket(zmq.PAIR)
            soc.bind("tcp://*:%i" % self.available_ip)
            self._node_sockets[node_name] = soc
            self.available_ip += 1

    def register_listener(self, msg):
        topic, node_name = msg["data"], msg["source"]
        logging.info("Registering  %s for %s" % (node_name, topic))

        if topic not in self._listeners:
            self._listeners[topic] = []

        if node_name not in self._listeners[topic]:
            self._listeners[topic].append(node_name)

    def run(self):

        logging.info("Starting queue management")

        while True:
            for node_name in list(self._node_sockets):
                try:
                    soc = self._node_sockets[node_name]
                    msg = soc.recv_json(flags=zmq.NOBLOCK)
                    print(msg)
                    msg["source"] = node_name

                    if msg["action_at"] <= time.time():
                        logging.info("Received message %r" % msg)

                        topic = msg["topic"]

                        if topic in self._manager_listeners:
                            self._manager_listeners[topic](msg)
                        else:
                            if topic in self._listeners:
                                for nodes_listening in self._listeners[topic]:
                                    logging.info("Sending %r to %s" % (msg, nodes_listening))
                                    self._node_sockets[nodes_listening].send_json(msg)
                            else:
                                logging.info("No one listening to %s" % msg)
                except zmq.Again:
                    pass


if __name__ == "__main__":
    cm = CospyManager()
    cm.run()
