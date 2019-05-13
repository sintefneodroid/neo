#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import draugr

__author__ = 'cnheider'

import os
import warnings

import numpy as np

import neodroid.models as M
from neodroid.models import Reaction
from neodroid.utilities import (construct_step_reaction, flattened_observation, launch_environment,
                                         verify_configuration_reaction,
                                         )
from neodroid.networking_environment import NetworkingEnvironment

file_dir = os.path.dirname(os.path.realpath(__file__))
default_environments_dir = os.path.abspath(os.path.join(file_dir, 'environments'))


class NeodroidEnvironment(NetworkingEnvironment):

  @property
  def description(self):
    return self._description

  @property
  def observation_space(self):
    return self._observation_space

  @property
  def action_space(self):
    return self._action_space

  @property
  def signal_space(self):
    return self._signal_space

  @property
  def simulator_configuration(self):
    return self._simulator_configuration

  @property
  def neodroid_api_version(self):
    return '0.1.6'

  def __init__(self,
               *,
               environment_name=None,
               clones=0,
               path_to_executables_directory=default_environments_dir,
               headless=False,
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
        if self._debug_logging:
          self._logger.debug(f'successfully started environment {environment_name}')
      else:
        if self._debug_logging:
          self._logger.debug(f'could not start environment {environment_name}')

    self._setup_connection()

    if self._verbose:
      warnings.warn(f'Using Neodroid API version {self.neodroid_api_version}')

    server_version = self._simulator_configuration.api_version
    if self.neodroid_api_version != server_version:
      if server_version == '':
        server_version = '*Unspecified*'
      if self._verbose:
        warnings.warn(f'Server is using different version {server_version}, complications may occur!')

    print(f'Server API version: {server_version}')

    if self._verbose:
      draugr.sprint(f'\nconfigurable space:\n{self.description.configurables}\n',
                    color='blue',
                    bold=True,
                    highlight=True)

  def _configure(self, *args, **kwargs):
    return self._reset()

  def _react(
      self,
      input_reactions=None,
      *,
      parameters=None,
      normalise=False,
      on_reaction_sent_callback=None,
      on_step_done_callback=None,
      **kwargs):
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
    self._warn_react()

    if isinstance(input_reactions, list) and len(input_reactions) > 0 and isinstance(input_reactions[0],
                                                                                     M.Reaction):
      pass
    else:
      if input_reactions is None:
        parameters = M.ReactionParameters(
            episode_count=True, step=True, terminable=True
            )
        input_reactions = [M.Reaction(parameters=parameters)]
      elif not isinstance(input_reactions, Reaction):
        input_reaction = self.maybe_infer_motion_reaction(input_reactions=input_reactions,
                                                          normalise=normalise,
                                                          description=self._description,
                                                          verbose=self._verbose)
        input_reactions = [input_reaction]

    new_states, simulator_configuration = self._message_server.send_reactions(input_reactions)

    if new_states:
      self.update_interface_statics(new_states, simulator_configuration)
      return new_states

    self._warn_no_state_received()

  def _display(self, displayables):
    conf_reaction = Reaction(
        displayables=displayables
        )
    message = self.reset(conf_reaction)
    if message:
      return np.array(flattened_observation(message)), message

  @staticmethod
  def maybe_infer_configuration_reaction(input_reaction, description, verbose=False):
    if description:
      input_reaction = verify_configuration_reaction(input_reaction=input_reaction,
                                                     environment_description=description,
                                                     verbose=verbose)
    else:
      input_reaction = verify_configuration_reaction(input_reaction=input_reaction, verbose=verbose)

    return input_reaction

  def _reset(self, input_reactions=None, state=None, on_reset_callback=None):
    self._warn_reset()

    if input_reactions is None:
      parameters = M.ReactionParameters(terminable=True,
                                        describe=True,
                                        episode_count=False,
                                        reset=True)
      input_reactions = [M.Reaction(parameters=parameters)]

    new_states, simulator_configuration = self._message_server.send_reactions(input_reactions)
    if new_states:
      self.update_interface_statics(new_states, simulator_configuration)
      return new_states
    self._warn_no_state_received()

  def _close(self, callback=None):
    '''

:param callback:
:type callback:
:return:
:rtype:
'''
    self._warn_closing()
    # if self._message_server:
    #  self._message_server.__del__()
    if self._simulation_instance is not None:
      self._simulation_instance.terminate()
    if callback:
      callback()
    return 0

  @staticmethod
  def maybe_infer_motion_reaction(*,
                                  input_reactions,
                                  normalise,
                                  description,
                                  verbose=False):
    '''

:param verbose:
:type verbose:
:param input_reactions:
:type input_reactions:
:param normalise:
:type normalise:
:param description:
:type description:
:return:
:rtype:
'''
    if description:
      out_reaction = construct_step_reaction(input_reactions,
                                             description,
                                             normalise,
                                             verbose=verbose)
    else:
      out_reaction = construct_step_reaction(input_reactions,
                                             None,
                                             False,
                                             verbose=verbose)

    if verbose:
      print(out_reaction)

    return out_reaction

  def _warn_closing(self):
    if self._verbose:
      warnings.warn('Closing')
    if self._debug_logging:
      self._logger.debug('Closing')

  def _warn_react(self):
    if self._verbose:
      warnings.warn('Reacting in environment')
    if self._debug_logging:
      self._logger.debug('Reacting in environment')

  def _warn_reset(self):
    if self._verbose:
      warnings.warn('Resetting environment')
    if self._debug_logging:
      self._logger.debug('Resetting environment')

  def _warn_no_state_received(self):
    if self._verbose:
      warnings.warn('No valid was new_state received')
    if self._debug_logging:
      self._logger.debug('No valid was new_state received')

  def __str__(self):
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
  parser.add_argument(
      '--ENVIRONMENT_NAME',
      type=str,
      default='mab',
      metavar='ENVIRONMENT_NAME',
      help='name of the environment to run',
      )
  parser.add_argument(
      '--CONNECT_TO_RUNNING',
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
