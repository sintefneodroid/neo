from threading import Thread

import zmq

from .FBSModels import FBSState
from .FBSUtilities import build_flat_reaction, create_state

_connected = False
_waiting_for_response = False
_ctx = zmq.Context.instance()
# _ctx = zmq.Context()
_req_socket = _ctx.socket(zmq.REQ)
_use_inter_process_communication = False
_time_out = 2000  # Milliseconds


def send_reaction(reaction, info):
  global _waiting_for_response, _connected
  if _connected and not _waiting_for_response:
    flat_reaction = build_flat_reaction(reaction, info)
    _req_socket.send(flat_reaction)
    _waiting_for_response = True


def receive_state(timeout_callback,
                  on_step_done_callback=None):
  global _waiting_for_response
  if _waiting_for_response:
    if _req_socket.poll(timeout=_time_out) is 0:
      timeout_callback()
      return
    by = _req_socket.recv()
    _waiting_for_response = False
    flat_buffer_state = FBSState.GetRootAsFBSState(by, 0)
    state = create_state(flat_buffer_state)
    if on_step_done_callback:
      on_step_done_callback(state)
    else:
      return state


def setup_connection(tcp_address, tcp_port, on_connected_callback=None):
  global _ctx, _connected, _req_socket
  _req_socket = _ctx.socket(zmq.REQ)
  if _use_inter_process_communication:
    _req_socket.connect("ipc:///tmp/neodroid/messages")
    # _req_socket.connect("inproc://neodroid")
    print('using inter-process communication protocol')
  else:
    _req_socket.connect("tcp://%s:%s" % (tcp_address, tcp_port))
    print('using tcp communication protocol')
  _connected = True
  if on_connected_callback:
    on_connected_callback()


def close_connection(on_disconnect_callback=None):
  global _ctx, _connected, _req_socket
  _req_socket.setsockopt(zmq.LINGER, 0)
  _req_socket.close()
  # del _req_socket
  _ctx.destroy()
  _ctx.term()
  del _ctx
  # _ctx = zmq.Context()
  _ctx = zmq.Context.instance()
  _connected = False
  if on_disconnect_callback:
    on_disconnect_callback()


def start_setup_connection_thread(on_connected_callback,
                                  tcp_ip_address='127.0.0.1',
                                  tcp_port=5555):
  thread = Thread(
      target=setup_connection,
      args=(tcp_ip_address, tcp_port, on_connected_callback))
  thread.daemon = True
  # Terminate with the rest of the program
  # is a Background Thread
  thread.start()


def start_send_reaction_thread(reaction, on_reaction_sent_callback):
  thread = Thread(target=send_reaction,
                  args=(reaction,
                        on_reaction_sent_callback))
  # Terminate with the rest of the program
  thread.daemon = True  # is a Background Thread
  thread.start()


def start_receive_state_thread(on_step_done_callback, timeout_callback):
  thread = Thread(target=receive_state,
                  args=(timeout_callback,
                        on_step_done_callback))
  # Terminate with the rest of the program
  thread.daemon = True  # is a Background Thread
  thread.start()
