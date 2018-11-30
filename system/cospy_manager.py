from multiprocessing.managers import process
from multiprocessing.managers import BaseManager

import queue
import threading
import time



class CospyManager:

    def __init__(self, address=50000, authkey=b'costume'):
        self._main_queue = queue.Queue()
        self._node_queues = {}
        self._listeners = {}

        self._queue_manager = BaseManager(address=('', address), authkey=authkey)
        self._queue_manager.register('get_node_queue', callable=self._get_node_queue)
        self._queue_manager.register('get_main_queue', callable=self._get_main_queue)

        queue_server = self._queue_manager.get_server()

        queue_server.stop_event = threading.Event()

        process.current_process()._manager_server = queue_server

        queue_server_accepter = threading.Thread(target=queue_server.accepter)
        queue_server_accepter.daemon = True
        queue_server_accepter.start()

    def _get_main_queue(self):
        return self._main_queue

    def _get_node_queue(self, node_name):
        if node_name not in self._node_queues:
            self._node_queues[node_name] = queue.Queue()

        return self._node_queues[node_name]

    def run(self):

        while True:
            if not self._main_queue.empty():
                msg = self._main_queue.get()
                if msg.action_at > time.time():
                    self._main_queue.put(msg)
                else:
                    if msg.topic == "_listen_for":
                        node_name = msg.data["node_name"]
                        topic_to_listen = msg.data["topic"]
                        if topic_to_listen not in self._listeners:
                            self._listeners[topic_to_listen] = []
                        self._listeners[topic_to_listen].append(node_name)
                    else:
                        print(self._listeners)
                        for node_name in self._listeners[msg.topic]:
                            self._node_queues[node_name].put(msg)


if __name__ == "__main__":
    cm = CospyManager()
    cm.run()
