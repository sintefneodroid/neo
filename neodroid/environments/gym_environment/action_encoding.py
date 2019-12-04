#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from neodroid.environments.gym_environment import NeodroidVectorGymEnvironment
from neodroid.utilities.transformations.encodings import signed_ternary_encoding

__author__ = "Christian Heider Nielsen"


class DiscreteActionEncodingWrapper(NeodroidVectorGymEnvironment):
    def step(self, action: int = 0, **kwargs) -> Any:
        ternary_action = signed_ternary_encoding(
            size=self.action_space.discrete_steps // 3, index=action
        )
        return super().step(ternary_action, **kwargs)
