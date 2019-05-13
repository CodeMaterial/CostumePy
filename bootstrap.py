from CostumePy.cospy_manager import CospyManager
import CostumePy
import threading
import time
import subprocess
import sys
import os
import logging


class Bootstrap:

    def __init__(self, node_names):

        self.node = CostumePy.new_node("bootstrap")
        self.running_processes = {}
        self.node.listen("launch", self.launch_file)
        self.python_interpreter = sys.executable
        self.root_dir, _ = os.path.split(os.path.abspath(__file__))
        self.node_names = node_names

        for node_name in self.node_names:
            self.node.ui.add_button("launch_%s" % node_name, "Launch %s" % node_name, "launch", data=node_name)

        self.node.ui.update()

    def launch_file(self, msg):
        file_name = msg["data"]
        file_location = self.root_dir + "/" + file_name
        i = [self.python_interpreter, file_location, "&"]
        logging.info("Launching %s" % file_location)
        self.running_processes[file_name] = subprocess.Popen(i)


if __name__ == "__main__":

    cm = CospyManager()
    manager_thread = threading.Thread(target=cm.run)
    manager_thread.start()

    time.sleep(2)

    from CostumePy import web

    web_thread = threading.Thread(target=web.app.run)
    web_thread.start()

    b = Bootstrap(["example_nodes/radiator.py"])
