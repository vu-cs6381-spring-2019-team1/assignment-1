#!/usr/bin/env python3

import socket
import threading
import time
import uuid
import zmq
from common import config

class Publisher:
    
    def __init__(self, port, useBroker=None):
        self.id = uuid.uuid4()
        self.port = port
        if useBroker is None:
            self.useBroker = False
        else:
            self.useBroker = useBroker

    # private method
    def __register_pub(self, topic):
        broker_addr = config()["broker"]["ip"]
        request_port = config()["broker"]["backendReplier"]
        
        broker_addr = "localhost"
        request_port = "5555"

        context = zmq.Context()
        sckt = context.socket(zmq.REQ)
        sckt.connect(f"tcp://{broker_addr}:{request_port}")

        start = time.time()
        sckt.send_string(f"{self.port},{topic}")
        temp = sckt.recv_string()
        end = time.time()

        print(f"broker request completed in {end-start}")

    def register_pub(self, topic):
        self.rp = threading.Thread(target=self.__register_pub, args=[topic])
        self.rp.start()

if __name__ == "__main__":

    p = Publisher("7777")
    p.register_pub("nothing")

    ctx = zmq.Context()
    skt = ctx.socket(zmq.REP)
    skt.bind("tcp://*:5555")
    msg = skt.recv_string()
    print(msg)
    skt.send_string("hello you")
    p.rp.join()
    print("joined")
