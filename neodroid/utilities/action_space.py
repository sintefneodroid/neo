import numpy as np


class ActionSpace(object):

  def __init__(self, valid_inputs):
    self._valid_inputs = valid_inputs

  def sample(self):
    actions = []
    for valid_input in self._valid_inputs:
      sample = np.random.uniform(valid_input.get_min_value(), valid_input.get_max_value(), 1)
      actions.append(np.round(sample, valid_input.get_decimal_granularity()))
    return actions

  def num_actions(self):
    return len(self._valid_inputs)

  def num_binary_actions(self):
    return len(self._valid_inputs)*2

  def discrete_binary_one_hot_sample(self):
    idx = np.random.randint(0, self.num_actions())
    zeros = np.zeros(self.num_binary_actions())
    sample =np.random.uniform(self._valid_inputs[idx].get_min_value(), self._valid_inputs[idx].get_max_value(), 1)
    if sample > 0:
      zeros[idx] = 1
    else:
      zeros[idx+self.num_actions()] = 1
    return zeros

  def one_hot_sample(self):
    idx = np.random.randint(0, self.num_actions())
    zeros = np.zeros(self.num_actions())
    sample = np.random.uniform(self._valid_inputs[idx].get_min_value(), self._valid_inputs[idx].get_max_value(), 1)
    zeros[idx] = np.round(sample,self._valid_inputs[idx].get_decimal_granularity())
    return zeros
