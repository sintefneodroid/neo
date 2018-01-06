import numpy as np

from neodroid.messaging import create_poses, create_bodies


class Unobservables(object):
  def __init__(self, unobservables):
    self._unobservables = unobservables

  def get_poses_numpy(self):
    return create_poses(self._unobservables)


  def get_bodies_numpy(self):
    return create_bodies(self._unobservables)


  def get_unobservable_state_configuration(self):
    return np.array([self.get_poses_numpy().flatten(), self.get_bodies_numpy().flatten()]).flatten()

  def __repr__(self):
    return '<Unobservables>\n' + \
           '  <Poses>\n' + \
           str(self.get_poses_numpy()) + \
           '  </Poses>\n' + \
           '  <Bodies>\n' + \
           str(self.get_bodies_numpy()) + \
           '  </Bodies>\n' + \
           '</Unobservables>\n'

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()