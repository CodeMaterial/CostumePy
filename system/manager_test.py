from multiprocessing.managers import BaseManager, process
import queue
import threading
import time


class Event(object):

    def __init__(self, name, data=None, delay=0, source=None):
        super().__init__()
        self.source = source
        self.name = name
        self.data = data
        self.created = time.time()
        self.delay = delay
        self.action_at = self.created + delay

    def __eq__(self, other):
        """Overrides the default implementation"""
        is_equal = True
        if isinstance(other, Event):
            is_equal *= other.name == self.name
            if other.source and self.source:
                is_equal *= other.source == self.source
            if other.data and self.data:
                is_equal *= other.data == self.data
            if other.delay and self.delay:
                is_equal *= other.delay == self.delay

        return is_equal

    def __repr__(self):
        return "<%s - {source: %r, name:%r, data:%r, created:%r, delay:%r}>" % \
               (self.__class__.__name__, self.source, self.name, self.data, self.created, self.delay)


class QueueManager(BaseManager):
    pass


class CospyManager():

    def __init__(self, address=50000, authkey=b'costume'):
        super().__init__()
        self._main_queue = queue.Queue()
        self._module_queues = {}
        self.listeners = {}

        self.manager = QueueManager(address=('', address), authkey=authkey)
        self.manager.register('get_module_queue', callable=self._get_module_queue)
        self.manager.register('get_main_queue', callable=self._get_main_queue)

        self.server = self.manager.get_server()

        self.server.stop_event = threading.Event()

        process.current_process()._manager_server = self.server

        accepter = threading.Thread(target=self.server.accepter)
        accepter.daemon = True
        accepter.start()

    def _get_main_queue(self):
        return self._main_queue

    def _get_module_queue(self, module_name):
        print("getting queue %s" % module_name)
        if module_name not in self._module_queues:
            print("creating new queue")
            self._module_queues[module_name] = queue.Queue()

        return self._module_queues[module_name]

    def run(self):

        while True:
            if not self._main_queue.empty():
                event = self._main_queue.get()
                if event.action_at > time.time():
                    self._main_queue.put(event)
                else:
                    topic = event.name
                    print(topic)
                    if topic == "_listen_to":
                        module_name = event.data["module_name"]
                        topic = event.data["topic"]
                        if topic not in self.listeners:
                            self.listeners[topic] = []
                        self.listeners[topic].append(module_name)
                    else:
                        for module_name in self.listeners[topic]:
                            self._module_queues[module_name].put(event)



if __name__ == "__main__":
    cm = CospyManager()
    cm.run()