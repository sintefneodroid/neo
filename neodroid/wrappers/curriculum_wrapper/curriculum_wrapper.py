#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Any

from neodroid.models import Reaction, ReactionParameters
from neodroid.utilities.encodings import signed_ternary_encoding

__author__ = 'cnheider'

import numpy as np

from neodroid.utilities import flattened_observation
from neodroid.wrappers.experimental.single_environment_wrapper import SingleEnvironmentWrapper


class NeodroidCurriculumWrapper(SingleEnvironmentWrapper):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def __next__(self):
    if not self._is_connected_to_server:
      raise StopIteration
    return self.act()

  def act(self, action=None, *args, **kwargs):
    message = super().react(action[0], *args, **kwargs)
    if message:
      return (np.array([flattened_observation(message)]),
              np.array([message.signal]),
              np.array([message.terminated]),
              message,
              )
    return None, None, None, None

  def configure(self, *args, **kwargs):
    message = super().reset(*args, **kwargs)
    if message:
      return np.array([flattened_observation(message)]), message
    return None, None

  def generate_trajectory_from_configuration(self,
                                             initial_configuration,
                                             motion_horizon=6,
                                             non_terminable_horizon=10,
                                             random_process=None
                                             ):
    configure_params = ReactionParameters(reset=True,
                                          terminable=False,
                                          configure=True
                                          # ,episode_count=False
                                          )

    conf_reaction = Reaction(parameters=configure_params,
                             configurations=initial_configuration)

    non_terminable_params = ReactionParameters(step=True,
                                               terminable=False
                                               #                                              ,
                                               #                                              episode_count=False
                                               )

    initial_states = set()
    self.configure()
    while len(initial_states) < 1:
      state, _ = self.configure(conf_reaction)
      for i in range(non_terminable_horizon):
        state, _, terminated, info = self.act(self.action_space.sample(),
                                              parameters=non_terminable_params)

      for i in range(motion_horizon):
        if random_process is not None:
          actions = random_process.sample()
          actions = self.action_space.validate(actions)
        else:
          actions = self.action_space.sample()

        state, _, terminated, info = self.act(actions)

        if not terminated:
          initial_states.add(info)
      non_terminable_horizon += 1

    return initial_states

  def generate_trajectory_from_state(self,
                                     state,
                                     motion_horizon=10,
                                     random_process=None):
    initial_states = set()
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
          initial_states.add(info)
      motion_horizon += 1

    return initial_states

  def observe(self, *args, **kwargs):
    message = super().observe()
    if message:
      return (flattened_observation(message),
              message.signal,
              message.terminated,
              message,
              )
    return None, None, None, None

  def quit(self, *args, **kwargs):
    return self.close(*args, **kwargs)


class BinaryActionEncodingCurriculumEnvironment(NeodroidCurriculumWrapper):

  def step(self, action: int = 0, **kwargs) -> Any:
    a = signed_ternary_encoding(size=self.action_space.n,
                                index=action)
    return super().act(a, **kwargs)

  @property
  def action_space(self):
    self.act_spc = super().action_space

    # self.act_spc.sample = self.signed_one_hot_sample

    return self.act_spc

  def signed_one_hot_sample(self):
    num = self.act_spc.n
    return random.randrange(num)
