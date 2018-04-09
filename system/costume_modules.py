from multiprocessing import Process
import time
import logging

class CostumeModule(Process):

    def __init__(self, refresh_rate):
        super().__init__()
        self.refresh_rate = refresh_rate
        self.running = True
        self.next_loop = None
        self.send_queue = None
        self.receive_queue = None
        self.name = self.__class__.__name__
        self.listeners = {"SHUTDOWN": self.shutdown}  # This could be {"NOSE_PRESS":self.nose_press)}

        logging.info("Initialised")

    def __repr__(self):
        return "Costume Module: %s" % self.name

    def shutdown(self):
        logging.info("Shutting down")
        self.running = False

    def set_queues(self, manager_queue, module_queue):
        logging.debug("Setting queues")
        self.send_queue = manager_queue
        self.receive_queue = module_queue

    def broadcast(self, event):
        event.source = self.name
        logging.debug("Broadcasting %r" % event)
        self.send_queue.put(event)

    def run(self):
        logging.info("Starting idle")
        while self.pause():
            if not self.receive_queue.empty():
                event = self.receive_queue.get()
                if event.name in self.listeners:
                    self.listeners[event.name](event)
                else:
                    logging.error("%r doesn't have any handles" % event)
        logging.info("Finished idle")

    def pause(self):

        if not self.next_loop:
            self.next_loop = time.time() + self.refresh_rate

        time_to_sleep = self.next_loop - time.time()
        if time_to_sleep > 0:
            time.sleep(self.refresh_rate)
        else:
            logging.error("Overrunning")

        self.next_loop = time.time() + self.refresh_rate

        return self.running
