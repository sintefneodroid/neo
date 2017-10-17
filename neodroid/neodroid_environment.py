import logging
import os
import shlex
import subprocess
import time

import neodroid.messaging as messaging


class NeodroidEnvironment(object):
  def __init__(self,
               ip="127.0.0.1",
               port=5555,
               connect_to_running=False,
               name='carscene.exe',
               path_to_executables_directory=os.path.join(
                   os.path.dirname(os.path.realpath(__file__)),
                   'environments'),
               seconds_before_connect=8,
               debug_logging=False,
               on_connected_callback=None,
               on_disconnected_callback=None):

    # Logging
    self._debug_logging = debug_logging
    if self._debug_logging:
      logging.basicConfig(filename='log.txt', level=logging.DEBUG)
      self._logger = logging.getLogger(__name__)
      self._logger.debug('Initializing Environment')

    # Simulation
    self._simulation_instance = None

    # Networking
    self._connected = False
    self._awaiting_response = False
    self._ip = ip
    self._port = port
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback

    if not connect_to_running and not self._simulation_instance:
      if self.__start_instance__(name, path_to_executables_directory, ip,
                                 port):
        if self._debug_logging:
          self._logger.debug('successfully started environment ' + str(
              name))
          self._logger.debug('waiting ' + str(seconds_before_connect) +
                             'seconds for ' + str(name) + ' to accept clients')
        time.sleep(seconds_before_connect)
      else:
        if self._debug_logging:
          self._logger.debug('could not start environment ' + str(name))
    self.__connect__()

  def __start_instance__(self, name, path_to_executables_directory, ip, port):
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

  def __on_connected_callback__(self):
    self._connected = True
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  def on_disconnected_callback(self):
    self._connected = False
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  def is_connected(self):
    return self._connected

  def __connect__(self):
    if self._debug_logging:
      self._logger.debug('Connecting to server')
    messaging.start_setup_connection_thread(self.__on_connected_callback__,
                                            self._ip,
                                            self._port)

  def step(self,
           input_reaction,
           on_step_done_callback=None,
           on_reaction_sent_callback=None):
    if self._debug_logging:
      self._logger.debug('Step')
    self._awaiting_response = True
    if self._connected:
      if on_reaction_sent_callback:
        messaging.start_send_reaction_thread(input_reaction,
                                             on_reaction_sent_callback)
      else:
        messaging.send_reaction(input_reaction)

      if on_step_done_callback:
        messaging.start_receive_state_thread(on_step_done_callback,
                                             self.__timeout_callback__)
        self._awaiting_response = False
        return
      else:
        message = messaging.receive_state(self.__timeout_callback__)
        self._awaiting_response = False
        if message:
          return (message.get_observers(),
                  message.get_reward_for_last_step(),
                  message.get_interrupted())
    else:
      if self._debug_logging:
        self._logger.debug('Is not connected to environment')
    return (None,
            None,
            None)

  def describe(self):
    if self._debug_logging:
      self._logger.debug('Describe')

  def __timeout_callback__(self):
    self._connected = False
    print('Trying to reconnect to server')
    messaging.close_connection(
        on_disconnect_callback=self.on_disconnected_callback())
    self.__connect__()

  def reset(self, input_configuration):  # , on_reset_callback=None):
    if self._debug_logging:
      self._logger.debug('Reset')

    # messaging.start_send_configuration_thread(input_configuration,
    #                                      on_reset_callback)
    # message = messaging.receive_state(self.__timeout_callback__())
    return self.step(input_configuration)

  def close(self, callback=None):
    if self._debug_logging:
      self._logger.debug('Close')
    if self._connected:
      self._connected = False
      if self._simulation_instance is not None:
        self._simulation_instance.terminate()
      if callback:
        callback()

  def __del__(self):
    self.close()

  def __str__(self):
    return '<NeodroidEnvironment>'
