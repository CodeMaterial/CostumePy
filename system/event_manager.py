import logging
from multiprocessing import Process, Queue
import time

from system.events import Event

class EventManager(Process):

    def __init__(self):
        super().__init__()
        self.modules = {}
        self.listeners = {}  # {event_id:[module_id, module_id]}
        self.own_listeners = {"SHUTDOWN": self.shutdown}

        self.module_queues = {}  # {module_id: queue}
        self.main_queue = Queue()

        self.running = True
        self.name = self.__class__.__name__
        logging.debug("%r initialised" % self.name)

    def __repr__(self):
        return "<Event Manager>"

    def add_module(self, module_class):

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

    def start_modules(self):
        for module_name in self.modules:
            logging.debug("Starting new process for %r" % module_name)
            module = self.modules[module_name]
            module.start()

    def shutdown(self, event): # can only be run if the manager is running in the main process
        shutdown_event = Event("SHUTDOWN",True)
        for module_name in self.module_queues:
            logging.info("Shutting down %s"%module_name)
            self.module_queues[module_name].put(shutdown_event)
            logging.info("Joining %s"%module_name)
            self.modules[module_name].join()
            logging.info("%s Joined"%module_name)

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

    def inject(self, event):
        event.source = "inject"
        logging.debug("Injecting event %r" % event)
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

        logging.info("end")
