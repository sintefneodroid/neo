from threading import Thread

import zmq

from neodroid.utilities import debug_print
from .FlatBufferModels import FlatBufferState as FlatBufferState
from .FlatBufferUtilities import build_flat_reaction, create_state

_connected = False
_waiting_for_response = False
_ctx = zmq.Context.instance()
_req_socket = _ctx.socket(zmq.REQ)
_use_inter_process_communication = False


def send_reaction(stream, reaction, callback):
  global _waiting_for_response, _connected
  if _connected and not _waiting_for_response:
    flat_reaction = build_flat_reaction(reaction)
    stream.send(flat_reaction)
    if callback:
      callback()
    _waiting_for_response = True


def synchronous_receive_message(stream):
  global _waiting_for_response
  if _waiting_for_response:
    by = stream.recv()
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
  if _use_inter_process_communication:
    # _req_socket.connect("inproc://neodroid")
    _req_socket.connect("ipc:///tmp/neodroid/0")
    print('using inter process communication protocol')
  else:
    # _req_socket.connect("tcp://localhost:%s" % tcp_port)
    _req_socket.connect("tcp://%s:%s" % (tcp_address, tcp_port))
    print('using tcp communication protocol')
  on_connect_callback(_req_socket)
  _connected = True


def close_connection(stream, on_disconnect_callback):
  global _connected
  stream.shutdown(1)
  stream.close()
  on_disconnect_callback()
  _connected = False


def start_connect_thread(tcp_ip_address='127.0.0.1',
                         tcp_port=5555,
                         on_connected_callback=debug_print):
  thread = Thread(
      target=setup_connection,
      args=(tcp_ip_address, tcp_port, on_connected_callback))
  thread.daemon = True
  # Terminate with the rest of the program
  # is a Background Thread
  thread.start()


def start_send_msg_thread(stream, action, on_connected_callback):
  thread = Thread(
      target=send_reaction, args=(stream, action, on_connected_callback))
  thread.daemon = True
  # Terminate with the rest of the program,
  # is a Background Thread
  thread.start()


def start_receive_environment_state_thread(stream, on_connected_callback):
  thread = Thread(
      target=receive_environment_state, args=(stream, on_connected_callback))
  thread.daemon = True
  # Terminate with the rest of the program
  # is a Background Thread
  thread.start()
