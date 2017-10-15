import functools
import logging
import os
import shlex
import subprocess
import time

from .messaging import (send_reaction, start_connect_thread,
                        synchronous_receive_message)
from .utilities import debug_print


class NeodroidEnvironment(object):
  def __init__(self,
               ip="127.0.0.1",
               port=5555,
               on_connected_callback=debug_print,
               connect_to_running=False,
               name='carscene.exe',
               path_to_executables_directory=os.path.join(
                   os.path.dirname(os.path.realpath(__file__)),
                   'environments')):

    # Logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG)
    self._logger = logging.getLogger(__name__)
    self._logger.debug('Initializing Environment')

    # Simulation
    self._simulation_instance = None

    # Networking
    self._stream = None
    self._connected = False
    self._awaiting_response = False

    if not connect_to_running and not self._simulation_instance:
      if self._start_instance(name, path_to_executables_directory, ip,
                              port):
        self._logger.debug('successfully started environment ' + str(
            name))
        time.sleep(8)
      else:
        self._logger.debug('could not start environment ' + str(name))
    self._connect(ip, port, on_connected_callback)

  def _start_instance(self, name, path_to_executables_directory, ip, port):
    path_to_executable = os.path.join(path_to_executables_directory, name)
    args = shlex.split(
        '-ip ' + str(ip) + ' -port ' + str(port) +
        ' -screen-fullscreen 0 -screen-height 500 -screen-width 500'
    )  # -batchmode -nographics')
    print([path_to_executable] + args)
    self._simulation_instance = subprocess.Popen(
        [path_to_executable] +
        args)  # Figure out have to parameterise unity executable
    # time.sleep(8) # Not good a callback would be better.
    if self._simulation_instance:
      self._logger.debug('Started executable ' + str(name))
      return True
    else:
      self._logger.debug('Failed to start executable ' + str(name))
      return False

  def _internal_on_connected_callback(self, stream, on_connected_callback):
    self._stream = stream
    self._connected = True
    on_connected_callback()

  def is_connected(self):
    return self._connected

  def _connect(self, ip, port, on_connected_callback):
    self._logger.debug('Connecting to server')
    start_connect_thread(ip, port,
                         functools.partial(
                             self._internal_on_connected_callback,
                             on_connected_callback=on_connected_callback))

  def get_environment(self):
    message = synchronous_receive_message(self._stream)
    return message

  def step(self, input_reaction, callback=None):
    self._logger.debug('Step')
    sent_callback = debug_print
    self._awaiting_response = True
    send_reaction(self._stream, input_reaction, sent_callback)
    if callback:
      # recv_msg(self._stream, callback)
      self._awaiting_response = False
    else:
      message = synchronous_receive_message(self._stream)
      self._awaiting_response = False
      return message

  def reset(self, input_reaction, callback=None):
    self._logger.debug('Reset')
    send_reaction(self._stream, input_reaction, callback)
    message = synchronous_receive_message(self._stream)
    return message

  def close(self, callback=None):
    self._logger.debug('Close')
    if self._connected:
      self._stream.close()
      self._stream = None
      self._connected = False
      if self._simulation_instance is not None:
        self._simulation_instance.terminate()
      if callback:
        callback()

  def __del__(self):
    self.close()

  def __str__(self):
    return '<NeodroidEnvironment>'
