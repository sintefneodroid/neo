#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict

from neodroid.utilities.unity_specifications.configurable import Configurable
from neodroid.utilities.unity_specifications.sensor import Sensor
from neodroid.utilities.spaces import (
    ObservationSpace,
    Sequence,
    ActionSpace,
    SignalSpace,
    Range,
)
from neodroid.messaging.fbs.FBSModels import FEnvironmentDescription
from neodroid.messaging.fbs.fbs_state_utilties import (
    deserialise_actors,
    deserialise_sensors,
    deserialise_configurables,
)

__author__ = "Christian Heider Nielsen"


class EnvironmentDescription(object):
    def __init__(self, fbs_description: FEnvironmentDescription):
        self._fbs_description = fbs_description

    @property
    def objective_name(self) -> str:
        return self._fbs_description.Objective().ObjectiveName()

    @property
    def max_episode_length(self) -> int:
        return self._fbs_description.Objective().MaxEpisodeLength()

    @property
    def actors(self):
        return deserialise_actors(self._fbs_description)

    def actor(self, key):
        actors = self.actors
        if key in actors:
            return actors[key]

    @property
    def actuators(self):
        actuators_out = []
        for a in deserialise_actors(self._fbs_description).values():
            actuators_out.append(a.actuators)
        return actuators_out

    def actuator(self, key):
        actuators = self.actuators
        if key in actuators:
            return actuators[key]

    @property
    def sensors(self):
        return deserialise_sensors(self._fbs_description)

    def sensor(self, key) -> Sensor:
        if key in self.sensors:
            return self.sensors[key]

    @property
    def configurables(self) -> Dict[str, Configurable]:
        return deserialise_configurables(self._fbs_description)

    def configurable(self, key: str) -> Configurable:
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

    @property
    def observation_space(self) -> ObservationSpace:
        sensor_names = self.sensors.keys()
        observation_spaces = []
        observers = self.sensors.values()
        for observer in observers:
            observation_spaces.extend(observer.space)

        return ObservationSpace(observation_spaces, sensor_names)

    @property
    def action_space(self) -> ActionSpace:
        motion_names = self.actors.keys()
        motion_spaces = []
        for actor in self.actors.values():
            for actuator in actor.actuators.values():
                motion_spaces.append(actuator.motion_space)

        return ActionSpace(motion_spaces, motion_names)

    @property
    def signal_space(environment_description) -> SignalSpace:
        return SignalSpace((Range(min_value=-1, max_value=1, decimal_granularity=3),))


if __name__ == "__main__":
    ed = EnvironmentDescription(None)
    print(ed.signal_space)
