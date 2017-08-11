import zmq
import time
import flatbuffers
import neodroid.messaging as msging


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

reaction = msging.build_reaction()

while True:
    socket.send(reaction)
    msg = socket.recv()
    print(len(msg))
    print(type(msg))
    msg_ = msging.deserialize_state(msg)
    print(type(msg_))
    print(msg_.Observers(1).Name())
    time.sleep(1)