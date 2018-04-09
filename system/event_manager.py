import logging
from multiprocessing import Process, Queue
import time



class EventManager(Process):

    def __init__(self):
        super().__init__()
        self.modules = []
        self.listeners = {}  # {event_id:[module_id, module_id]}

        self.module_queues = {}  # {module_id: queue}
        self.main_queue = Queue()

        self.running = True
        self.name = self.__class__.__name__
        logging.debug("%r initialised" % self.name)

    def __repr__(self):
        return "<Event Manager>"

    def add_module(self, module_class):

        module = module_class()

        self.modules.append(module)


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
        for module in self.modules:
            logging.debug("Starting new process for %r" % module)
            module.start()

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

    def run(self):  # This method should be accessed via the start() method only

        logging.debug("Starting event management cycle")
        while self.running:
            if not self.main_queue.empty():
                event = self.main_queue.get()

                if event.action_at > time.time():
                    self.main_queue.put(event)
                else:
                    queues = self.find_queues(event)
                    logging.debug("Sending: %r to %r" % (event, queues))
                    for queue in queues:
                        queue.put(event)

        logging.info("end ")
