#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from typing import Any

import numpy as np

from neodroid.neodroid_utilities.encodings import signed_ternary_encoding
from neodroid.wrappers.gym_wrapper import NeodroidGymWrapper
from warg import NOD

__author__ = 'cnheider'

from neodroid.wrappers.curriculum_wrapper import NeodroidCurriculumWrapper


class BinaryActionEncodingWrapper(NeodroidGymWrapper):

  def step(self, action: int = 0, **kwargs) -> Any:
    ternary_action = signed_ternary_encoding(size=self.action_space.num_motors,
                                             index=action)
    return super().step(ternary_action, **kwargs)

  @property
  def action_space(self):
    self.act_spc = super().action_space

    # self.act_spc.sample = self.signed_one_hot_sample

    return self.act_spc

  def signed_one_hot_sample(self):
    num = self.act_spc.num_binary_actions
    return random.randrange(num)


class BinaryActionEncodingCurriculumEnvironment(NeodroidCurriculumWrapper):

  def step(self, action: int = 0, **kwargs) -> Any:
    a = signed_ternary_encoding(size=self.action_space.num_motors,
                                index=action)
    return super().act(input_reaction=a, **kwargs)

  @property
  def action_space(self):
    self.act_spc = super().action_space

    # self.act_spc.sample = self.signed_one_hot_sample

    return self.act_spc

  def signed_one_hot_sample(self):
    num = self.act_spc.num_binary_actions
    return random.randrange(num)


class NeodroidWrapper():
  def __init__(self, env):
    self.env = env

  def react(self, a,*args, **kwargs):
    if isinstance(a,np.ndarray):
      if len(a.shape)>1:
        a = list(*a)
      else:
        pass
        a = a[0]

    observables, signal, terminated, *_ = self.env.step(a, *args, **kwargs)

    return NOD.dict_of(observables, signal, terminated)

  def reset(self):
    return self.env.reset()

  def __getattr__(self, item):
    return getattr(self.env, item)
