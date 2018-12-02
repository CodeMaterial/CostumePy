from multiprocessing.managers import process
from multiprocessing.managers import BaseManager

import queue
import threading
import time
import logging


class CospyManager:

    def __init__(self, manager_key='costume'):
        self._main_queue = queue.Queue()
        self._node_queues = {}
        self._listeners = {}
        self.set_logging_level(logging.INFO)

        try:
            logging.info("Creating new Cospy Manager")
            self._queue_manager = BaseManager(address=('', 50000), authkey=manager_key.encode('UTF-8'))
            self._queue_manager.register('get_node_queue', callable=self._get_node_queue)
            self._queue_manager.register('get_main_queue', callable=self._get_main_queue)
        except:
            logging.info("Failed to register Cospy manager")
            raise

        try:
            logging.info("Launching new Cospy manager server")
            queue_server = self._queue_manager.get_server()

            queue_server.stop_event = threading.Event()

            process.current_process()._manager_server = queue_server

            queue_server_accepter = threading.Thread(target=queue_server.accepter)
            queue_server_accepter.daemon = True
            queue_server_accepter.start()
        except:
            logging.info("Failed to launch Cospy server")
            raise

    def _get_main_queue(self):
        return self._main_queue

    def _get_node_queue(self, node_name):
        logging.info("Retrieving node queue for %s" % node_name)
        if node_name not in self._node_queues:
            logging.info("Node queue for %s does not exist, creating." % node_name)
            self._node_queues[node_name] = queue.Queue()

        return self._node_queues[node_name]

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

        while True:
            if not self._main_queue.empty():
                msg = self._main_queue.get()
                if msg.action_at > time.time():
                    self._main_queue.put(msg)
                else:
                    logging.info("Received message %r" % msg)
                    if msg.topic == "_listen_for":
                        self.register_node(msg.data["node_name"], msg.data["topic"])
                    else:
                        if msg.topic in self._listeners:
                            for node_name in self._listeners[msg.topic]:
                                logging.info("Sending %r to %s" % (msg, node_name))
                                self._node_queues[node_name].put(msg)
                        else:
                            logging.info("No one listening to %s" % msg)


if __name__ == "__main__":
    cm = CospyManager()
    cm.set_logging_level(logging.DEBUG)
    cm.run()
