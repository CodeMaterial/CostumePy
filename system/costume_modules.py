import multiprocessing
import time
import logging


class CostumeModule(multiprocessing.Process):

    def __init__(self, refresh_rate):
        super().__init__()
        self.event_queue = None
        self.refresh_rate = refresh_rate
        self.running = True
        self.next_loop = time.time() + refresh_rate

        logging.info("CostumeModule instantiated")

    def __repr__(self):
        return "Costume Module: %s" % self.__class__.__name__

    def broadcast(self, event):
        event.source = self.__class__
        self.event_queue.put(event)
        logging.info("Event broadcast: %r" % event)

    def set_manager(self, event_queue):
        self.event_queue = event_queue

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.run_at_frame_rate()

    def run_at_frame_rate(self):

        time_to_sleep = self.next_loop - time.time()
        if time_to_sleep > 0:
            time.sleep(self.refresh_rate)
        else:
            logging.error("Overunning")

        self.next_loop = time.time() + self.refresh_rate

        return self.running