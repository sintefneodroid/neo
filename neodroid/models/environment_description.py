import neodroid.messaging


class EnvironmentDescription(object):
  def __init__(self, fbs_description):
    self._fbs_description = fbs_description

  @property
  def simulator_configuration(self):
    return self._fbs_description.SimulatorConfiguration()

  @property
  def api_version(self):
    return self._fbs_description.ApiVersion().decode()

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
    return neodroid.messaging.create_actors(self._fbs_description)

  def actor(self, key):
    actors = self.actors
    if key in actors:
      return actors[key]

  @property
  def configurables(self):
    return neodroid.messaging.create_configurables(self._fbs_description)

  def configurable(self, key):
    configurables = self.configurables
    if key in configurables:
      return configurables[key]

  def __repr__(self):
    actors_str = ''.join(
        [str(actor.__repr__()) for actor in self.actors.values()])

    configurables_str = ''.join(
        [str(configurable.__repr__()) for configurable in self.configurables.values()])

    # '  <objective_name>' +  self.objective_name + '</objective_name>\n' \

    return '<EnvironmentDescription>\n' + \
           '  <MaxEpisodeLength>' + str(
        self.max_episode_length) + '</MaxEpisodeLength>\n' \
                                   '  <SolvedThreshold>' + str(
        self.solved_threshold) + '</SolvedThreshold>\n' \
                                 '  <Actors>\n' + \
           actors_str + \
           '  </Actors>\n' + \
           '  <Configurables>\n' + \
           configurables_str + \
           '  </Configurables>\n' + \
           '</EnvironmentDescription>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
