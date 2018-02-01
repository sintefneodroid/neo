import numpy as np


class ActionSpace(object):

  def __init__(self, valid_inputs):
    self._valid_inputs = valid_inputs

  def sample(self):
    actions = []
    for valid_input in self._valid_inputs:
      sample = np.random.uniform(valid_input.min_value, valid_input.max_value, 1)
      actions.append(np.round(sample, valid_input.decimal_granularity))
    return actions

  def validate(self, actions):
    for i in range(len(actions)):
      clipped = np.clip(self._valid_inputs[i].min_value, self._valid_inputs[i].max_value, actions[i])
      actions[i] = np.round(clipped, self._valid_inputs[i].decimal_granularity)
    return actions

  @property
  def shape(self):
    return [self.num_actions]

  @property
  def n(self):
    return self.num_actions

  @property
  def low(self):
    return [motion_space.min_value() for motion_space in self._valid_inputs]

  @property
  def high(self):
    return [motion_space.max_value() for motion_space in self._valid_inputs]

  @property
  def num_actions(self):
    return len(self._valid_inputs)

  @property
  def num_binary_actions(self):
    return len(self._valid_inputs) * 2

  @property
  def num_ternary_actions(self):
      return len(self._valid_inputs) * 3

  def discrete_ternary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_actions)
    zeros = np.zeros(self.num_ternary_actions)
    if len(self._valid_inputs) > 0:
      sample = np.random.uniform(self._valid_inputs[idx].min_value, self._valid_inputs[idx].max_value, 1)
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_actions] = 1
    return zeros

  def discrete_binary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_actions)
    zeros = np.zeros(self.num_binary_actions)
    if len(self._valid_inputs) > 0:
      sample = np.random.uniform(self._valid_inputs[idx].min_value, self._valid_inputs[idx].max_value, 1)
      if sample > 0:
        zeros[idx] = 1
      else:
        zeros[idx + self.num_actions] = 1
    return zeros

  def discrete_one_hot_sample(self):
    idx = np.random.randint(0, self.num_actions)
    zeros = np.zeros(self.num_actions)
    if len(self._valid_inputs) > 0:
      val = np.random.random_integers(self._valid_inputs[idx].min_value(),
                                      self._valid_inputs[idx].max_value(), 1)
      zeros[idx] = val
    return zeros

  def one_hot_sample(self):

    idx = np.random.randint(0, self.num_actions)
    zeros = np.zeros(self.num_actions)
    if len(self._valid_inputs) > 0:
      zeros[idx] = 1
    return zeros

  def __call__(self, *args, **kwargs):
    return self.shape

  def __len__(self):
    return len(self.shape)

  def __repr__(self):
    return str(self.shape)

  #def __int__(self):
  #  return int(sum(self.shape))