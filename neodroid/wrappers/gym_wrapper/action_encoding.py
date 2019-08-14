#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from neodroid.wrappers import NeodroidVectorGymEnvironment
from neodroid.utilities.transformations.encodings import signed_ternary_encoding

__author__ = 'cnheider'


class DiscreteActionEncodingWrapper(NeodroidVectorGymEnvironment):

  def step(self, action: int = 0, **kwargs) -> Any:
    ternary_action = signed_ternary_encoding(size=self.action_space.num_discrete_actions // 3,
                                             index=action)
    return super().step(ternary_action, **kwargs)
