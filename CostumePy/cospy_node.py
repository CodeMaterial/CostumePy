import threading
import logging
import zmq
import CostumePy
import socket
import time


class CospyNode:

    def __init__(self, name):
        self.name = name
        self.topic2callback = {"_network_update": self.network_update}  # {topic:callback}
        self.topic2addresses = {}  # {topic:[address]}
        self.incoming_addresses = []  # ip's
        self.address2socket = {}  # {ip:sock}

        self.running = True

        self.update_pending = 0

        self._zmq_context = zmq.Context()

        self.manager_sock = self._zmq_context.socket(zmq.PAIR)

        try:
            self._connect_to_manager(self.manager_sock)
        except ConnectionRefusedError:
            raise

        self.listener_thread = threading.Thread(target=self._listen_for_callbacks)
        self.listener_thread.start()

    def _connect_to_manager(self, manager_sock, retries=0, max_retries=5):

        print("connecting to manager...")

        if retries > max_retries:
            raise ConnectionRefusedError("Cannot contact manager, has it been started?")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        manager_available = sock.connect_ex(('', 55556)) == 0
        sock.close()
        if not manager_available:
            logging.info("Cannot connect to manager, retrying...")
            time.sleep(1)
            return self._connect_to_manager(manager_sock, retries=retries+1)

        with self._zmq_context.socket(zmq.REQ) as manager_request_socket:
            manager_request_socket.connect("tcp://localhost:55556")
            manager_request_socket.send_string(self.name)

            ip_address = manager_request_socket.recv().decode('UTF-8')

        manager_sock.connect(ip_address)

        print("connected to manager")

    def network_update(self, msg):

        print("recieved network update request", msg)

        self.topic2addresses = msg["data"]["outgoing"]  # {"outgoing": topic2ip, "incoming": listening_ips})

        for topic in self.topic2addresses:
            for address in self.topic2addresses[topic]:
                if address not in self.address2socket:
                    soc = zmq.Context().socket(zmq.PAIR)
                    soc.bind("tcp://*:%i" % address)
                    self.address2socket[address] = soc

        self.incoming_addresses = msg["data"]["incoming"]

        for address in self.incoming_addresses:
            if address not in self.address2socket:
                soc = self._zmq_context.socket(zmq.PAIR)
                soc.connect("tcp://localhost:" + address)

                self.address2socket[address] = soc

        self.update_pending -= 1

    def update(self):

        print("Updating network")

        self.update_pending += 1

        msg = CostumePy.message("_state_update", data=self.state())
        msg["source"] = self.name
        self.manager_sock.send_json(msg)

        print("waiting for server update")
        while self.update_pending:
            time.sleep(0.01)
        print("server update recieved")

    def state(self):
        state = {"listening": list(self.topic2callback.keys()), "broadcasting": list(self.topic2addresses.keys())}
        print("retrieving state", state)
        return state

    def broadcast(self, topic, data=None, delay=0):

        msg = CostumePy.message(topic, data=data, delay=delay)
        msg["source"] = self.name

        print("broadcsating message", msg)

        if msg["topic"] not in self.topic2addresses:
            print("unexpected topic")
            self.update()

        if msg["topic"] in self.topic2addresses:
            for address in self.topic2addresses[msg["topic"]]:
                print("sending %r to %r" % (msg, address))
                sock = self.address2socket[address]
                sock.send_json(msg)
        else:
            print("no known targets for topic %r" % msg["topic"])

    def listen_to(self, topic, callback):

        print("listening to ", topic, callback)

        self.topic2callback[topic] = callback
        self.update()

    def stop(self):
        death_msg = CostumePy.message("_death")
        self.manager_sock.send_json(death_msg)

        self.running = False
        self.listener_thread.join()

    def _listen_for_callbacks(self):

        while self.running:
            time.sleep(.5)

            for soc in [self.address2socket[address] for address in self.incoming_addresses] + [self.manager_sock]:
                try:
                    msg = soc.recv_json(flags=zmq.NOBLOCK)
                    print("recieved message", msg)
                    if msg["topic"] in self.topic2callback:
                        callback = self.topic2callback[msg["topic"]]
                        callback(msg)
                except zmq.Again:
                    pass