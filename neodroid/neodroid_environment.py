import logging
import os
import shlex
import subprocess
import sys
import time
import warnings
from types import coroutine

import numpy as np

import neodroid.messaging as messaging
import neodroid.models as M
from neodroid.utilities.action_space import ActionSpace
from neodroid.utilities.reaction_factory import verify_motion_reaction, verify_configuration_reaction
from neodroid.utilities.statics import flattened_observation, contruct_action_space


class NeodroidEnvironment(object):
  def __init__(self,
               ip="localhost",
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
    self._ip = ip
    self._port = port
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback

    self._connected_to_server = True

    # Environment
    self._description = None
    self._state = None
    self._observation_space = np.zeros(1)
    self._action_space = ActionSpace()

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

    self._message_server = messaging.MessageClient(self._ip,
                                                   self._port,
                                                   on_timeout_callback=self.__on_timeout_callback__,
                                                   on_disconnected_callback=self.__on_disconnected_callback__)

    self.reset()

  @property
  def description(self):
    return self._description

  def __iter__(self):
    return self

  def __next__(self):
    return self.react()

  @coroutine
  def coroutine_generator(self):
    return self

  def __start_instance__(self, name, path_to_executables_directory, ip, port):
    path_to_executable = os.path.join(path_to_executables_directory,
                                      name + '.exe')
    if sys.platform != 'win32':
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
    warnings.warn('Connected to server')
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  def __on_disconnected_callback__(self):
    self._connected_to_server = False
    warnings.warn('Disconnected from server')
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  def __on_timeout_callback__(self):
    warnings.warn('Connection timeout')

  def is_connected(self):
    return self._connected_to_server

  def __str__(self):
    return '<NeodroidEnvironment></NeodroidEnvironment>'

  def seed(self, seed):
    np.random.seed(seed)

  def __observation_space__(self):
    return self._observation_space

  def __action_space__(self):
    return self._action_space

  def maybe_infer_motion_reaction(self, input_reaction):
    if self._description:
      input_reaction = verify_motion_reaction(input_reaction,
                                              self._description)
    else:
      input_reaction = verify_motion_reaction(input_reaction, None)

    return input_reaction

  def get_environment_description(self):
    return self._description

  def react(self,
            input_reaction=None,
            parameters=None,
            on_reaction_sent_callback=None,
            on_step_done_callback=None):

    if self._debug_logging:
      self._logger.debug('Reacting in environment')

    input_reaction = self.maybe_infer_motion_reaction(input_reaction)
    if parameters is not None:
      input_reaction.parameters = parameters

    message = self._message_server.send_reaction(input_reaction)

    if message:
      self._observation_space = flattened_observation(message)
      self._state = message
      if message.description:
        self._description = message.description
      return message
    if self._debug_logging:
      self._logger.debug('No valid was message received')

  def maybe_infer_configuration_reaction(self, input_reaction):
    if self._description:
      input_reaction = verify_configuration_reaction(input_reaction,
                                                     self._description)
    else:
      input_reaction = verify_configuration_reaction(input_reaction, None)

    return input_reaction

  def observe(self,
              parameters=M.ReactionParameters(
                  terminable=True,
                  describe=True,
                  episode_count=False)
              ):
    return self._message_server.send_reaction(M.Reaction(parameters))

  def reset(self, input_reaction=None, state=None, on_reset_callback=None):
    """

    The environments argument lets you specify which environments to reset.

    :param input_reaction:
    :type on_reset_callback: object
    """
    if self._debug_logging:
      self._logger.debug('Resetting enviroment')

    input_reaction = self.maybe_infer_configuration_reaction(input_reaction)
    if state:
      input_reaction.unobservables = state.unobservables

    message = self._message_server.send_reaction(input_reaction)

    if message:
      self._observation_space = flattened_observation(message)
      self._state = message
      if message.description:
        self._description = message.description
        self._action_space = contruct_action_space(self._description)
      return message
    if self._debug_logging:
      self._logger.debug('No valid was message received')

  def close(self, callback=None):
    if self._debug_logging:
      self._logger.debug('Close')
    # if self._message_server:
    #  self._message_server.__del__()
    if self._simulation_instance is not None:
      self._simulation_instance.terminate()
    if callback:
      callback()
