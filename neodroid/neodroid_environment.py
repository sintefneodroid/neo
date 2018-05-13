#!/usr/bin/env python3
# coding=utf-8
import time

from neodroid.models import Reaction

__author__ = 'cnheider'

import logging
import os
import warnings
from types import coroutine

import numpy as np

import neodroid.messaging as messaging
import neodroid.models as M
from neodroid.utilities.debug import ClientEvents, message_client_event
from neodroid.utilities.environment import Environment
from neodroid.utilities.environment_launcher import launch_environment
from neodroid.utilities.reaction_factory import (
  verify_configuration_reaction,
  verify_motion_reaction,
  )
from neodroid.utilities.statics import (
  construct_action_space,
  construct_observation_space,
  flattened_observation,
  )


class NeodroidEnvironment(Environment):

  def _configure(self):
    pass

  def _reset(self):
    pass

  def _react(self):
    pass

  def _observer(self):
    pass

  def _display(self):
    pass

  def _close(self):
    pass

  def __init__(
      self,
      *,
      ip='localhost',
      port=6969,
      connect_to_running=False,
      name='grid_world',
      path_to_executables_directory=os.path.join(
          os.path.dirname(os.path.realpath(__file__)), 'environments'
          ),
      debug_logging=False,
      verbose=False,
      logging_directory='logs',
      seed=8,
      on_connected_callback=None,
      on_disconnected_callback=None,
      on_timeout_callback=None,
      ):

    self._neodroid_api_version = '0.1.6'
    self._verbose = verbose
    self.seed(seed)

    # Logging
    self._debug_logging = debug_logging
    if self._debug_logging:
      logging.basicConfig(
          format='%(asctime)s %(new_state)s',
          filename=os.path.join(logging_directory, 'neodroid-log.txt'),
          level=logging.DEBUG,
          )
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
    self._simulator_configuration = None
    self._last_message = None
    self._observation_space = None
    self._action_space = None

    if not connect_to_running and not self._simulation_instance:
      self._simulation_instance = launch_environment(
          name, path_to_executables_directory, ip, port
          )
      if self._simulation_instance:
        if self._debug_logging:
          self._logger.debug(f'successfully started environment {name}')
      else:
        if self._debug_logging:
          self._logger.debug(f'could not start environment {name}')

    self._message_server = messaging.MessageClient(
        self._ip,
        self._port,
        on_timeout_callback=self.__on_timeout_callback__,
        on_connected_callback=self.__on_connected_callback__,
        on_disconnected_callback=self.__on_disconnected_callback__,
        verbose=self._verbose)

    if self._verbose:
      warnings.warn(f'Using Neodroid API version {self._neodroid_api_version}')

    warnings.warn('Connecting to server')
    while self._description is None:
      print('.')
      self.reset()
      time.sleep(0.2)

    self._connected_to_server = True

    server_version = self._simulator_configuration.api_version
    if self._neodroid_api_version != server_version:
      if server_version == '':
        server_version = '*Unspecified*'
      if self._verbose:
        warnings.warn(f'Server is using different version {server_version}, complications may occur!')

  @property
  def description(self):
    return self._description

  @property
  def is_connected(self):
    return self._connected_to_server

  @property
  def observation_space(self):
    return self._observation_space

  @property
  def action_space(self):
    return self._action_space

  def __iter__(self):
    return self

  def __next__(self):
    if not self._connected_to_server:
      return
    return self.react()

  def __str__(self):
    return f'<NeodroidEnvironment>\n' \
           f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n' \
           f'  <ActionSpace>{self.action_space}</ActionSpace>\n' \
           f'  <Description>{self.description}</Description>\n' \
           f'  <IsConnected>{self.is_connected}</IsConnected>\n' \
           f'</NeodroidEnvironment>'

  @staticmethod
  def seed(seed):
    '''

:param seed:
:type seed:
'''
    np.random.seed(seed)

  @staticmethod
  def maybe_infer_motion_reaction(
      input_reaction, normalise, description, verbose=False
      ):
    '''

:param verbose:
:type verbose:
:param input_reaction:
:type input_reaction:
:param normalise:
:type normalise:
:param description:
:type description:
:return:
:rtype:
'''
    if description:
      input_reaction = verify_motion_reaction(
          input_reaction, description, normalise, verbose=verbose
          )
    else:
      input_reaction = verify_motion_reaction(
          input_reaction, None, False, verbose=verbose
          )
    return input_reaction

  @coroutine
  def coroutine_generator(self):
    '''

:return:
:rtype:
'''
    return self

  @message_client_event(event=ClientEvents.CONNECTED)
  def __on_connected_callback__(self):
    '''

'''
    if self._external_on_connected_callback:
      self._external_on_connected_callback()

  @message_client_event(event=ClientEvents.DISCONNECTED)
  def __on_disconnected_callback__(self):
    '''

'''
    self._connected_to_server = False
    if self._external_on_disconnected_callback:
      self._external_on_disconnected_callback()

  @message_client_event(event=ClientEvents.TIMEOUT)
  def __on_timeout_callback__(self):
    '''

'''
    if self._external_on_timeout_callback:
      self._external_on_timeout_callback()

  def react(
      self,
      input_reaction=None,
      parameters=None,
      normalise=False,
      on_reaction_sent_callback=None,
      on_step_done_callback=None,
      single_env=True
      ):
    '''

:param input_reaction:
:type input_reaction:
:param parameters:
:type parameters:
:param normalise:
:type normalise:
:param on_reaction_sent_callback:
:type on_reaction_sent_callback:
:param on_step_done_callback:
:type on_step_done_callback:
:return:
:rtype:
'''
    if single_env:
      if self._verbose:
        warnings.warn('Reacting in environment')
      if self._debug_logging:
        self._logger.debug('Reacting in environment')

      input_reaction = self.maybe_infer_motion_reaction(
          input_reaction, normalise, self._description, verbose=self._verbose
          )
      if parameters is not None:
        input_reaction.parameters = parameters

      new_states, simulator_configuration = self._message_server.send_reactions([input_reaction])

      if new_states:
        self.update_interface_statics(new_states, simulator_configuration)
        return new_states

      warnings.warn('No valid was new_state received')
      if self._debug_logging:
        self._logger.debug('No valid was new_state received')

    else:
      raise NotImplementedError

  @staticmethod
  def maybe_infer_configuration_reaction(input_reaction, description, verbose=False):
    if description:
      input_reaction = verify_configuration_reaction(
          input_reaction, description, verbose=verbose
          )
    else:
      input_reaction = verify_configuration_reaction(
          input_reaction, None, verbose=verbose
          )

    return input_reaction

  def describe(self):
    return self.observe(parameters=M.ReactionParameters(
        terminable=False, describe=True, episode_count=False
        ))

  def display(self, displayables, single_env=True):
    if single_env:
      conf_reaction = Reaction(
          displayables=displayables
          )
      message = self.reset(conf_reaction)
      if message:
        return np.array(flattened_observation(message)), message
    else:
      raise NotImplementedError

  def observe(
      self,
      parameters=M.ReactionParameters(
          terminable=True, describe=True, episode_count=False
          ), single_env=True
      ):
    '''

:param parameters:
:type parameters:
:return:
:rtype:
'''
    if single_env:
      new_states, simulator_configuration = self._message_server.send_reactions(
          [M.Reaction(parameters=parameters)])
      if new_states:

        self.update_interface_statics(new_states, simulator_configuration)
        return new_states
    else:
      raise NotImplementedError

  def reset(self, input_reaction=None, state=None, on_reset_callback=None, single_env=True):
    '''

The environments argument lets you specify which environments to reset.

:param state:
:type state:
:param input_reaction:
:type on_reset_callback: object
'''
    if single_env:
      if self._verbose:
        warnings.warn('Resetting environment')
      if self._debug_logging:
        self._logger.debug('Resetting environment')

      input_reaction = self.maybe_infer_configuration_reaction(
          input_reaction, self._description, verbose=self._verbose
          )
      if state:
        input_reaction.unobservables = state.unobservables

      input_reactions = [input_reaction]  # TODO: Only accepting a single reaction for now
      new_states, simulator_configuration = self._message_server.send_reactions(input_reactions)

      if new_states:
        self.update_interface_statics(new_states, simulator_configuration)
        return new_states
      if self._verbose:
        warnings.warn('No valid was new_state received')
      if self._debug_logging:
        self._logger.debug('No valid was new_state received')
    else:
      raise NotImplementedError
      input_reactions = None
      new_states = self._message_server.send_reactions(input_reactions)

  def close(self, callback=None):
    '''

:param callback:
:type callback:
:return:
:rtype:
'''
    if self._verbose:
      warnings.warn('Closing')
    if self._debug_logging:
      self._logger.debug('Closing')
    # if self._message_server:
    #  self._message_server.__del__()
    if self._simulation_instance is not None:
      self._simulation_instance.terminate()
    if callback:
      callback()
    return 0

  def update_interface_statics(self, new_states, new_simulator_configuration):
    self._last_message = new_states
    # flat_message = flattened_observation(new_state)
    self._simulator_configuration=new_simulator_configuration
    first_environment = list(self._last_message.values())[0]
    observables = first_environment.observables
    if observables is not None:
      self._observation_space = construct_observation_space(observables)
    if first_environment.description:
      self._description = first_environment.description
      self._action_space = construct_action_space(self._description)


if __name__ == '__main__':
  import argparse
  from tqdm import tqdm

  parser = argparse.ArgumentParser(description='PG Agent')
  parser.add_argument(
      'ENVIRONMENT_NAME',
      type=str,
      nargs='+',
      metavar='ENVIRONMENT_NAME',
      help='name of the environment to run',
      )
  args = parser.parse_args()

  env = NeodroidEnvironment(name=args.ENVIRONMENT_NAME)

  observation_session = tqdm(env, leave=False)
  for state in observation_session:
    if state.terminated:
      print('Interrupted', state.signal)
