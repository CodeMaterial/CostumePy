import time
import multiprocessing
import logging

from system.costume_modules import CostumeModule


class EventManager(multiprocessing.Process):

    def __init__(self):
        super().__init__()
        self.modules = []
        self.event_queue = multiprocessing.Queue()
        self.listeners = {}

        logging.info("Event Manager instantiated")

    def __repr__(self):
        return "Event Manager"

    def inject(self, event):
        self.event_queue.put(event)
        logging.info("Event Injected: %r" % event)

    def add_module(self, module):
        if isinstance(module, list):
            for i in module:
                self.add_module(i)

        if isinstance(module, CostumeModule):
            module.set_manager(self.event_queue)
            self.modules.append(module)

        logging.info("%r added to Event Manager" % module)

    def add_listener(self, method, message_id):
        if message_id in self.listeners:
            self.listeners[message_id].append(method)
        else:
            self.listeners[message_id] = [method]
            logging.info("%r now listening for %r" % (method, message_id))

    def run_all(self):
        for module in self.modules:
            logging.info("Starting module %r" % module)
            module.start()

    def run(self):
        logging.info("Starting event management cycle")
        while True:
            if not self.event_queue.empty():
                event = self.event_queue.get()
                if event.action_at > time.time():
                    self.event_queue.put(event)
                else:
                    if event.name in self.listeners:
                        methods = self.listeners[event.name]
                        for method in methods:
                            try:
                                method(event)
                            except Exception as e:
                                logging.error("Method %r failed to handle event %r: %r" % (method, event, str(e)))
