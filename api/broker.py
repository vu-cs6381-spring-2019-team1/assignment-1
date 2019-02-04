#!/usr/bin/env python3

from collections import defaultdict 
from pprint import pprint
import threading
import uuid
import zmq

from common import config

class Broker:

    def __init__(self):
        self.id = uuid.uuid4()
        self.setupBroker()
        self.topicList = defaultdict(list)
        
    def __setupBroker(self):
        frontendPort = config()["broker"]["frontendForwarder"]
        backendPort = config()["broker"]["backendForwarder"]

        try:
            self.context = zmq.Context()

            frontend = self.context.socket(zmq.XSUB)
            frontend.bind(f"tcp://*:{frontendPort}")

            backend = self.context.socket(zmq.XPUB)
            backend.bind(f"tcp://*:{backendPort}")

            print("Bound frontend and backend of Broker")

            zmq.proxy(frontend, backend)

        except Exception as e:
            print(e)

        finally:
            pass
            print("Shutting down broker")
            frontend.close()
            backend.close()
            self.context.term()

    def setupBroker(self):
        self.broker = threading.Thread(target=self.__setupBroker)
        self.broker.start()

if __name__ == "__main__":

    b = Broker()
    print("got here")
