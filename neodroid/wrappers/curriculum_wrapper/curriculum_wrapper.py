from neodroid import NeodroidEnvironment, Reaction, Configuration
from neodroid.modeling.reaction_parameters import ReactionParameters
from neodroid.utilities.statics import flattened_observation


class NeodroidCurriculumWrapper(NeodroidEnvironment):
  def __init__(self, **kwargs):
    super(NeodroidCurriculumWrapper, self).__init__(**kwargs)
    self.observation_space = self.__observation_space__()
    self.action_space = self.__action_space__()

  def act(self,
          input_reaction=None,
          on_step_done_callback=None,
          on_reaction_sent_callback=None):
    message = super(NeodroidCurriculumWrapper, self).react(input_reaction,
                                                       on_reaction_sent_callback,
                                                       on_step_done_callback)
    if message:
      return (flattened_observation(message),
              message.get_reward(),
              message.get_interrupted(), message)
    return None, None, None, None

  def configure(self, input_configuration=[], on_reset_callback=None):
    message = super(NeodroidCurriculumWrapper, self).reset(input_configuration,
                                                       on_reset_callback)
    if message:
      return flattened_observation(message), message
    return None, None

  def get_goal_configuration(self):
    message = super(NeodroidCurriculumWrapper, self).observe()
    if message:
      goal_x = message.get_environment_description().get_configurable(b'GoalTransformX').get_current_value()
      goal_y = message.get_environment_description().get_configurable(b'GoalTransformY').get_current_value()
      goal_z = message.get_environment_description().get_configurable(b'GoalTransformZ').get_current_value()
      return goal_z

  def generate_inital_states(self, motion_horizon=99, num=999):
    goal_pos = self.get_goal_configuration()
    initial_states=[]
    while len(initial_states) < num:
      params = ReactionParameters(False,False,True,True,True)
      init = Reaction(params,[Configuration('ActorTransformX',goal_pos[0]),
                              Configuration('ActorTransformY',goal_pos[1]),
                              Configuration('ActorTransformZ',goal_pos[2])])
      _, info = self.configure(init)
      terminated = False

      for i in range(motion_horizon):
        _,_,terminated,info =  self.act(self.run_brownian_motion(1))
        if not terminated:
          initial_states.append(info)
        else:
          break


    return initial_states

  def quit(self, callback=None):
    self.close(callback=callback)
