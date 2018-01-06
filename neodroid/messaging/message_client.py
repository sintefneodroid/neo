from threading import Thread

import zmq

from .FBSModels import FBSState
from .fbs_utilities import build_reaction, create_state

REQUEST_TIMEOUT = 2500  # Milliseconds
REQUEST_RETRIES = 9


class MessageClient(object):

  def __init__(self,
               tcp_address='localhost',
               tcp_port=5555,
               on_timeout_callback=None,
               on_step_done_callback=None,
               on_connected_callback=None,
               on_disconnected_callback=None
):

    self._tcp_address = tcp_address
    self._tcp_port = tcp_port

    self._use_ipc_medium = False
    self._socket_type = zmq.REQ
    #self._socket_type = zmq.PAIR

    self._on_timeout_callback = on_timeout_callback
    self._on_disconnected_callback = on_disconnected_callback

    self._context = zmq.Context.instance()

    if not self._context:
      raise RuntimeError('Failed to create ZMQ context!')

    self._poller = zmq.Poller()

    self.open_connection()
    self._expecting_response = False

  def open_connection(self):

    self._request_socket = self._context.socket(self._socket_type)
    if not self._request_socket:
      raise RuntimeError('Failed to create ZMQ socket!')

    if self._use_ipc_medium:
      self._request_socket.connect("ipc:///tmp/neodroid/messages")
    else:
      self._request_socket.connect("tcp://%s:%s" % (self._tcp_address, self._tcp_port))

    self._poller.register(self._request_socket, zmq.POLLIN)

  def close_connection(self):
    #if not self._request_socket.closed:
      self._request_socket.setsockopt(zmq.LINGER, 0)
      self._request_socket.close()
      self._poller.unregister(self._request_socket)

  def teardown(self):
    self._context.term()

  def send_reaction(self, reaction):
    if not self._expecting_response:
      e = build_reaction(reaction)
      self._request_socket.send(e)
      self._expecting_response = True

      retries_left = REQUEST_RETRIES

      while self._expecting_response:
        sockets = dict(self._poller.poll(REQUEST_TIMEOUT))

        if sockets.get(self._request_socket):
          response = self._request_socket.recv()
          if not response:
            break

          self._expecting_response = False

          flat_buffer_state = FBSState.GetRootAsFBSState(response, 0)
          state = create_state(flat_buffer_state)
          return state

        else:
          if self._on_timeout_callback:
            self._on_timeout_callback()
          self.close_connection()
          retries_left -= 1

          if retries_left <= 0:
            print('Out of retries, tearing down client')
            self.teardown()
            if self._on_disconnected_callback:
              self._on_disconnected_callback()
            break

          else:
            print('Retrying sending reaction, attempt: %d/%d'%(retries_left,REQUEST_RETRIES))
            self.open_connection()
            self._request_socket.send(e)
