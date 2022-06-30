#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Iterable, Union

from gym import Env

from neodroid.utilities.snapshot_extraction.vector_environment_snapshot import (
    VectorEnvironmentSnapshot,
)
from neodroid.utilities.specifications.unity_specifications import EnvironmentSnapshot
from trolls.spaces import ActionSpace, ObservationSpace, Dimension, SignalSpace

__author__ = "Christian Heider Nielsen"

import gym

from warg import drop_unused_kws

__all__ = ["NeodroidGymEnvironment"]


class NeodroidGymEnvironment:
    """ """

    @drop_unused_kws
    def __init__(
        self, environment: Union[str, Env] = "", *, auto_reset_on_terminal_state=True
    ):
        """

        :param environment:"""
        if isinstance(environment, str):
            self._env = gym.make(
                environment
            )  # NormalisedActions(gym.make(environment))
        else:
            self._env = environment

        self._environment_name = environment
        self._auto_reset_on_terminal_state = auto_reset_on_terminal_state

    @property
    def signal_space(self) -> SignalSpace:
        """

        :return:"""

        space = SignalSpace(
            [
                Dimension(
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

        :return:"""

        if len(self._env.observation_space.shape) >= 1:
            aspc = self._env.observation_space
            space = ObservationSpace(
                [
                    Dimension(decimal_granularity=2, min_value=mn, max_value=mx)
                    for _, mn, mx in zip(range(aspc.shape[0]), aspc.low, aspc.high)
                ]
            )
        else:
            space = ObservationSpace(
                [
                    Dimension(
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

        :return:"""

        if len(self._env.action_space.shape) >= 1:
            aspc = self._env.action_space
            space = ActionSpace(
                [
                    Dimension(decimal_granularity=2, min_value=mn, max_value=mx)
                    for _, mn, mx in zip(range(aspc.shape[0]), aspc.low, aspc.high)
                ]
            )

        else:
            space = ActionSpace(
                [
                    Dimension(
                        min_value=0,
                        max_value=self._env.action_space.n - 1,
                        decimal_granularity=0,
                    )
                ]
            )

        return space

    @property
    def environment_name(self):
        """

        :return:
        :rtype:
        """
        return self._environment_name

    @drop_unused_kws
    def react(self, a: Iterable) -> VectorEnvironmentSnapshot:
        """

        :param a:
        :type a:
        :return:
        :rtype:
        """
        a = a[0]
        e = EnvironmentSnapshot.from_gym(self.environment_name, *self._env.step(a))
        return VectorEnvironmentSnapshot({self.environment_name: e})

    def reset(self) -> VectorEnvironmentSnapshot:
        """

        :return:
        :rtype:
        """
        observables = self._env.reset()
        e = EnvironmentSnapshot.from_gym(
            self.environment_name, observables, 0, False, None
        )
        return VectorEnvironmentSnapshot({self.environment_name: e})

    def __getattr__(self, item):
        return getattr(self._env, item)


if __name__ == "__main__":
    env = NeodroidGymEnvironment("CartPole-v1")
    print(env.observation_space)
    print(env.action_space)
    print(env.signal_space)
    print(env.reset())
    print(env.react([1]))
    for _ in range(10):
        env.reset()
        for _ in range(200):
            print(env.react([env.action_space.sample()]))
            env.render()
