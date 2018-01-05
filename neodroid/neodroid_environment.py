import logging
import os
import shlex
import subprocess
import sys
import time
import warnings

import numpy as np

import neodroid.messaging as messaging
import neodroid.modeling as modeling
from neodroid import Reaction
from neodroid.modeling.reaction_parameters import ReactionParameters
from neodroid.utilities.action_space import ActionSpace
from neodroid.utilities.reaction_factory import verify_motion_reaction, verify_configuration_reaction
from neodroid.utilities.statics import flattened_observation, contruct_action_space


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
    self._ip = ip
    self._port = port
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback

    # Environment
    self._environment_description = None
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


    self._message_server = messaging.MessageServer(self._ip,self._port)
    self._message_server.setup_connection()

    time.sleep(seconds_before_connect / 4)
    reaction = modeling.Reaction(ReactionParameters(False,False,True,False,True))
    self.reset(reaction)

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
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  def __on_disconnected_callback__(self):
    warnings.warn('Disconnected from server')
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  def __on_step_done_callback__(self):
    pass

  def __get_state__(self, on_step_done_callback=None):
    if on_step_done_callback:
      self._message_server.start_receive_state_thread(on_step_done_callback,
                                           self.__timeout_callback__)
    else:
      return self._message_server.receive_state(self.__timeout_callback__)

  def __timeout_callback__(self):
    warnings.warn('Timeout')
    #self._message_server.close_connection(
    #    on_disconnect_callback=self.__on_disconnected_callback__())
    #self.__connect__()

  def __del__(self):
    self.close()

  def __str__(self):
    return '<NeodroidEnvironment>'

  def is_connected(self):
    return self._message_server.is_connected()

  def seed(self, seed):
    np.random.seed(seed)

  def __observation_space__(self):
    return self._observation_space

  def run_brownian_motion(self, iterations=1):
    message=None
    for i in range(iterations):
      rp = ReactionParameters(True,True)
      message = self.react(self._action_space.sample(), rp)
    return message

  def __action_space__(self):
    return self._action_space

  def maybe_infer_motion_reaction(self, input_reaction):
    if self._environment_description:
      input_reaction = verify_motion_reaction(input_reaction,
                                              self._environment_description)
    else:
      input_reaction = verify_motion_reaction(input_reaction, None)

    return input_reaction

  def react(self,
            input_reaction=None,
            parameters=None,
            on_reaction_sent_callback=None,
            on_step_done_callback=None):

    if self._debug_logging:
      self._logger.debug('Reacting')

    input_reaction = self.maybe_infer_motion_reaction(input_reaction)
    if parameters is not None:
      input_reaction.set_parameters(parameters)

    if self._message_server.is_connected():
      if on_reaction_sent_callback:
        self._message_server.start_send_reaction_thread(input_reaction,
                                             on_reaction_sent_callback)
      else:
        self._message_server.send_reaction(input_reaction)

      message = self.__get_state__(on_step_done_callback)
      if message:
        self._observation_space = flattened_observation(message)
        self._state = message
        if message.get_environment_description():
          self._environment_description = message.get_environment_description()
        return message
    if self._debug_logging:
      self._logger.debug('Is not connected to environment')
    return None

  def maybe_infer_configuration_reaction(self, input_reaction):
    if self._environment_description:
      input_reaction = verify_configuration_reaction(input_reaction,
                                                     self._environment_description)
    else:
      input_reaction = verify_configuration_reaction(input_reaction, None)

    return input_reaction

  def observe(self):
    self._message_server.send_reaction(Reaction(ReactionParameters(True,False,False,False,True)))
    return self.__get_state__()

  def reset(self, input_reaction=None, on_reset_callback=None):
    """

    The environments argument lets you specify which environments to reset.

    :param input_reaction:
    :type on_reset_callback: object
    """
    if self._debug_logging:
      self._logger.debug('Resetting')

    if self._message_server.is_connected():

      input_reaction = self.maybe_infer_configuration_reaction(input_reaction)

      if on_reset_callback:
        self._message_server.start_send_reaction_thread(input_reaction, on_reset_callback)
      else:
        self._message_server.send_reaction(input_reaction)

      message = self.__get_state__()

      if message:
        self._observation_space = flattened_observation(message)
        self._state = message
        if message.get_environment_description():
          self._environment_description = message.get_environment_description()
          self._action_space = contruct_action_space(self._environment_description)
        return message
    return None

  def close(self, callback=None):
    if self._debug_logging:
      self._logger.debug('Close')
    #if self._message_server:
    #  self._message_server.__del__()
    if self._message_server.is_connected():
      if self._simulation_instance is not None:
        self._simulation_instance.terminate()
      if callback:
        callback()
