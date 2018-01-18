import logging
import os
import warnings
from types import coroutine

import numpy as np

import neodroid.messaging as messaging
import neodroid.models as M
from neodroid.utilities.debug import ClientEvents, message_client_event
from neodroid.utilities.environment_launcher import launch_environment
from neodroid.utilities.reaction_factory import verify_motion_reaction, verify_configuration_reaction
from neodroid.utilities.statics import flattened_observation, contruct_action_space, \
  contruct_observation_space


class NeodroidEnvironment(object):
  def __init__(self,
               ip="localhost",
               port=5555,
               connect_to_running=False,
               name='carscene',
               path_to_executables_directory=os.path.join(
                   os.path.dirname(os.path.realpath(__file__)),
                   'environments'),
               debug_logging=False,
               logging_directory='logs',
               on_connected_callback=None,
               on_disconnected_callback=None,
   on_timeout_callback = None):

    self._neodroid_api_version = '0.1.2'

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
    self._external_on_timeout_callback = on_timeout_callback



    # Environment
    self._description = None
    self._observation_space = None
    self._action_space = None

    if not connect_to_running and not self._simulation_instance:
      self._simulation_instance = launch_environment(name, path_to_executables_directory, ip, port)
      if self._simulation_instance:
        if self._debug_logging:
          self._logger.debug('successfully started environment ' + str(
              name))
      else:
        if self._debug_logging:
          self._logger.debug('could not start environment ' + str(name))

    self._message_server = messaging.MessageClient(self._ip,
                                                   self._port,
                                                   on_timeout_callback=self.__on_timeout_callback__,
                                                   on_disconnected_callback=self.__on_disconnected_callback__)
    self._connected_to_server = True
    self.reset()
    print('Using Neodroid API version %s' % self._neodroid_api_version)

    server_version = self._description.api_version
    if self._neodroid_api_version != server_version:
      if server_version == '':
        server_version = '*Unspecified*'
      warnings.warn('Server is using different version %s, complications may occur!' % server_version)

  @property
  def description(self):
    return self._description

  def __iter__(self):
    return self

  def __next__(self):
    if not self._connected_to_server:
      raise StopIteration
    return self.react()

  @coroutine
  def coroutine_generator(self):
    return self

  @message_client_event(event=ClientEvents.CONNECTED)
  def __on_connected_callback__(self):
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  @message_client_event(event=ClientEvents.DISCONNECTED)
  def __on_disconnected_callback__(self):
    self._connected_to_server = False
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  @message_client_event(event=ClientEvents.TIMEOUT)
  def __on_timeout_callback__(self):
    if self._external_on_timeout_callback:
      self._external_on_timeout_callback()

  @property
  def is_connected(self):
    return self._connected_to_server

  def __str__(self):
    return '<NeodroidEnvironment></NeodroidEnvironment>'

  def seed(self, seed):
    np.random.seed(seed)

  @property
  def observation_space(self):
    return self._observation_space

  @property
  def action_space(self):
    return self._action_space


  def maybe_infer_motion_reaction(self, input_reaction, normalise):
    if self._description:
      input_reaction = verify_motion_reaction(input_reaction,
                                              self._description, normalise)
    else:
      input_reaction = verify_motion_reaction(input_reaction, None,False)

    return input_reaction


  def react(self,
            input_reaction=None,
            parameters=None,
            normalise=False,
            on_reaction_sent_callback=None,
            on_step_done_callback=None):

    if self._debug_logging:
      self._logger.debug('Reacting in environment')



    input_reaction = self.maybe_infer_motion_reaction(input_reaction, normalise)
    if parameters is not None:
      input_reaction.parameters = parameters

    message = self._message_server.send_reaction(input_reaction)

    if message:
      flatm = flattened_observation(message)
      if flatm is not None:
        self._observation_space = contruct_observation_space(flatm)
      if message.description:
        self._description = message.description
      return message
    warnings.warn('No valid was message received')
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
      flatm = flattened_observation(message)
      if flatm is not None:
        self._observation_space = contruct_observation_space(flatm)
      if message.description:
        self._description = message.description
        self._action_space = contruct_action_space(self._description)
      return message
    warnings.warn('No valid was message received')
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
    return 0
