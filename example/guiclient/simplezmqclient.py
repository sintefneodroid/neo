import zmq
import time
import flatbuffers
import neodroid.messaging as msging


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

reaction = msging.build_reaction()

#socket.send(reaction)
while True:
    socket.send(reaction)
    msg = socket.recv()
    print(len(msg))
    msg_ = msging.deserialize_state(msg)
    print(msg_.RewardForLastStep())