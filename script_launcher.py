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

        self.node = CostumePy.new_node("script_launcher")
        self.running_processes = {}
        self.node.listen("launch", self.launch_file)
        self.python_interpreter = sys.executable
        self.root_dir, _ = os.path.split(os.path.abspath(__file__))
        self.node_names = node_names

        for i, node_name in enumerate(self.node_names):
            self.node.ui.add_button("launch_%s" % node_name, "Launch %s" % node_name, "launch", data=node_name, order=i*2)
            self.node.ui.add_break("break_%s" % node_name, order=i*2+1)

        self.node.ui.update()

    def launch_file(self, msg):
        file_name = msg["data"]
        if file_name not in self.running_processes:

            file_location = self.root_dir + "/" + file_name
            i = [self.python_interpreter, file_location, "&"]
            logging.info("Launching %s" % file_location)
            self.running_processes[file_name] = subprocess.Popen(i)

            self.check()

        elif self.running_processes[file_name].poll() is not None:
            del self.running_processes[file_name]
            self.launch_file(msg)
            self.check()
        else:
            logging.info("%s Is already running" % file_name)

    def check(self):

        for filename in self.running_processes:
            alive = self.running_processes[filename].poll() is not None
            self.node.ui.get("launch_%s" % filename)["button_class"] = "btn " + "btn-default" if alive else "btn-success"
            self.node.ui.get("launch_%s" % filename)["enabled"] = alive
        self.node.ui.update()


if __name__ == "__main__":

    cm = CospyManager()
    manager_thread = threading.Thread(target=cm.run)
    manager_thread.start()

    time.sleep(2)

    from CostumePy import web

    web_thread = threading.Thread(target=web.app.run, args=["0.0.0.0"])
    web_thread.start()

    b = Bootstrap(sys.argv[1:])
    while b.node.running:
        time.sleep(2)
        b.check()
