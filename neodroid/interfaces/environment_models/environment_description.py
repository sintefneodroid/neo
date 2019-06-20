#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import neodroid.messaging


class EnvironmentDescription(object):

  def __init__(self, fbs_description):
    self._fbs_description = fbs_description

  @property
  def objective_name(self):
    return self._fbs_description.Objective().ObjectiveName()

  @property
  def max_episode_length(self):
    return self._fbs_description.Objective().MaxEpisodeLength()

  @property
  def solved_threshold(self):
    return self._fbs_description.Objective().SolvedThreshold()

  @property
  def actors(self):
    return neodroid.messaging.deserialise_actors(self._fbs_description)

  def actor(self, key):
    actors = self.actors
    if key in actors:
      return actors[key]

  @property
  def actuators(self):
    return neodroid.messaging.deserialise_actors(self._fbs_description)[0].actuators

  def actuator(self, key):
    actuators = self.actuators
    if key in actuators:
      return actuators[key]

  @property
  def sensors(self):
    return neodroid.messaging.deserialise_sensors(self._fbs_description)

  def sensor(self, key):
    sensors = self.sensors
    if key in sensors:
      return sensors[key]

  @property
  def configurables(self):
    return neodroid.messaging.deserialise_configurables(self._fbs_description)

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
            f'<SolvedThreshold>{self.solved_threshold}</SolvedThreshold>\n'
            f'<Actors>\n{actors_str}</Actors>\n'
            f'<Configurables>\n{configurables_str}</Configurables>\n'
            f'</EnvironmentDescription>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
