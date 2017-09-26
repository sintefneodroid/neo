from threading import Thread

import zmq

from .FlatBufferModels import *

from neodroid.models import Reaction
from .FlatBufferUtilities import build_flat_reaction, create_state

_connected = False
_waiting_for_response = False
ctx = zmq.Context.instance()
_req_socket = ctx.socket(zmq.REQ)

def send_reaction(stream, reaction: Reaction, callback):
  global _waiting_for_response, _connected
  #try:
  if _connected and not _waiting_for_response:
    flat_reaction = build_flat_reaction(reaction)
    _req_socket.send(flat_reaction)
    if callback:
      callback()
    _waiting_for_response = True
  #except:
    #print('Failed at sending reaction to environment')


def synchronous_receive_message(_req_socket):
  global _waiting_for_response
  if _waiting_for_response:
    by = _req_socket.recv()
    _waiting_for_response = False
    reply = FlatBufferState.GetRootAsFlatBufferState(by, 0)
    state = create_state(reply)
    return state


def receive_environment_state(stream, callback=None):
  global _waiting_for_response, _connected
  if _connected:
    _waiting_for_response = True
    reply = synchronous_receive_message(stream)
    _waiting_for_response = False
    if callback:
      callback(reply)
    return reply
  return None


def setup_connection(tcp_address, tcp_port, on_connect_callback):
  global _connected
  _req_socket.connect("tcp://localhost:%s" % tcp_port)
  on_connect_callback(_req_socket)
  _connected = True


def close_connection(stream, on_disconnect_callback):
  global _connected
  stream.shutdown(1)
  stream.close()
  on_disconnect_callback()
  _connected = False


def start_connect_thread(tcp_ip_address='127.0.0.1', tcp_port=5555, on_connected_callback=print):
  thread = Thread(target=setup_connection, args=(tcp_ip_address, tcp_port, on_connected_callback))
  thread.daemon = True  # Terminate with the rest of the program, is a Background Thread
  thread.start()


def start_send_msg_thread(stream, action, on_connected_callback):
  thread = Thread(target=send_reaction, args=(stream, action, on_connected_callback))
  thread.daemon = True  # Terminate with the rest of the program, is a Background Thread
  thread.start()


def start_receive_environment_state_thread(stream, on_connected_callback):
  thread = Thread(target=receive_environment_state, args=(stream, on_connected_callback))
  thread.daemon = True  # Terminate with the rest of the program, is a Background Thread
  thread.start()
