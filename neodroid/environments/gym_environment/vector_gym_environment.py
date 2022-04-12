#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import cpu_count
from typing import Sequence

from neodroid.environments.environment import Environment
from neodroid.utilities import EnvironmentDescription
from neodroid.utilities.snapshot_extraction.vector_environment_snapshot import (
    VectorEnvironmentSnapshot,
)
from neodroid.utilities.specifications.unity_specifications import EnvironmentSnapshot
from trolls.spaces import (
    ActionSpace,
    ObservationSpace,
    Range,
    SignalSpace,
    VectorActionSpace,
    VectorObservationSpace,
    VectorSignalSpace,
)

__author__ = "Christian Heider Nielsen"

from trolls.multiple_environments_wrapper import SubProcessEnvironments, make_gym_env
from warg import drop_unused_kws, passes_kws_to

__all__ = ["NeodroidVectorGymEnvironment"]


class NeodroidVectorGymEnvironment(Environment):
    """ """

    def configure(self, *args, **kwargs) -> EnvironmentSnapshot:
        pass

    def display(self, *args, **kwargs) -> EnvironmentSnapshot:
        pass

    def describe(self, *args, **kwargs) -> EnvironmentSnapshot:
        pass

    @property
    def description(self) -> EnvironmentDescription:
        pass

    @drop_unused_kws
    def __init__(
        self,
        environment_name,
        *,
        num_env: int = cpu_count(),
        auto_reset_on_terminal_state=False,
    ):

        self._env = SubProcessEnvironments(
            [make_gym_env(environment_name) for _ in range(num_env)],
            auto_reset_on_terminal_state=auto_reset_on_terminal_state,
        )
        self._num_env = num_env
        self._environment_name = environment_name

    @property
    def signal_space(self) -> VectorSignalSpace:
        """

        :return:"""

        space = SignalSpace(
            [
                Range(
                    min_value=-float("inf"),
                    max_value=float("inf"),
                    decimal_granularity=9,
                )
            ]
        )

        return VectorSignalSpace(space, self._num_env)

    @property
    def observation_space(self) -> VectorObservationSpace:
        """

        :return:"""

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

        return VectorObservationSpace(space, self._num_env)

    @property
    def action_space(self) -> VectorActionSpace:
        """

        :return:"""

        if len(self._env.action_space.shape) >= 1:
            aspc = self._env.action_space
            space = ActionSpace(
                [
                    Range(
                        decimal_granularity=aspc.action_space.is_singular_discrete,
                        min_value=mn,
                        max_value=mx,
                    )
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

        return VectorActionSpace(space, self._num_env)

    @property
    def environment_name(self):
        """

        :return:
        :rtype:
        """
        return self._environment_name

    @drop_unused_kws
    def react(self, a: Sequence) -> VectorEnvironmentSnapshot:
        """

        :param a:
        :type a:
        :return:
        :rtype:
        """
        a = self.action_space.reproject(a)
        # if self.action_space.is_discrete:
        #    a = numpy.squeeze(a, -1)
        res = self._env.step(a)

        if res:
            e = {
                f"{self.environment_name}{i}": EnvironmentSnapshot.from_gym(
                    self.environment_name,
                    self.observation_space.project(o),
                    self.signal_space.project(s),
                    t,
                    info,
                )
                for i, (o, s, t, info) in enumerate(res)
            }
            return VectorEnvironmentSnapshot(e)
        raise ValueError("received None res")

    def reset(self) -> VectorEnvironmentSnapshot:
        """

        :return:
        :rtype:
        """
        res = self._env.reset()
        if res:
            e = {
                f"{self.environment_name}{i}": EnvironmentSnapshot.from_gym(
                    self.environment_name, o, 0, False, None
                )
                for i, o in enumerate(res)
            }
            return VectorEnvironmentSnapshot(e)
        raise ValueError("received None res")

    @passes_kws_to(SubProcessEnvironments.render)
    def render(self, *args, **kwargs):
        return self._env.render(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self._env, item)

    def __next__(self):
        return self.react(self.action_space.sample())


if __name__ == "__main__":

    def asda():
        env = NeodroidVectorGymEnvironment("CartPole-v1")
        print(env.observation_space)
        print(env.action_space)
        print(env.signal_space)
        print(env.reset())
        for i in range(10):
            s = env.react(env.action_space.sample())
            env.render()
            if s.terminated.all():
                env.reset()
        env.close()

    asda()
