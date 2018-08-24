from multiprocessing import Process
import time
import logging
from CostumePy.system.events import Event


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

        self.listeners = {"SHUTDOWN": self.shutdown,
                          "HEARTBEAT_REQUEST": self.heartbeat_request,
                          "MEASURE_REFRESH": self.measure_refresh}
        self.actions = {}

        self.refresh_times_limit = int(max(2.0, 1.0/refresh_rate*2))
        self.refresh_times = [0]*self.refresh_times_limit

        logging.info("Initialised")

    def __repr__(self):
        return "Costume Module: %s" % self.name

    def heartbeat_request(self, event):
        self.broadcast("HEARTBEAT")

    def shutdown(self, event):
        logging.info("Shutting down")
        self.broadcast("DEATH")
        self.running = False

    def setup(self):
        pass

    def measure_refresh(self, event):

        rate = 0
        if len(self.refresh_times) == self.refresh_times_limit:

            time_sum = 0
            for i in range(self.refresh_times_limit-1):
                time_sum += self.refresh_times[i+1] - self.refresh_times[i]

            rate = time_sum/(self.refresh_times_limit-1)

        self.broadcast("REFRESH_RATE", data=rate)

    def set_queues(self, manager_queue, module_queue):
        logging.debug("Setting queues")
        self.send_queue = manager_queue
        self.receive_queue = module_queue

    def broadcast(self, event, data=None, delay=0):

        if not isinstance(event, Event):
            event = Event(event, data=data, delay=delay, source=self.name)

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

        self.execute_queue()

        current_time = time.time()
        if not self.next_loop:
            self.next_loop = current_time + self.refresh_rate

        time_to_sleep = self.next_loop - current_time

        self.next_loop = current_time + self.refresh_rate

        self.refresh_times.append(current_time)
        self.refresh_times = self.refresh_times[1:self.refresh_times_limit+1]

        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

        return self.running
