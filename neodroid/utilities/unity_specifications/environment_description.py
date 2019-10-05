#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from neodroid.utilities.unity_specifications.sensor import Sensor
from neodroid.utilities.spaces import ObservationSpace, Sequence, ActionSpace
from neodroid.messaging.fbs.FBSModels import FEnvironmentDescription
from neodroid.messaging.fbs.fbs_state_utilties import (deserialise_actors,
                                                       deserialise_sensors,
                                                       deserialise_configurables,
                                                       )

__author__ = 'Christian Heider Nielsen'


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
    return list(deserialise_actors(self._fbs_description).values())[0].actuators

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
  def configurables(self):
    return deserialise_configurables(self._fbs_description)

  def configurable(self, key):
    configurables = self.configurables
    if key in configurables:
      return configurables[key]

  def __repr__(self):
    actors_str = ''.join([str(actor.__repr__()) for actor in self.actors.values()])

    configurables_str = ''.join([str(configurable.__repr__())
                                 for configurable in self.configurables.values()
                                 ]
                                )

    # '  <objective_name>' +  self.objective_name + '</objective_name>\n' \

    return (f'<EnvironmentDescription>\n'
            f'<MaxEpisodeLength>{self.max_episode_length}</MaxEpisodeLength>\n'
            f'<Sensors>\n{self.sensors}</Sensors>\n'
            f'<Actors>\n{actors_str}</Actors>\n'
            f'<Configurables>\n{configurables_str}</Configurables>\n'
            f'</EnvironmentDescription>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()

  @property
  def observation_space(self):
    sensor_names = self.sensors.keys()
    observation_spaces = []
    observers = self.sensors.values()
    for observer in observers:
      if isinstance(observer.space, Sequence):
        for r in observer.space:
          observation_spaces.append(r)
      else:
        observation_spaces.append(observer.space)

    return ObservationSpace(observation_spaces, sensor_names)

  @property
  def action_space(self):
    motion_names = self.actors.keys()
    motion_spaces = []
    for actor in self.actors.values():
      for actuator in actor.actuators.values():
        motion_spaces.append(actuator.motion_space)

    return ActionSpace(motion_spaces, motion_names)

  @property
  def signal_space(environment_description):
    return None
    '''
    sensor_names = environment_description.signal_space
    observation_spaces = []
    observers = environment_description.sensors.values()
    for observer in observers:
      if isinstance(observer.space, Sequence):
        for r in observer.space:
          observation_spaces.append(r)
      else:
        observation_spaces.append(observer.space)

    return SignalSpace(observation_spaces, sensor_names)
    '''
