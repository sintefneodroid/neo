#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Iterable, Sized, Sequence

import numpy
from gym import Env

from neodroid.utilities.snapshot_extraction.vector_environment_snapshot import (
    VectorEnvironmentSnapshot,
)
from neodroid.utilities.spaces import ActionSpace, ObservationSpace, Range, SignalSpace
from neodroid.utilities.unity_specifications import EnvironmentSnapshot

__author__ = "Christian Heider Nielsen"

import gym

from trolls import SubProcessEnvironments, make_gym_env
from warg import drop_unused_kws

__all__ = ["NeodroidVectorGymEnvironment"]


class NeodroidVectorGymEnvironment(object):
    @drop_unused_kws
    def __init__(
        self, environment_name, *, num_envs: int = 6, auto_reset_on_terminal_state=False
    ):

        self._env = SubProcessEnvironments(
            [make_gym_env(environment_name) for _ in range(num_envs)],
            auto_reset_on_terminal_state=auto_reset_on_terminal_state,
        )
        self._environment_name = environment_name

    @property
    def signal_space(self) -> SignalSpace:
        """

:return:
"""

        space = SignalSpace(
            [
                Range(
                    min_value=-float("inf"),
                    max_value=float("inf"),
                    decimal_granularity=9,
                )
            ]
        )

        return space

    @property
    def observation_space(self) -> ObservationSpace:
        """

:return:
"""

        if len(self._env.observation_space.shape) >= 1:
            aspc = self._env.observation_space
            space = ObservationSpace(
                [
                    Range(decimal_granularity=6, min_value=mn, max_value=mx)
                    for _, mn, mx in zip(
                        range(self._env.observation_space.shape[0]), aspc.low, aspc.high
                    )
                ]
            )
        else:
            space = ObservationSpace(
                [
                    Range(
                        min_value=0,
                        max_value=self._env.observation_space.n,
                        decimal_granularity=0,
                    )
                ]
            )

        return space

    @property
    def action_space(self) -> ActionSpace:
        """

:return:
"""

        if len(self._env.action_space.shape) >= 1:
            aspc = self._env.action_space
            space = ActionSpace(
                [
                    Range(decimal_granularity=2, min_value=mn, max_value=mx)
                    for _, mn, mx in zip(
                        range(self._env.action_space.shape[0]), aspc.low, aspc.high
                    )
                ]
            )

        else:
            space = ActionSpace(
                [
                    Range(
                        min_value=0,
                        max_value=self._env.action_space.n - 1,
                        decimal_granularity=0,
                    )
                ]
            )

        return space

    @property
    def environment_name(self):
        return self._environment_name

    @drop_unused_kws
    def react(self, a: Sequence) -> VectorEnvironmentSnapshot:
        res = self._env.step(a)

        e = {
            f"{self.environment_name}{i}": EnvironmentSnapshot.from_gym(
                self.environment_name, *o
            )
            for i, o in enumerate(res)
        }
        return VectorEnvironmentSnapshot(e)

    def reset(self) -> VectorEnvironmentSnapshot:
        res = self._env.reset()
        e = {
            f"{self.environment_name}{i}": EnvironmentSnapshot.from_gym(
                self.environment_name, o, 0, False, None
            )
            for i, o in enumerate(res)
        }
        return VectorEnvironmentSnapshot(e)

    def __getattr__(self, item):
        return getattr(self._env, item)

    def __next__(self):
        return self.react(self.action_space.sample())

    @property
    def metadata(self) -> dict:
        return {"render.modes": ["rgb_array"]}

    @property
    def reward_range(self) -> tuple:
        return -float("inf"), float("inf")

    @property
    def spec(self):
        return None


if __name__ == "__main__":
    env = NeodroidVectorGymEnvironment("CartPole-v1")
    print(env.observation_space)
    print(env.action_space)
    print(env.signal_space)
    print(env.reset())
    print(env.react([1]))
    print(env.react(env.action_space.sample()))
