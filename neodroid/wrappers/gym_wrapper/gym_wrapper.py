from collections import namedtuple

import numpy as np

from neodroid import NeodroidEnvironment, messaging
from neodroid.models import Reaction
from neodroid.utilities.reaction_factory import verify_reaction


class NeodroidGymWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidGymWrapper, self).__init__(**kwargs)
    self.observation_space = self.__observation_space__()
    self.action_space = self.__action_space__()

  def step(self,
           input_reaction=None,
           on_step_done_callback=None,
           on_reaction_sent_callback=None):
    if self._debug_logging:
      self._logger.debug('Step')
    if self._latest_received_state:
      input_reaction = verify_reaction(input_reaction,
                                       self._latest_received_state.get_actors().values())
    else:
      input_reaction = verify_reaction(input_reaction, None)
    self._awaiting_response = True
    if self._connected:
      if on_reaction_sent_callback:
        messaging.start_send_reaction_thread(input_reaction,
                                             on_reaction_sent_callback)
      else:
        messaging.send_reaction(input_reaction)

      message = self.__get_state__(on_step_done_callback)
      if message:
        self._awaiting_response = False
        self._latest_received_state = message
        return (np.array([[obs.get_position(), obs.get_rotation(),
                           obs.get_direction()] for
                          obs in
                          message.get_observers(

                          ).values()]).flatten(),
                message.get_reward_for_last_step(),
                message.get_interrupted(), None)
    else:
      if self._debug_logging:
        self._logger.debug('Is not connected to environment')
    return (None,
            None,
            None,
            None)

  def reset(self, input_configuration=[]):
    if self._debug_logging:
      self._logger.debug('Reset')

    messaging.send_reaction(Reaction(True, input_configuration, []))

    message = self.__get_state__()

    if message:
      self._awaiting_response = False
      self._latest_received_state = message
      return np.array([obs.get_position()+ obs.get_rotation()+
                        obs.get_direction() for
                       obs in
                       message.get_observers(

                       ).values()]).flatten()
    else:
      return None

  def seed(self, seed):
    pass

  def __observation_space__(self):
    if self._latest_received_state:
      o = np.array([obs.get_position()+obs.get_rotation()+obs.get_direction() for obs in
                self._latest_received_state.get_observers().values()]).flatten()
      return o
    return np.zeros(1)

  def __sample_action_space__(self):
    return np.random.randint(-1,1,self._motors_num)


  def __action_space__(self):
    self._motors_num=0
    if self._latest_received_state:
      for actor in self._latest_received_state.get_actors().values():
        self._motors_num+=len(actor.get_motors().values())
    else:
      self._motors_num = 1
    action_space = namedtuple('action_space', ('n', 'sample'))
    return action_space(self._motors_num, self.__sample_action_space__)

  def render(self, *args, **kwargs):
    pass
