#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, Union

from draugr.tqdm_utilities import progress_bar

from neodroid import DEFAULT_ENVIRONMENTS_PATH, __version__
from neodroid.factories.motion_reactions import verify_motion_reactions
from neodroid.utilities import launch_environment
from neodroid.utilities.specifications.unity_specifications import Reaction
from neodroid.utilities.specifications.unity_specifications.environment_description import (
    EnvironmentDescription,
)
from neodroid.utilities.specifications.unity_specifications.environment_snapshot import (
    EnvironmentSnapshot,
)
from neodroid.utilities.specifications.unity_specifications.reaction_parameters import (
    ReactionParameters,
)
from neodroid.utilities.specifications.unity_specifications.simulator_configuration import (
    SimulatorConfiguration,
)
from trolls.spaces import ActionSpace, ObservationSpace, SignalSpace

__author__ = "Christian Heider Nielsen"

__all__ = ["DictUnityEnvironment"]

from neodroid.environments.networking_environment import NetworkingEnvironment


class DictUnityEnvironment(NetworkingEnvironment):
    """ """

    def __init__(
        self,
        *,
        environment_name: str = None,
        clones: int = 0,
        path_to_executables_directory: Union[str, Path] = DEFAULT_ENVIRONMENTS_PATH,
        headless: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Environment
        self._simulator_configuration = None
        self._last_snapshots = None
        # Simulation
        self._simulation_instance = None
        self._clones = clones

        self._description = None
        self._action_space = None
        self._observation_space = None
        self._signal_space = None

        if (
            not self._connect_to_running
            and not self._simulation_instance
            and environment_name is not None
        ):
            self._simulation_instance = launch_environment(
                environment_name,
                ip=self._ip,
                port=self._port,
                path_to_executables_directory=path_to_executables_directory,
                headless=headless,
            )
            if self._simulation_instance:
                logging.debug(f"successfully started environment {environment_name}")
            else:

                logging.debug(f"could not start environment {environment_name}")

        self._setup_connection()

    @property
    def description(self) -> Mapping[str, EnvironmentDescription]:
        """

        :return:
        :rtype:
        """
        while not self._description:
            self.describe()
        return self._description

    @property
    def observation_space(self) -> Mapping[str, ObservationSpace]:
        """

        :return:
        :rtype:
        """
        while not self._observation_space:
            self.describe()
        return self._observation_space

    @property
    def action_space(self) -> Mapping[str, ActionSpace]:
        """

        :return:
        :rtype:
        """
        while not self._action_space:
            self.describe()
        return self._action_space

    @property
    def signal_space(self) -> Mapping[str, SignalSpace]:
        """

        :return:
        :rtype:
        """
        while not self._signal_space:
            self.describe()
        return self._signal_space

    @property
    def simulator_configuration(self) -> SimulatorConfiguration:
        """

        :return:
        :rtype:
        """
        while not self._simulator_configuration:
            self.describe()
        return self._simulator_configuration

    @property
    def neodroid_api_version(self):
        """

        :return:
        :rtype:
        """
        return __version__

    def sensor(self, name: str):
        """

        :param name:
        :type name:
        :return:
        :rtype:
        """
        envs = list(self._last_snapshots.values())

        observer = []
        for e in envs:
            o = e.sensor(name)
            if not o:
                logging.warning("Sensor was not found!")
            observer.append(o)
        return observer

    def _setup_connection(self, auto_describe=True):
        super()._setup_connection(auto_describe)
        if auto_describe:
            # TODO: WARN ABOUT WHEN INDIVIDUAL OBSERVATIONS AND UNOBSERVABLES ARE UNAVAILABLE due to simulator
            #  configuration

            logging.warning(f"Using Neodroid API version {self.neodroid_api_version}")

            server_version = self.simulator_configuration.api_version
            logging.info(f"Server API version: {server_version}")

            if self.neodroid_api_version != server_version:
                if server_version == "":
                    server_version = "*Unspecified*"

                logging.warning(
                    f"Server is using different version {server_version}, complications may occur!"
                )

    def configure(self, *args, **kwargs) -> Mapping[str, EnvironmentSnapshot]:
        """

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        return self.reset(*args, **kwargs)

    def react(
        self,
        input_reactions: Optional[Any] = None,
        *,
        parameters: Optional[ReactionParameters] = ReactionParameters(
            episode_count=True, step=True, terminable=True
        ),
        normalise: bool = False,
        on_reaction_sent_callback: Optional[Callable] = None,
        on_step_done_callback: Optional[Callable] = None,
        **kwargs,
    ) -> Mapping[str, EnvironmentSnapshot]:
        """

        :param input_reactions:
        :type input_reactions:
        :param parameters:
        :type parameters:
        :param normalise:
        :type normalise:
        :param on_reaction_sent_callback:
        :type on_reaction_sent_callback:
        :param on_step_done_callback:
        :type on_step_done_callback:
        :return:
        :rtype:"""
        logging.info(f"Reacting in environment: {self.environment_name}")

        if (
            isinstance(input_reactions, list)
            and len(input_reactions) > 0
            and isinstance(input_reactions[0], Reaction)
        ):
            pass
        else:
            if input_reactions is None:
                parameters = ReactionParameters(
                    episode_count=True, step=True, terminable=True
                )
                input_reactions = [
                    Reaction(parameters=parameters, environment_name="all")
                ]
            elif not isinstance(input_reactions, Reaction):
                input_reactions = verify_motion_reactions(
                    input_reactions=input_reactions,
                    environment_descriptions=self.description,
                    environment_snapshots=self._last_snapshots,
                )

        return self.send(input_reactions)

    def send(self, input_reactions: Iterable) -> Dict[str, Any]:
        """

        :param input_reactions:
        :type input_reactions:
        :return:
        :rtype:
        """
        (new_snapshots, simulator_configuration) = self._message_server.send_receive(
            input_reactions
        )

        if new_snapshots:
            self._last_snapshots = new_snapshots
        else:
            logging.warning("No valid was new_state received")

        if simulator_configuration and new_snapshots:
            self.update_interface_attributes(new_snapshots, simulator_configuration)
        else:
            pass
            # logging.warning("No valid was simulator_configuration received")

        return new_snapshots

    def display(self, displayables: Sequence) -> Mapping[str, EnvironmentSnapshot]:
        """

        :param displayables:
        :type displayables:
        :return:
        :rtype:
        """
        conf_reaction = Reaction(displayables=displayables)
        message = self.reset(conf_reaction)
        if message:
            return message

    def reset(
        self,
        input_reactions: Optional[Any] = None,
        state: Optional[EnvironmentSnapshot] = None,
        on_reset_callback: Optional[Callable] = None,
    ) -> Mapping[str, EnvironmentSnapshot]:
        """

        :param input_reactions:
        :type input_reactions:
        :param state: Reset to a certain state #TODO NOT IMPLEMENTED
        :type state:
        :param on_reset_callback:
        :type on_reset_callback:
        :return:
        :rtype:
        """
        logging.info("Resetting environment")

        if input_reactions is None:
            parameters = ReactionParameters(
                terminable=True, describe=True, episode_count=False, reset=True
            )
            input_reactions = [Reaction(parameters=parameters, environment_name="all")]

        return self.send(input_reactions)

    def _close(self, callback: Optional[Callable] = None):
        """

        :param callback:
        :type callback:
        :return:
        :rtype:"""
        logging.info("Closing")
        # if self._message_server:
        #  self._message_server.__del__()
        if self._simulation_instance is not None:
            self._simulation_instance.terminate()
        if callback:
            callback()
        return 0

    def describe(self) -> Mapping[str, EnvironmentSnapshot]:
        """

        :return:
        :rtype:"""
        reaction = Reaction(
            parameters=ReactionParameters(
                terminable=False, describe=True, episode_count=False
            )
        )

        return self.send([reaction])

    def update_interface_attributes(
        self,
        new_states: Dict[str, EnvironmentSnapshot],
        new_simulator_configuration: SimulatorConfiguration,
        ensure_no_space_changes: bool = False,
    ) -> None:
        """

        :param ensure_no_space_changes:
        :type ensure_no_space_changes:
        :param new_states:
        :type new_states:
        :param new_simulator_configuration:
        :type new_simulator_configuration:
        """
        if not self._description:
            self._description = {}
        if not self._action_space:
            self._action_space = {}
        if not self._observation_space:
            self._observation_space = {}
        if not self._signal_space:
            self._signal_space = {}

        self._simulator_configuration = new_simulator_configuration
        envs = new_states.items()

        for key, env in envs:
            if env.description:
                self._description[key] = env.description

                if key in self._action_space and ensure_no_space_changes:
                    assert (
                        self._action_space[key] == env.description.action_space
                    ), f"Action space changed! {self._action_space[key], env.description.action_space}"
                else:
                    self._action_space[key] = env.description.action_space

                if key in self._observation_space and ensure_no_space_changes:
                    assert (
                        self._observation_space[key]
                        == env.description.observation_space
                    ), f"Observation space changed! {self._observation_space[key], env.description.observation_space}"
                else:
                    self._observation_space[key] = env.description.observation_space

                if key in self._signal_space and ensure_no_space_changes:
                    assert (
                        self._signal_space[key] == env.description.signal_space
                    ), f"Signal space changed! {self._signal_space[key], env.description.signal_space}"
                else:
                    self._signal_space[key] = env.description.signal_space

    def __on_reconnected_callback__(self):
        super().__on_reconnected_callback__()
        if False:
            new_states = self.describe()

    def __repr__(self):
        return (
            f"<NeodroidEnvironment>\n"
            f"  <ObservationSpace>{self.observation_space}</ObservationSpace>\n"
            f"  <ActionSpace>{self.action_space}</ActionSpace>\n"
            f"  <Description>{self.description}</Description>\n"
            f"  <SimulatorConfiguration>{self.simulator_configuration}</SimulatorConfiguration>\n"
            f"  <IsConnected>{self.is_connected}</IsConnected>\n"
            f"</NeodroidEnvironment>"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Neodroid Environments")
    parser.add_argument(
        "--ENVIRONMENT_NAME",
        type=str,
        default="mab",
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
    arguments = parser.parse_args()

    env = DictUnityEnvironment(
        name=arguments.ENVIRONMENT_NAME, connect_to_running=arguments.CONNECT_TO_RUNNING
    )

    observation_session = progress_bar(env)
    i = 0
    for environment_state in observation_session:
        first_environment_state = list(environment_state.values())[0]
        i += 1
        if first_environment_state.terminated:
            print(
                f"Interrupted, local frame number: {i}, remote:{first_environment_state.frame_number}"
            )
            env.reset()
            i = 0
