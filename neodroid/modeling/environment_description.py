from neodroid.messaging import create_actors, create_configurables


class EnvironmentDescription(object):
  def __init__(self, fbs_description):
    self._fbs_description = fbs_description

  def get_max_episode_length(self):
    return self._fbs_description.MaxEpisodeLength()

  def get_solved_threshold(self):
    return self._fbs_description.SolvedThreshold()

  def get_actors(self):
    return create_actors(self._fbs_description)

  def get_actor(self, key):
    return create_actors(self._fbs_description)[key]

  def get_configurables(self):
    return create_configurables(self._fbs_description)

  def get_configurable(self, key):
    return create_configurables(self._fbs_description)[key]

  def __repr__(self):
    actors_str = ''.join(
        [str(actor.__repr__()) for actor in self.get_actors().values()])

    configurables_str = ''.join(
        [str(configurable.__repr__()) for configurable in self.get_configurables().values()])

    return '<EnvironmentDescription>\n' + \
           '  <MaxEpisodeLength>' + str(
        self.get_max_episode_length()) + '</MaxEpisodeLength>\n' \
                                         '  <SolvedThreshold>' + str(
      self.get_solved_threshold()) + '</SolvedThreshold>\n' \
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
