#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict

from neodroid.messaging.fbs.FBSModels import FEnvironmentDescription
from neodroid.messaging.fbs.fbs_state_utilties import (
    deserialise_actors,
    deserialise_configurables,
    deserialise_sensors,
)
from neodroid.utilities.spaces import ActionSpace, ObservationSpace, Range, SignalSpace
from neodroid.utilities.unity_specifications.configurable import Configurable
from neodroid.utilities.unity_specifications.sensor import Sensor

__author__ = "Christian Heider Nielsen"

from warg import cached_property


class EnvironmentDescription(object):
    """

    """

    def __init__(self, fbs_description: FEnvironmentDescription):
        self._fbs_description = fbs_description

    @cached_property
    def objective_name(self) -> str:
        """

        @return:
        @rtype:
        """
        return self._fbs_description.Objective().ObjectiveName()

    @cached_property
    def max_episode_length(self) -> int:
        """

        @return:
        @rtype:
        """
        return self._fbs_description.Objective().MaxEpisodeLength()

    @cached_property
    def actors(self):
        """

        @return:
        @rtype:
        """
        return deserialise_actors(self._fbs_description)

    def actor(self, key):
        """

        @param key:
        @type key:
        @return:
        @rtype:
        """
        actors = self.actors
        if key in actors:
            return actors[key]

    @cached_property
    def actuators(self):
        """

        @return:
        @rtype:
        """
        actuators_out = []
        for a in deserialise_actors(self._fbs_description).values():
            actuators_out.append(a.actuators)
        return actuators_out

    def actuator(self, key):
        """

        @param key:
        @type key:
        @return:
        @rtype:
        """
        actuators = self.actuators
        if key in actuators:
            return actuators[key]

    @cached_property
    def sensors(self):
        """

        @return:
        @rtype:
        """
        return deserialise_sensors(self._fbs_description)

    def sensor(self, key) -> Sensor:
        """

        @param key:
        @type key:
        @return:
        @rtype:
        """
        if key in self.sensors:
            return self.sensors[key]

    @cached_property
    def configurables(self) -> Dict[str, Configurable]:
        """

        @return:
        @rtype:
        """
        return deserialise_configurables(self._fbs_description)

    def configurable(self, key: str) -> Configurable:
        """

        @param key:
        @type key:
        @return:
        @rtype:
        """
        configurables = self.configurables
        if key in configurables:
            return configurables[key]

    def __repr__(self) -> str:
        actors_str = "".join([str(actor.__repr__()) for actor in self.actors.values()])

        configurables_str = "".join(
            [
                str(configurable.__repr__())
                for configurable in self.configurables.values()
            ]
        )

        # '  <objective_name>' +  self.objective_name + '</objective_name>\n' \

        return (
            f"<EnvironmentDescription>\n"
            f"<MaxEpisodeLength>{self.max_episode_length}</MaxEpisodeLength>\n"
            f"<Sensors>\n{self.sensors}</Sensors>\n"
            f"<Actors>\n{actors_str}</Actors>\n"
            f"<Configurables>\n{configurables_str}</Configurables>\n"
            f"</EnvironmentDescription>\n"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __unicode__(self) -> str:
        return self.__repr__()

    @cached_property
    def observation_space(self) -> ObservationSpace:
        """

        @return:
        @rtype:
        """
        sensor_names = self.sensors.keys()
        observation_spaces = []
        observers = self.sensors.values()
        for observer in observers:
            observation_spaces.extend(observer.space)

        return ObservationSpace(observation_spaces, sensor_names)

    @cached_property
    def action_space(self) -> ActionSpace:
        """

        @return:
        @rtype:
        """
        motion_names = self.actors.keys()
        motion_spaces = []
        for actor in self.actors.values():
            for actuator in actor.actuators.values():
                motion_spaces.append(actuator.motion_space)

        return ActionSpace(motion_spaces, motion_names)

    @cached_property
    def signal_space(environment_description) -> SignalSpace:
        """

        @return:
        @rtype:
        """
        return SignalSpace((Range(min_value=-1, max_value=1, decimal_granularity=3),))


if __name__ == "__main__":
    ed = EnvironmentDescription(None)
    print(ed.signal_space)
