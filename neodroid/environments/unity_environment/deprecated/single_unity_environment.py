#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.environments.unity_environment import UnityEnvironment
from neodroid.exceptions.exceptions import NoEnvironmentError
from neodroid.factories.single.single_reaction_factory import (
    verify_configuration_reaction,
    verify_motion_reaction,
)
from neodroid.utilities.spaces import ActionSpace, ObservationSpace, SignalSpace
from neodroid.utilities.unity_specifications import (
    EnvironmentDescription,
    EnvironmentSnapshot,
    Reaction,
    Sensor,
)

__author__ = "Christian Heider Nielsen"
__all__ = ["SingleUnityEnvironment"]


class SingleUnityEnvironment(UnityEnvironment):
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
    def action_space(self) -> ActionSpace:
        while not self._action_space:
            self.describe()
        return next(iter(self._action_space.values()))

    @property
    def signal_space(self) -> SignalSpace:
        while not self._signal_space:
            self.describe()
        return next(iter(self._signal_space.values()))

    def __next__(self):
        if not self._is_connected_to_server:
            return
        return self.react()

    def react(
        self, input_reaction=None, *, parameters=None, normalise=False, **kwargs
    ) -> EnvironmentSnapshot:
        if not isinstance(input_reaction, Reaction):
            input_reaction = verify_motion_reaction(
                reaction_input=input_reaction,
                normalise=normalise,
                environment_description=self.description,
                action_space=self.action_space,
            )
        if parameters is not None:
            input_reaction.parameters = parameters

        input_reactions = [input_reaction]

        env_states = super().react(input_reactions=input_reactions, **kwargs)

        first_environment = list(env_states.values())[0]
        if first_environment:
            return first_environment
        raise NoEnvironmentError()

    def reset(
        self, input_reaction=None, state=None, on_reset_callback=None
    ) -> EnvironmentSnapshot:

        input_reaction = verify_configuration_reaction(
            input_reaction=input_reaction, environment_description=self.description
        )
        if state:
            input_reaction.unobservables = state.unobservables

        input_reactions = [input_reaction]
        new_states = super().reset(input_reactions)

        new_state = list(new_states.values())[0]
        return new_state

    def configure(self, *args, **kwargs) -> EnvironmentSnapshot:
        return self.reset(*args, **kwargs)

    def describe(self, *args, **kwargs) -> EnvironmentSnapshot:
        new_states = super().describe(*args, **kwargs)
        message = list(new_states.values())[0]
        return message

    def sensor(self, name, *args, **kwargs) -> Sensor:
        state_env_0 = list(self._last_snapshots.values())[0]
        sens = state_env_0.sensor(name)
        if not sens:
            warn("Sensor was not found!")
        return sens


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

    env = SingleUnityEnvironment(
        environment_name=proc_args.ENVIRONMENT_NAME,
        connect_to_running=proc_args.CONNECT_TO_RUNNING,
    )

    observation_session = tqdm(env, leave=False)
    for environment_state in observation_session:
        if environment_state.terminated:
            print(f"Interrupted {environment_state.signal}")
            env.reset()
