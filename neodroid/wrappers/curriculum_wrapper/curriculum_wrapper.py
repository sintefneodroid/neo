#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import numpy as np

from neodroid import NeodroidEnvironment
from neodroid.models import Reaction, ReactionParameters
from neodroid.utilities.statics import flattened_observation


class NeodroidCurriculumWrapper(NeodroidEnvironment):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def __next__(self):
    if not self._connected_to_server:
      raise StopIteration
    return self.act()

  def act(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).react(*args, **kwargs)
    if message:
      return (
        np.array(flattened_observation(message)),
        message.signal,
        message.terminated,
        message,
        )
    return None, None, None, None

  def configure(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).reset(*args, **kwargs)
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
    configure_params = ReactionParameters(
        terminable=False, episode_count=False, reset=True, configure=True
        )
    init = Reaction(
        parameters=configure_params, configurations=initial_configuration
        )

    non_terminable_params = ReactionParameters(
        terminable=False,
        episode_count=False,
        reset=False,
        configure=False,
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
        state, _, terminated, info = self.act(reaction)

      for i in range(motion_horizon):
        if random_process is not None:
          actions = random_process.sample()
          actions = self.action_space.validate(actions)
        else:
          actions = self.action_space.sample()

        state, _, terminated, info = self.act(actions)

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

        s, _, terminated, info = self.act(actions)

        if not terminated:
          initial_states.append(info)
      motion_horizon += 1

    return initial_states

  def observe(self, *args, **kwargs):
    message = super(NeodroidCurriculumWrapper, self).observe()
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
