#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'cnheider'

import numpy as np

from neodroid import Reaction, ReactionParameters
from neodroid.neodroid_utilities import flattened_observation
from neodroid.wrappers.single_environment_wrapper import SingleEnvironmentWrapper


class NeodroidCurriculumWrapper(SingleEnvironmentWrapper):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def __next__(self):
    if not self._is_connected_to_server:
      return
    return self.act()

  def act(self, **kwargs):
    message = super().react(**kwargs)
    if message:
      return (
        np.array(flattened_observation(message)),
        message.signal,
        message.terminated,
        message,
        )
    return None, None, None, None

  def configure(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return np.array(flattened_observation(message)), message
    return None, None

  def generate_trajectory_from_configuration(
      self,
      initial_configuration,
      motion_horizon=6,
      non_terminable_horizon=10,
      random_process=None,
      ):
    configure_params = ReactionParameters(reset=True, configure=True
                                          )
    init = Reaction(
        parameters=configure_params, configurations=initial_configuration
        )

    non_terminable_params = ReactionParameters(
        step=True,
        )

    initial_states = []
    self.configure()
    while len(initial_states) < 1:
      state, _ = self.configure(init)
      for i in range(non_terminable_horizon):
        reaction = Reaction(
            motions=self.action_space.sample(), parameters=non_terminable_params
            )
        state, _, terminated, info = self.act(actions=reaction)

      for i in range(motion_horizon):
        if random_process is not None:
          actions = random_process.sample()
          actions = self.action_space.validate(actions)
        else:
          actions = self.action_space.sample()

        state, _, terminated, info = self.act(actions=actions)

        if not terminated:
          initial_states.append(info)
      non_terminable_horizon += 1

    return initial_states

  def generate_trajectory_from_state(
      self, state, motion_horizon=10, random_process=None
      ):
    initial_states = []
    self.configure()
    while len(initial_states) < 1:
      s, _ = self.configure(state=state)
      for i in range(motion_horizon):
        if random_process is not None:
          actions = random_process.sample()
          actions = self.action_space.validate(actions)
        else:
          actions = self.action_space.sample()

        s, _, terminated, info = self.act(actions=actions)

        if not terminated:
          initial_states.append(info)
      motion_horizon += 1

    return initial_states

  def observe(self, *args, **kwargs):
    message = super().observe()
    if message:
      return (
        flattened_observation(message),
        message.signal,
        message.terminated,
        message,
        )
    return None, None, None, None

  def quit(self, *args, **kwargs):
    return self.close(*args, **kwargs)
