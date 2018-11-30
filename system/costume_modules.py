from multiprocessing import Process
import time
import logging
from CostumePy.system.message import Event


class CostumeModule(Process):

    def __init__(self, refresh_rate=1/30):
        super().__init__()
        self.refresh_rate = refresh_rate
        self.name = self.__class__.__name__
        self.description = None

        self.running = True
        self.next_loop = None
        self.is_setup = False

        self.send_queue = None
        self.receive_queue = None

        self.listeners = {"SHUTDOWN": self.shutdown}

        logging.info("Initialised")

    def __repr__(self):
        return "Costume Module: %s" % self.name

    def setup(self):
        pass

    def shutdown(self, event):
        logging.info("Shutting down")
        self.broadcast("DEATH")
        self.running = False

    def set_queues(self, manager_queue, module_queue):
        logging.debug("Setting queues")
        self.send_queue = manager_queue
        self.receive_queue = module_queue

    def broadcast(self, event, data=None, delay=0):

        if not isinstance(event, Event):
            event = Event(event, data=data, delay=delay, source=self.name)

        logging.debug("Broadcasting %r" % event)
        self.send_queue.put(event)

    def _execute_queue(self):
        if not self.receive_queue.empty():
            event = self.receive_queue.get()
            if event.name in self.listeners:
                self.listeners[event.name](event)
            else:
                logging.error("%r doesn't have any handles" % event)

    def run(self):
        logging.info("Starting idle")

        try:
            while self.run_at_frame_rate():
                pass
        except KeyboardInterrupt:
            self.shutdown(None)
            pass

    def run_at_frame_rate(self):

        if not self.is_setup:
            self.setup()
            self.is_setup = True

        self._execute_queue()

        current_time = time.time()
        if not self.next_loop:
            self.next_loop = current_time + self.refresh_rate

        time_to_sleep = self.next_loop - current_time

        self.next_loop = current_time + self.refresh_rate

        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

        return self.running
