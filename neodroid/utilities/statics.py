import numpy as np

def flat_observation(message):
  return np.array([obs.get_data() for obs in message.get_observers().values()]).flatten()
