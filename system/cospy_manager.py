import time
import logging
import zmq
import threading

class CospyManager:

    def __init__(self):
        self._node_sockets = {}
        self._listeners = {}
        self.set_logging_level(logging.INFO)

        self.zmq_context = zmq.Context()
        self.request_socket = self.zmq_context.socket(zmq.REP)
        self.request_socket.bind("tcp://*:5556")

        self.ip_iter = 5557

        self._address_manager = threading.Thread(target=self.manage_requests)
        self._address_manager.start()

    def manage_requests(self):

        while True:
            node_name = self.request_socket.recv_string()
            address = "tcp://localhost:%i" % self.ip_iter
            self.request_socket.send_string(address)
            soc = zmq.Context().socket(zmq.PAIR)
            soc.bind("tcp://*:%i" % self.ip_iter)
            self._node_sockets[node_name] = soc
            self.ip_iter += 1


    def set_logging_level(self, logging_level):
        logging_format = '%(asctime)s [%(levelname)-5s]  %(message)s'
        logging.basicConfig(level=logging_level, format=logging_format)

    def register_node(self, node_name, topic_to_listen):
        logging.info("Registering  %s for %s" % (node_name, topic_to_listen))

        if topic_to_listen not in self._listeners:
            self._listeners[topic_to_listen] = []

        if node_name not in self._listeners[topic_to_listen]:
            self._listeners[topic_to_listen].append(node_name)

    def run(self):

        logging.info("Starting queue management")

        msg_todo = []

        while True:
            messages = msg_todo
            msg_todo = []
            for node_name in list(self._node_sockets):
                try:
                    soc = self._node_sockets[node_name]
                    msg = soc.recv_json(flags=zmq.NOBLOCK)
                    msg["_node_name"] = node_name
                    messages.append(msg)
                except zmq.Again:
                    pass

            for msg in messages:

                if msg["action_at"] > time.time():
                    msg_todo.append(msg)
                else:
                    logging.info("Received message %r" % msg)

                    if msg["topic"] == "_listen_for":
                        self.register_node(msg["_node_name"], msg["data"])
                    else:
                        if msg["topic"] in self._listeners:
                            for node_name in self._listeners[msg["topic"]]:
                                logging.info("Sending %r to %s" % (msg, node_name))
                                msg["responded"] = True
                                self._node_sockets[node_name].send_json(msg)
                        else:
                            logging.info("No one listening to %s" % msg)


if __name__ == "__main__":
    cm = CospyManager()
    cm.set_logging_level(logging.DEBUG)
    cm.run()
