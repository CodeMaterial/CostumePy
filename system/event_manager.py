import logging
import time
from multiprocessing import Process, Queue

from system.events import Event


class EventManager(Process):

    def __init__(self):
        super().__init__()
        self.modules = {}
        self.listeners = {}
        self.own_listeners = {"SHUTDOWN": self.shutdown}

        self.module_queues = {}  # {module_id: queue}
        self.main_queue = Queue()

        self.running = True
        self.name = self.__class__.__name__
        logging.debug("%r initialised" % self.name)

    def __repr__(self):
        return "<Event Manager>"

    def list_modules(self, event):
        self.broadcast("ALL_MODULES", data=list(self.modules.keys()))  # Cast to a list to make pickle-able

    def add_module(self, module_class):

        passed_testing = self.test_module(module_class)

        if not passed_testing:
            print("Module failed to pass test criteria. Dropping")
            return

        module = module_class()

        self.modules[module.name] = module

        # Setup queues
        module_queue = Queue()
        self.module_queues[module.name] = module_queue

        module.set_queues(self.main_queue, module_queue)

        # Setup listeners
        for event_id in module.listeners:
            if event_id in self.listeners:
                self.listeners[event_id].append(module.name)
            else:
                self.listeners[event_id] = [module.name]

        logging.debug("%r added to manager" % module)

    def test_module(self, module):
        logging.debug("Testing module %s" % module.__name__)

        try:
            exec("from tests.unit.%s_test import %sTest" % (module.__name__.lower(), module.__name__))
        except ImportError:
            print("Cannot load %sTest, does it exist?" % module.__name__)
            return True

        test_class = eval("%sTest" % module.__name__)
        test = test_class()
        test.run_tests()
        passed = test.has_passed()
        del test
        return passed

    def start_modules(self):
        for module_name in self.modules:

            logging.debug("Starting new process for %r" % module_name)
            module = self.modules[module_name]
            module.start()

    def shutdown(self, event):

        shutdown_event = Event("SHUTDOWN")
        for module_name in self.module_queues:
            self.module_queues[module_name].put(shutdown_event)
            self.modules[module_name].join()

        logging.info("All modules joined")
        self.running = False

    def find_queues(self, event):

        queues = []

        if event.name not in self.listeners:
            logging.error("Cannot find any modules listening to %s" % event.name)
        else:
            for module_id in self.listeners[event.name]:
                if module_id in self.module_queues:
                    queues.append(self.module_queues[module_id])
                else:
                    logging.error("Cannot find associated pipe for %s" % module_id)

        return queues

    def broadcast(self, message_id, data=None, delay=0):
        event = Event(message_id, data=data, delay=delay,source=self.name)
        logging.debug("Broadcasting event %r" % event)
        for queue in self.find_queues(event):
            queue.put(event)

    """ This method should be called directly in the main process but can be called as a process using start()
        If using start() then shutdown() needs to be called explicitly in the main process to cleanup the modules"""
    def run(self):

        logging.debug("Starting event management cycle")
        while self.running:
            if not self.main_queue.empty():
                event = self.main_queue.get()

                if event.action_at > time.time():
                    self.main_queue.put(event)
                else:
                    if event.name in self.own_listeners:
                        self.own_listeners[event.name](event)
                    else:
                        queues = self.find_queues(event)
                        logging.debug("Sending: %r to %r" % (event, queues))
                        for queue in queues:
                            queue.put(event)

        logging.info("Complete event management cycle")
