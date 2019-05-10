from CostumePy.cospy_manager import CospyManager
from CostumePy.UI import Button
import CostumePy
import threading
import time
import subprocess
import sys
import os

class Bootstrap:

    def __init__(self, node_names):

        self.node = CostumePy.new_node("bootstrap")
        self.running_nodes = {}
        self.node.listen("launch", self.launch_node)
        self.python_interpreter = sys.executable
        self.root_dir, _ = os.path.split(os.path.abspath(__file__))
        self.node_names = node_names

        for node_name in self.node_names:
            self.node.ui.add_elements(Button("launch %s" % node_name, "launch", data=node_name))

    def launch_node(self, msg):
        node_name = msg["data"]
        self.node_names.remove(node_name)
        file_location = self.root_dir + "/" + node_name
        i = [self.python_interpreter, file_location, "&"]
        print("launching %r" % i)
        self.running_nodes[node_name] = subprocess.Popen(i)
        print("Launched")


if __name__ == "__main__":

    cm = CospyManager()
    manager_thread = threading.Thread(target=cm.run)
    manager_thread.start()

    time.sleep(2)

    from CostumePy import web

    web_thread = threading.Thread(target=web.app.run)
    web_thread.start()

    b = Bootstrap(["example_nodes/radiator.py", "node_2"])