#!/usr/bin/env python3

import socket
import threading
import time
import uuid
import zmq

from common import config

class Publisher:
    
    def __init__(self, addr, port, useBroker=None):
        self.id = uuid.uuid4()
        self.addr = addr
        self.port = port
        if useBroker is None:
            self.useBroker = False
        else:
            self.useBroker = useBroker
        self.__initializeContext()

    def __initializeContext(self):
        
        self.ctx = zmq.Context()

        self.bSocket = self.ctx.socket(zmq.PUB)
        self.bSocket.bind(f"tcp://*:{self.port}")
        print(f"Finished binding context for Publisher at address {self.addr} and port {self.port}.")

        broker_addr = config()["broker"]["ip"]
        proxy_frontend = config()["broker"]["frontendForwarder"]

        self.cSocket = self.ctx.socket(zmq.PUB)
        self.cSocket.connect(f"tcp://{broker_addr}:{proxy_frontend}")
        print(f"Finished connecting to proxy at address {broker_addr} and port {proxy_frontend}")

    def __register_pub(self, topic):
        broker_addr = config()["broker"]["ip"]
        request_port = config()["broker"]["frontendReplier"]
        
        broker_addr = "localhost"
        request_port = "5555"

        regContext = zmq.Context()
        sckt = regContext.socket(zmq.REQ)
        sckt.connect(f"tcp://{broker_addr}:{request_port}")

        start = time.time()
        sckt.send_string(f"{topic},{self.addr}:{self.port}")
        temp = sckt.recv_string()
        end = time.time()

        print(f"broker request completed in {end-start}")

    def register_pub(self, topic):
        self.rp = threading.Thread(target=self.__register_pub, args=[topic])
        self.rp.start()

    def publish(self, topic, value):
        if type(topic) is not type(str()):
            print("The topic must be of type string")
        elif useBroker:
            self.cSocket.send_string(f"{topic}:{value}")
        else:
            self.bSocket.send_string(f"{topic}:{value}")


if __name__ == "__main__":

    p = Publisher("localhost", "7777")
    p.register_pub("nothing")

    ctx = zmq.Context()
    skt = ctx.socket(zmq.REP)
    skt.bind("tcp://*:5555")
    msg = skt.recv_string()
    print(msg)
    skt.send_string("hello you")
    p.rp.join()
    print("joined")
