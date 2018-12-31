import zmq
import threading
import CostumePy


class CospyManager:

    def __init__(self):
        self.running = True
        self.nodes = {}  # {node_name, {"socket":socket, "ip": ip, "listening":[listening], "broadcasting":[broadcasting]}}
        self.node2node_ip = {}  # {node_name_1 + "_to_" + node_name_2: ip}

        self.callbacks = {"_state_update": self.node_change,
                          "_death": self.remove_node}

        self.request_socket = zmq.Context().socket(zmq.REP)
        self.request_socket.bind("tcp://*:55556")

        self.ip_address_manager = threading.Thread(target=self.manage_ip_requests)
        self.ip_address_manager.start()

        self.available_ip = 55557

        self.node2node_ip_iter = 66667

    def get_node2node_ip(self, node_name_a, node_name_b):
        connection = "_to_".join(sorted([node_name_a, node_name_b]))

        if connection not in self.node2node_ip:
            self.node2node_ip[connection] = self.node2node_ip_iter

            self.node2node_ip_iter += 1

        return self.node2node_ip[connection]

    def update_network(self):
        print("updating network")
        for node_name_a in list(self.nodes):

            outgoing = {}

            for topic in self.nodes[node_name_a]["broadcasting"]:
                outgoing[topic] = []
                for node_name_b in self.nodes:
                    if topic in self.nodes[node_name_b]["listening"]:
                        connecting_address = self.get_node2node_ip(node_name_a, node_name_b)
                        outgoing[topic].append(connecting_address)

            incoming = []

            for topic in self.nodes[node_name_a]["listening"]:
                for node_name_b in self.nodes:
                    if topic in self.nodes[node_name_b]["broadcasting"]:
                        connecting_address = self.get_node2node_ip(node_name_a, node_name_b)
                        incoming.append(connecting_address)

            network_update_msg = CostumePy.message("_network_update",
                                                   data={"outgoing": outgoing, "incoming": incoming})

            print("sending update message", node_name_a, network_update_msg)
            self.nodes[node_name_a]["socket"].send_json(network_update_msg)

    def add_node(self, name, socket, address):

        self.nodes[name] = {"socket": socket, "address": address, "listening": [], "broadcasting": []}

        self.update_network()

    def remove_node(self, msg):
        print("removing node", msg)
        del self.nodes[msg["source"]]
        self.update_network()

    def node_change(self, msg):
        new_state = msg["data"]
        node_name = msg["source"]
        print("node change", msg)

        self.nodes[node_name]["listening"] = new_state["listening"]
        self.nodes[node_name]["broadcasting"] = new_state["broadcasting"]
        self.update_network()

    def run(self):

        try:
            while self.running:
                node_names = list(self.nodes)
                for node_name in node_names:
                    try:
                        soc = self.nodes[node_name]["socket"]
                        msg = soc.recv_json(flags=zmq.NOBLOCK)
                        msg["source"] = node_name
                        self.action_msg(msg)

                    except zmq.Again:
                        pass

        finally:
            self.stop()

    def manage_ip_requests(self):

        while self.running:
            try:
                node_name = self.request_socket.recv_string(flags=zmq.NOBLOCK)
                address = "tcp://localhost:%i" % self.available_ip
                self.request_socket.send_string(address)
                soc = zmq.Context().socket(zmq.PAIR)
                soc.bind("tcp://*:%i" % self.available_ip)
                self.add_node(node_name, soc, address)
                self.available_ip += 1
            except zmq.Again:
                pass

    def action_msg(self, msg):
        topic = msg["topic"]
        print("recieved message to action", msg)
        self.callbacks[topic](msg)

    def stop(self):
        self.running = False
        self.ip_address_manager.join()


if __name__ == "__main__":

    cm = CospyManager()
    cm.run()
