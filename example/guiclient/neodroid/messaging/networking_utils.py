import socket
from _socket import socket as Socket
from threading import Thread

import msgpack

from neodroid.models import Reaction

_connected = False
_waiting_for_response = False
_unpacker = msgpack.Unpacker(use_list=False)  # , object_hook=EnvironmentState().unpack)


def send_reaction(stream, reaction: Reaction, callback):
  global _waiting_for_response, _connected
  if _connected and not _waiting_for_response:
    stream.send(msgpack.packb(reaction.to_dict(), use_bin_type=True))
    if callback:
      callback()
    _waiting_for_response = True


def recvall(stream, buffer_size=2):
  buf = stream.recv(buffer_size)
  while buf:
    yield buf
    print('yielding')
    buf = stream.recv(buffer_size)


def recv_msg(stream, callback=None):
  global _waiting_for_response
  if _waiting_for_response:
    reply = None
    while not reply:
      _unpacker.feed(stream.recv(1))
      for value in _unpacker:  #### Use unpackb instead has ...Unpacker's object_hook callback receives a dict; the object_pairs_hook callback may instead be used to receive a list of key-value pairs.
        reply = value
    _waiting_for_response = False
    callback(reply)
    # return reply


def synchronous_receive_message(stream):
  global _waiting_for_response
  if _waiting_for_response:
    reply = None
    while not reply:
      _unpacker.feed(stream.recv(1))
      for value in _unpacker:
        reply = value
    _waiting_for_response = False
    return reply


def receive_environment_state(stream, callback=None):
  global _waiting_for_response, _connected
  if _connected:
    _waiting_for_response = True
    # reply = stream.recv(4096*2*2)
    reply = recv_msg(stream)
    # reply = b''.join(recvall(stream))
    # reply = msgpack.unpackb(reply)
    _waiting_for_response = False
    # reply = msgpack.unpackb(reply, use_list=False)#, object_hook=EnvironmentState)
    if callback:
      callback(reply)
    return reply
  return None


def setup_connection(tcp_address, tcp_port, on_connect_callback):
  global _connected
  stream_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
  stream_socket.connect((tcp_address, tcp_port))
  on_connect_callback(stream_socket)
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


def start_recv_msg_thread(stream, on_receive_callback):
  thread = Thread(target=recv_msg, args=(stream, on_receive_callback))
  thread.daemon = True  # Terminate with the rest of the program, is a Background Thread
  thread.start()


def start_receive_environment_state_thread(stream, on_connected_callback):
  thread = Thread(target=receive_environment_state, args=(stream, on_connected_callback))
  thread.daemon = True  # Terminate with the rest of the program, is a Background Thread
  thread.start()
