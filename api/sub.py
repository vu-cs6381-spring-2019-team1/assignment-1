#!/usr/bin/env python3
import sys
import zmq
import uuid

class Subscriber:

    def __init__(self, addr, port, useBroker=None):
        self.id = uuid.uuid4()
        self.addr = addr
        self.port = port
        self.__initializeContext()

    def __initializeContext(self):
        
        self.ctx = zmq.Context()

        self.bSocket = self.ctx.socket(zmq.SUB)

        self.bSocket.connect(f"tcp://{self.addr}:{self.port}")
        print(f"Finished connecting at port {self.port}.")

    
    def addTopic(self, topic):
        self.bSocket.setsockopt_string(zmq.SUBSCRIBE, topic)

    def listen(self):
    	print('Waiting for a message')
        string = self.bSocket.recv()
        topic, messagedata = string.split()
        print(topic, messagedata)

if __name__ == "__main__":

    s = Subscriber("localhost", "7777")
    s.addTopic('234')
    s.listen()

