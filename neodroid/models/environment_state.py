class EnvironmentState(object):
  def __init__(self,
               time_since_reset=0,
               total_energy_spent_since_reset=0,
               actors=None,
               observers=None,
               last_steps_frame_number=0,
               reward_for_last_step=0,
               interrupted=False):
    if observers is None:
      observers = {}
    if actors is None:
      actors = {}
    self._time_since_reset = time_since_reset
    self._total_energy_spent_since_reset = total_energy_spent_since_reset
    self._actors = actors
    self._observers = observers
    self._reward_for_last_step = reward_for_last_step
    self._last_steps_frame_number = last_steps_frame_number
    self._interrupted = interrupted

  def get_time_since_reset(self):
    return self._time_since_reset

  def get_total_energy_spent_since_reset(self):
    return self._total_energy_spent_since_reset

  def get_actors(self):
    return self._actors

  def get_actor(self, key):
    return self._actors[key]

  def get_observers(self):
    return self._observers

  def get_observer(self, key):
    return self._observers[key]

  def get_reward_for_last_step(self):
    return self._reward_for_last_step

  def get_last_steps_frame_number(self):
    return self._last_steps_frame_number

  def get_interrupted(self):
    return self._interrupted

  def __repr__(self):
    observers_str = ''.join([
      str(observer.__repr__()) for observer in self._observers.values()
    ])
    actors_str = ''.join(
        [str(actor.__repr__()) for actor in self._actors.values()])

    return '<EnvironmentState>\n' + \
           '  <time_since_reset>' + \
           str(self._time_since_reset) + \
           '</time_since_reset>\n' + \
           '  <total_energy_spent_since_reset>' + \
           str(self._total_energy_spent_since_reset) + \
           '</total_energy_spent_since_reset>\n' + \
           '  <last_steps_frame_number>' + \
           str(self._last_steps_frame_number) + \
           '</last_steps_frame_number>\n' + \
           '  <reward_for_last_step>' + \
           str(self._reward_for_last_step) + \
           '</reward_for_last_step>\n' + \
           '  <interrupted>' + \
           str(self._interrupted) + \
           '</interrupted>\n' + \
           '  <Actors>\n' + \
           actors_str + \
           '  </Actors>\n' + \
           '  <Observers>\n' + \
           observers_str + \
           '  </Observers>\n' + \
           '</EnvironmentState>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
