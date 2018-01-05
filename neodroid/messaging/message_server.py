from threading import Thread

import zmq

from .FBSModels import FBSState
from .fbs_utilities import build_reaction, create_state

REQUEST_TIMEOUT = 2500  # Milliseconds
REQUEST_RETRIES = 3


class MessageServer(object):

  def __init__(self, tcp_address, tcp_port):

    self._tcp_address = tcp_address
    self._tcp_port = tcp_port

    self._connected = False
    self._expecting_response = False
    self._use_ipc_medium = False

    self._context = zmq.Context(1)
    self._poller = zmq.Poller()
    self._request_socket = None

    self.reset_retries()

  def reset_retries(self):
    self._retries_left = REQUEST_RETRIES

  def is_connected(self):
    return self._connected

  def setup_connection(self, on_connected_callback=None):

    self._request_socket = self._context.socket(zmq.REQ)

    if self._use_ipc_medium:
      self._request_socket.connect("ipc:///tmp/neodroid/messages")
      print('using inter-process medium')
    else:
      self._request_socket.connect("tcp://%s:%s" % (self._tcp_address, self._tcp_port))
      print('using tcp medium')

    self._poller.register(self._request_socket, zmq.POLLIN)

    self._connected = True

    if on_connected_callback:
      on_connected_callback()

  def close_connection(self, on_disconnect_callback=None):
    if self._connected:
      if self._request_socket:
        self._request_socket.setsockopt(zmq.LINGER, 0)
        self._request_socket.close()
        self._poller.unregister(self._request_socket)

      self._connected = False

      if on_disconnect_callback:
        on_disconnect_callback()

  def __del__(self):
    self.close_connection()

    # self._context.destroy()
    # self._context.term()

  def send_reaction(self, reaction):
    self._last_reaction = reaction
    if self._connected and not self._expecting_response:
      e = build_reaction(reaction)
      self._request_socket.send(e)
      self._expecting_response = True

  def receive_state(self,
                    timeout_callback,
                    on_step_done_callback=None):
    if self._expecting_response:
      while self._expecting_response:

        sockets = dict(self._poller.poll(REQUEST_TIMEOUT))
        if sockets.get(self._request_socket):
          response = self._request_socket.recv()

          if not response:
            break

          self.reset_retries()
          self._expecting_response = False

          flat_buffer_state = FBSState.GetRootAsFBSState(response, 0)
          state = create_state(flat_buffer_state)

          if on_step_done_callback:
            on_step_done_callback(state)
          else:
            return state

        else:
          timeout_callback()
          self.close_connection()
          self._retries_left -= 1
          if self._retries_left <= 0:
            return
          self.setup_connection()
          self.send_reaction(self._last_reaction)

  def start_setup_connection_thread(self, on_connected_callback):
    t = Thread(
        target=self.setup_connection,
        args=([on_connected_callback])
    )
    t.daemon = True  # Terminate with the rest of the program, deamon is a background thread
    t.start()

  def start_send_reaction_thread(self, reaction, on_reaction_sent_callback):
    t = Thread(
        target=self.send_reaction,
        args=(reaction,
              on_reaction_sent_callback)
    )
    t.daemon = True  # Terminate with the rest of the program, deamon is a background thread
    t.start()

  def start_receive_state_thread(self, on_step_done_callback, timeout_callback):
    t = Thread(
        target=self.receive_state,
        args=(timeout_callback,
              on_step_done_callback)
    )
    t.daemon = True  # Terminate with the rest of the program, deamon is a background thread
    t.start()
