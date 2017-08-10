import zmq
import random
import sys
import time

import flatbuffers
from neodroid.messaging import FlatBufferModels


port = "5555"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

msg = socket.recv()
while True:
    socket.send_string("Server message to client3")
    msg = socket.recv()
    monster = FlatBufferModels.FlatBufferReaction.GetRootAsFlatBufferReaction(msg, 0)
    print(monster.MotionsLength())
    print(monster.Reset())
    time.sleep(1)