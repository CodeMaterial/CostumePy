import logging
import time
from system.events import Event
from multiprocessing import Queue


class UnitTest:

    def __init__(self, module_class):
        self.current_test_name = ""
        self.passed = True
        self.diagnostic = {}
        self.send_queue = Queue()
        self.receive_queue = Queue()
        self.module_class = module_class
        self.module = None

    def send_input(self, event):
        self.send_queue.put(event)

    def run_tests(self):
        try:
            self.module = self.module_class()
            self.module.set_queues(self.receive_queue, self.send_queue)
            self.module.start()
        except:
            logging.error("Cannot initialise module")
            self.passed = False
            return

        self.run_all_tests()

    def has_passed(self):
        return self.passed

    def clear_queues(self):
        for q in [self.send_queue, self.receive_queue]:
            while not q.empty():
                q.get()

    def run_all_tests(self):
        logging.info("Executing %s" % self.__class__.__name__)
        for func in dir(self):
            if func.startswith("test_"):
                self.current_test_name = func
                test_function = eval("self.%s" % func)
                self.diagnostic[self.current_test_name] = ""
                self.clear_queues()
                try:
                    test_function()
                except:
                    logging.error("Test function failed")
                    self.passed = False
                    self.diagnostic[self.current_test_name] += "Test Failure"

        self.__test_shutdown()

        logging.info("Module passed!" if self.passed else "Module Failed!")
        for item in self.diagnostic:
            logging.info(item + self.diagnostic[item])

    def __test_shutdown(self):

        self.send_queue.put(Event("SHUTDOWN"))
        start_time = time.time()

        while time.time() - start_time < 1:
            if not self.module.is_alive():
                self.diagnostic["test_shutdown"] = "Passed, Module shutdown in %0.2f seconds" % (time.time() - start_time)
                return True

        self.passed = False
        self.diagnostic["__test_shutdown"] = "Failed, module failed to shutdown, killing"
        self.module.terminate()
        return False

    def check_output(self, event):

        start_time = time.time()

        while time.time() - start_time < 1:
            if not self.receive_queue.empty():
                e = self.receive_queue.get()
                if e == event:
                    self.diagnostic[self.current_test_name] += "Passed %s output check" % event
                    return
                else:
                    self.receive_queue.put(e)

        self.passed = False
        self.diagnostic[self.current_test_name] += "Failed %s output check" % event