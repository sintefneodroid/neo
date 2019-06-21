#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.api.environment import Environment

from neodroid.factories import construct_action_space, construct_observation_space

__author__ = 'cnheider'

from abc import ABC
import neodroid.interfaces.environment_models as M


class PythonEnvironment(Environment, ABC):

  def __init__(self,
               *,
               ip='localhost',
               port=6969,
               connect_to_running=False,
               on_connected_callback=None,
               on_disconnected_callback=None,
               on_timeout_callback=None,
               **kwargs):
    super().__init__(**kwargs)

    # Networking
    self._ip = ip
    self._port = port
    self._connect_to_running = connect_to_running
    self._external_on_connected_callback = on_connected_callback
    self._external_on_disconnected_callback = on_disconnected_callback
    self._external_on_timeout_callback = on_timeout_callback

  def __next__(self):
    return self.react()

  def describe(self):
    return self.react(parameters=M.ReactionParameters(
        terminable=False, describe=True, episode_count=False
        ))

  def update_interface_statics(self, new_states, new_simulator_configuration):
    self._last_message = new_states

    self._simulator_configuration = new_simulator_configuration
    first_environment = list(self._last_message.values())[0]
    observables = first_environment.observables
    if observables is not None:
      self._observation_space = construct_observation_space(observables)
    if first_environment.description:
      self._description = first_environment.description
      self._action_space = construct_action_space(self._description)

  def __repr__(self):
    return (f'<PythonEnvironment>\n'
            f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n'
            f'  <ActionSpace>{self.action_space}</ActionSpace>\n'
            f'  <Description>{self.description}</Description>\n'
            f'</PythonEnvironment>')
