import logging
import os
import shlex
import subprocess
import time
import warnings
from collections import namedtuple

import numpy as np

import neodroid.messaging as messaging
from neodroid.models import Reaction
from neodroid.utilities.reaction_factory import verify_reaction


class NeodroidEnvironment(object):
  def __init__(self,
               ip="127.0.0.1",
               port=5555,
               connect_to_running=False,
               name='carscene',
               path_to_executables_directory=os.path.join(
                   os.path.dirname(os.path.realpath(__file__)),
                   'environments'),
               seconds_before_connect=8,
               debug_logging=False,
               logging_directory='logs',
               on_connected_callback=None,
               on_disconnected_callback=None):

    # Logging
    self._debug_logging = debug_logging
    if self._debug_logging:
      logging.basicConfig(format='%(asctime)s %(message)s',
                          filename=os.path.join(logging_directory,
                                                'neodroid-log.txt'),
                          level=logging.DEBUG)
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

    # Environment
    self._latest_received_state = None
    self._first_received_state = None

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
    time.sleep(seconds_before_connect/4)
    self.reset()
    self.reset()
    self.reset()
    self.reset()
    self.reset()
    self.reset()

  def __start_instance__(self, name, path_to_executables_directory, ip, port):
    path_to_executable = os.path.join(path_to_executables_directory,
                                      name + '.x86')
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
      if self._debug_logging:
        self._logger.debug('Successfully started executable ' + str(name))
      return True
    else:
      if self._debug_logging:
        self._logger.debug('Failed to start executable ' + str(name))
      return False

  def __on_connected_callback__(self):
    self._connected = True
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  def __on_disconnected_callback__(self):
    self._connected = False
    warnings.warn('Disconnected from server')
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  def __on_step_done_callback__(self):
    self._awaiting_response = False

  def __connect__(self):
    if self._debug_logging:
      self._logger.debug('Connecting to server')
    messaging.start_setup_connection_thread(self.__on_connected_callback__,
                                            self._ip,
                                            self._port)

  def __get_state__(self, on_step_done_callback=None):
    if on_step_done_callback:
      messaging.start_receive_state_thread(on_step_done_callback,
                                           self.__timeout_callback__)
    else:
      return messaging.receive_state(self.__timeout_callback__)

  def __timeout_callback__(self):
    self._connected = False
    print('Trying to reconnect to server')
    messaging.close_connection(
        on_disconnect_callback=self.__on_disconnected_callback__())
    self.__connect__()

  def __del__(self):
    self.close()

  def __str__(self):
    return '<NeodroidEnvironment>'

  def is_connected(self):
    return self._connected

  def flat_observation(self, message):
    return np.array([obs.get_position()+ obs.get_rotation()+
                        obs.get_direction() for
                       obs in
                       message.get_observers().values()]).flatten()

  def seed(self, seed):
    pass

  def __observation_space__(self):
    if self._first_received_state:
      return self.flat_observation(self._first_received_state)
    return np.zeros(1) # Do not crash

  def sample_action_space(self, binary=True, discrete=False, one_hot=False):
    if one_hot:
      idx = np.random.randint(0,self._num_actions)
      zeros = np.zeros(self._num_actions)
      zeros[idx]=1
      return zeros
    else:
      if discrete:
        if binary:
          return np.random.randint(-1,2,size=int(self._num_actions/2))
        else:
          return np.random.randint(0,2,size=self._num_actions)
      else:
        if binary:
          return np.random.random_sample(int(self._num_actions/2))-0.5
        else:
          return np.random.random_sample(self._num_actions)



  def __action_space__(self):
    self._num_actions=0
    if self._first_received_state:
      for actor in self._first_received_state.get_actors().values():
        for motor in actor.get_motors().values():
          if motor.get_binary():
            self._num_actions+=2
          else:
            self._num_actions+=1
    else:
      self._num_actions = 1 # Do not crash
    action_space = namedtuple('action_space', ('n', 'sample'))
    return action_space(self._num_actions, self.sample_action_space)

  def maybe_infer_reaction(self, input_reaction):
    if self._latest_received_state:
      input_reaction = verify_reaction(input_reaction, self._latest_received_state.get_actors().values())
    else:
      input_reaction = verify_reaction(input_reaction, None)
    return input_reaction

  def react(self,
            input_reaction=None,
            on_reaction_sent_callback=None,
            on_step_done_callback=None):

    if self._debug_logging:
      self._logger.debug('Reacting')

    input_reaction = self.maybe_infer_reaction(input_reaction)

    if self._connected:
      if on_reaction_sent_callback:
        messaging.start_send_reaction_thread(input_reaction,
                                             on_reaction_sent_callback)
      else:
        messaging.send_reaction(input_reaction)

      self._awaiting_response = True

      message = self.__get_state__(on_step_done_callback)
      if message:
        self._awaiting_response = False
        self._latest_received_state = message
        if self._first_received_state == None:
          self._first_received_state = message
        return message
    if self._debug_logging:
      self._logger.debug('Is not connected to environment')
    return None

  def reset(self, input_configuration=[], on_reset_callback=None):
    if self._debug_logging:
      self._logger.debug('Resetting')

    if self._connected:
      if on_reset_callback:
        messaging.start_send_reaction_thread(Reaction(True, input_configuration, []),
                                             on_reset_callback)
      else:
        messaging.send_reaction(Reaction(True, input_configuration, []))

      self._awaiting_response = True

      message = self.__get_state__()

      if message:
        self._awaiting_response = False
        self._latest_received_state = message
        if self._first_received_state == None:
          self._first_received_state = message
        return message
    return None

  def close(self, callback=None):
    if self._debug_logging:
      self._logger.debug('Close')
    if self._connected:
      self._connected = False
      if self._simulation_instance is not None:
        self._simulation_instance.terminate()
      if callback:
        callback()
