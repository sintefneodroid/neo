#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from typing import Mapping, Union

from neodroid import DEFAULT_ENVIRONMENTS_PATH
from neodroid.factories.multi_reaction_factory import maybe_infer_multi_motion_reaction
from neodroid.interfaces import SimulatorConfiguration
from neodroid.interfaces.spaces import ActionSpace, ObservationSpace, SignalSpace
from neodroid.interfaces.specifications import EnvironmentDescription, EnvironmentSnapshot
from neodroid.utilities import launch_environment

__author__ = 'cnheider'

import neodroid.interfaces.specifications as M
from .networking_environment import NetworkingEnvironment


class NeodroidEnvironment(NetworkingEnvironment):

  @property
  def description(self) -> Mapping[str, EnvironmentDescription]:
    while not self._description:
      self.describe()
    return self._description

  @property
  def observation_space(self) -> [str, ObservationSpace]:
    while not self._observation_space:
      self.describe()
    return self._observation_space

  @property
  def action_space(self) -> Mapping[str, ActionSpace]:
    while not self._action_space:
      self.describe()
    return self._action_space

  @property
  def signal_space(self) -> Mapping[str, SignalSpace]:
    while not self._signal_space:
      self.describe()
    return self._signal_space

  @property
  def simulator_configuration(self) -> SimulatorConfiguration:
    while not self._simulator_configuration:
      self.describe()
    return self._simulator_configuration

  @property
  def neodroid_api_version(self):
    return '0.4.0'

  def _setup_connection(self, auto_describe=True):
    super()._setup_connection(auto_describe)
    if auto_describe:
      # TODO: WARN ABOUT WHEN INDIVIDUAL OBSERVATIONS AND UNOBSERVABLES ARE UNAVAILABLE due to simulator
      #  configuration

      logging.warning(f'Using Neodroid API version {self.neodroid_api_version}')

      server_version = self.simulator_configuration.api_version
      logging.info(f'Server API version: {server_version}')

      if self.neodroid_api_version != server_version:
        if server_version == '':
          server_version = '*Unspecified*'

        logging.warning(f'Server is using different version {server_version}, complications may occur!')

  def __init__(self,
               *,
               environment_name: str = None,
               clones: int = 0,
               path_to_executables_directory: Union[str, Path] = DEFAULT_ENVIRONMENTS_PATH,
               headless: bool = False,
               **kwargs
               ):
    super().__init__(**kwargs)

    # Environment
    self._description = None
    self._simulator_configuration = None
    self._last_message = None
    self._observation_space = None
    self._action_space = None
    self._signal_space = None

    # Simulation
    self._simulation_instance = None
    self._clones = clones

    if not self._connect_to_running and not self._simulation_instance and environment_name is not None:
      self._simulation_instance = launch_environment(environment_name,
                                                     ip=self._ip,
                                                     port=self._port,
                                                     path_to_executables_directory=path_to_executables_directory,
                                                     headless=headless)
      if self._simulation_instance:
        logging.debug(f'successfully started environment {environment_name}')
      else:

        logging.debug(f'could not start environment {environment_name}')

    self._setup_connection()

  def configure(self, *args, **kwargs) -> Mapping[str, EnvironmentSnapshot]:
    return self.reset()

  def react(
      self,
      input_reactions=None,
      *,
      parameters=None,
      normalise=False,
      on_reaction_sent_callback=None,
      on_step_done_callback=None,
      **kwargs) -> Mapping[str, EnvironmentSnapshot]:
    '''

:param input_reactions:
:type input_reactions:
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
    logging.info('Reacting in environment')

    if isinstance(input_reactions, list) and len(input_reactions) > 0 and isinstance(input_reactions[0],
                                                                                     M.Reaction):
      pass
    else:
      if input_reactions is None:
        parameters = M.ReactionParameters(episode_count=True,
                                          step=True,
                                          terminable=True
                                          )
        input_reactions = [M.Reaction(parameters=parameters)]
      elif not isinstance(input_reactions, M.Reaction):
        input_reactions = maybe_infer_multi_motion_reaction(input_reactions=input_reactions,
                                                            normalise=normalise,
                                                            descriptions=self._description,
                                                            action_space=self.action_space
                                                            )

    new_states, simulator_configuration = self._message_server.send_reactions(input_reactions)

    if new_states:
      self.update_interface_attributes(new_states, simulator_configuration)
      return new_states

    logging.warning('No valid was new_state received')

  def display(self, displayables) -> Mapping[str, EnvironmentSnapshot]:
    conf_reaction = M.Reaction(displayables=displayables)
    message = self.reset(conf_reaction)
    if message:
      return message

  def reset(self,
            input_reactions=None,
            state=None,
            on_reset_callback=None) -> Mapping[
    str, EnvironmentSnapshot]:
    logging.info('Resetting environment')

    if input_reactions is None:
      parameters = M.ReactionParameters(terminable=True,
                                        describe=True,
                                        episode_count=False,
                                        reset=True)
      input_reactions = [M.Reaction(parameters=parameters)]

    new_states, simulator_configuration = self._message_server.send_reactions(input_reactions)
    if new_states:
      self.update_interface_attributes(new_states, simulator_configuration)
      return new_states
    logging.warning('No valid was new_state received')

  def _close(self, callback=None):
    '''

:param callback:
:type callback:
:return:
:rtype:
'''
    logging.info('Closing')
    # if self._message_server:
    #  self._message_server.__del__()
    if self._simulation_instance is not None:
      self._simulation_instance.terminate()
    if callback:
      callback()
    return 0

  def describe(self,
               parameters=M.ReactionParameters(terminable=False,
                                               describe=True,
                                               episode_count=False)) -> Mapping[str, EnvironmentSnapshot]:
    '''

    :param parameters:
    :type parameters:
    :return:
    :rtype:
    '''
    reaction = M.Reaction(parameters=parameters)
    new_states, simulator_configuration = self._message_server.send_reactions([reaction])

    if new_states:
      self.update_interface_attributes(new_states, simulator_configuration)
      return new_states

  def update_interface_attributes(self, new_states, new_simulator_configuration):
    self._last_message = new_states
    self._simulator_configuration = new_simulator_configuration
    envs = self._last_message.items()
    first_environment = next(iter(envs))[1]
    if first_environment.description:
      self._description = {k:env.description for k, env in envs}
      self._action_space = next(iter({k:ActionSpace.from_environment_description(env.description) for k,
                                                                                                      env in
                                      envs}.values()))
      self._observation_space = next(iter({k:ObservationSpace.from_environment_description(env.description)
                                           for k, env in envs}.values()))

  def __repr__(self):
    return (f'<NeodroidEnvironment>\n'
            f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n'
            f'  <ActionSpace>{self.action_space}</ActionSpace>\n'
            f'  <Description>{self.description}</Description>\n'
            f'  <SimulatorConfiguration>{self.simulator_configuration}</SimulatorConfiguration>\n'
            f'  <IsConnected>{self.is_connected}</IsConnected>\n'
            f'</NeodroidEnvironment>')


if __name__ == '__main__':
  import argparse
  from tqdm import tqdm

  parser = argparse.ArgumentParser(description='Neodroid Environments')
  parser.add_argument('--ENVIRONMENT_NAME',
                      type=str,
                      default='mab',
                      metavar='ENVIRONMENT_NAME',
                      help='name of the environment to run',
                      )
  parser.add_argument('--CONNECT_TO_RUNNING',
                      '-C',
                      action='store_true',
                      default=True,
                      help='Connect to already running environment instead of starting another instance')
  arguments = parser.parse_args()

  env = NeodroidEnvironment(name=arguments.ENVIRONMENT_NAME, connect_to_running=arguments.CONNECT_TO_RUNNING)

  observation_session = tqdm(env, leave=False)
  i = 0
  for environment_state in observation_session:
    first_environment_state = list(environment_state.values())[0]
    i += 1
    if first_environment_state.terminated:
      print(f'Interrupted, local frame number: {i}, remote:{first_environment_state.frame_number}')
      env.reset()
      i = 0
