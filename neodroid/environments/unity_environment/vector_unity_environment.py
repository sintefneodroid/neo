#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from itertools import count
from typing import Union

from neodroid.environments.unity_environment import UnityEnvironment
from neodroid.factories.configuration_reactions import verify_configuration_reactions
from neodroid.factories.motion_reactions import verify_motion_reactions
from neodroid.utilities.snapshot_extraction.vector_environment_snapshot import (
    VectorEnvironmentSnapshot,
)
from neodroid.utilities.spaces import (
    ObservationSpace,
    SignalSpace,
    ActionSpace,
    VectorActionSpace,
)

from neodroid.utilities.unity_specifications import (
    EnvironmentDescription,
    Reaction,
    ReactionParameters,
)

__author__ = "Christian Heider Nielsen"
__all__ = ["VectorUnityEnvironment"]

from warg import drop_unused_kws


class VectorUnityEnvironment(UnityEnvironment):
    def __next__(self) -> Union[VectorEnvironmentSnapshot, None]:
        if not self._is_connected_to_server:
            return None
        return self.react()

    @drop_unused_kws
    def react(
        self, input_reactions=None, *, parameters: ReactionParameters = None
    ) -> VectorEnvironmentSnapshot:

        if not isinstance(input_reactions, Reaction):
            input_reactions = verify_motion_reactions(
                input_reactions=input_reactions,
                environment_descriptions=self._description,
                environment_snapshots=self._last_snapshots,
                _auto_reset=self._auto_reset,
            )
        if parameters is not None:
            input_reactions.parameters = parameters

        return VectorEnvironmentSnapshot(self.send(input_reactions=input_reactions))

    def reset(
        self, input_reactions=None, state=None, on_reset_callback: callable = None
    ) -> VectorEnvironmentSnapshot:

        input_reactions = verify_configuration_reactions(
            input_reactions=input_reactions, environment_descriptions=self._description
        )

        return VectorEnvironmentSnapshot(super().reset(input_reactions=input_reactions))

    def configure(self, *args, **kwargs) -> VectorEnvironmentSnapshot:
        return self.reset(*args, **kwargs)

    def describe(self) -> VectorEnvironmentSnapshot:
        return VectorEnvironmentSnapshot(super().describe())

    @property
    def action_space(self) -> VectorActionSpace:
        while not self._action_space:
            self.describe()
        return VectorActionSpace(
            next(iter(self._action_space.values())), len(self._action_space.values())
        )

    @property
    def description(self) -> EnvironmentDescription:
        while not self._description:
            self.describe()
        return next(iter(self._description.values()))

    @property
    def observation_space(self) -> ObservationSpace:
        while not self._observation_space:
            self.describe()
        return next(iter(self._observation_space.values()))

    @property
    def signal_space(self) -> SignalSpace:
        while not self._signal_space:
            self.describe()
        return next(iter(self._signal_space.values()))


if __name__ == "__main__":
    import argparse
    from tqdm import tqdm

    parser = argparse.ArgumentParser(description="Single environment wrapper")
    parser.add_argument(
        "--ENVIRONMENT_NAME",
        type=str,
        default="grd",
        metavar="ENVIRONMENT_NAME",
        help="name of the environment to run",
    )
    parser.add_argument(
        "--CONNECT_TO_RUNNING",
        "-C",
        action="store_true",
        default=True,
        help="Connect to already running environment instead of starting another instance",
    )
    proc_args = parser.parse_args()

    env = VectorUnityEnvironment(
        environment_name=proc_args.ENVIRONMENT_NAME,
        connect_to_running=proc_args.CONNECT_TO_RUNNING,
        auto_reset_on_terminal_state=True,
    )

    # observation_session = tqdm(env, leave=False)
    # for environment_state in observation_session:
    # if environment_state.terminated.all():
    #  print(f"Interrupted {environment_state.signal}")
    #  env.reset()

    for _ in count():
        print(env.react(env.action_space.sample()).terminated)
