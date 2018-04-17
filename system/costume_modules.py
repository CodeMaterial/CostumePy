from multiprocessing import Process
import time
import logging
from system.events import Event

class CostumeModule(Process):

    def __init__(self, refresh_rate=1, ignore_overrun=False):
        super().__init__()
        self.refresh_rate = refresh_rate
        self.running = True
        self.next_loop = None
        self.ignore_overrun = ignore_overrun
        self.is_setup = False

        self.send_queue = None
        self.receive_queue = None

        self.name = self.__class__.__name__

        self.listeners = {"SHUTDOWN": self.shutdown, "UI_REQUEST": self.ui_request}

        self.description = None

        self.actions = {}

        logging.info("Initialised")

    def __repr__(self):
        return "Costume Module: %s" % self.name

    def shutdown(self, event):
        logging.info("Shutting down")
        self.running = False

    def setup(self):
        pass

    def ui_request(self, event):
        e = Event("UI", {"descr": self.description, "actions": self.actions})

        self.broadcast("UI")

    def set_queues(self, manager_queue, module_queue):
        logging.debug("Setting queues")
        self.send_queue = manager_queue
        self.receive_queue = module_queue

    def broadcast(self, message_id, data=None, delay=0):
        event = Event(message_id, data=data, delay=delay, source=self.name)
        logging.debug("Broadcasting %r" % event)
        self.send_queue.put(event)

    def execute_queue(self):
        if not self.receive_queue.empty():
            event = self.receive_queue.get()
            if event.name in self.listeners:
                self.listeners[event.name](event)
            else:
                logging.error("%r doesn't have any handles" % event)

    def run(self):
        logging.info("Starting idle")
        
        while self.run_at_frame_rate():
            pass
        
        logging.info("Finished idle")

    def run_at_frame_rate(self):

        if not self.is_setup:
            self.setup()
            self.is_setup = True

        self.execute_queue()
        current_time = time.time()
        if not self.next_loop:
            self.next_loop = current_time + self.refresh_rate

        time_to_sleep = self.next_loop - current_time
        if time_to_sleep > 0:
            time.sleep(self.refresh_rate)
        else:
            if not self.ignore_overrun:
                logging.error("Overrunning by %r" % time_to_sleep)

        self.next_loop = current_time + self.refresh_rate

        return self.running
