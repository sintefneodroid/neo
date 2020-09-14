# !/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import numpy


class ContextualBanditEnvironment(object):
    """

  """

    def __init__(self, seed=0):

        self.np_random = numpy.random.RandomState()
        self.np_random.seed(seed)

        self.bandits = numpy.array(
            [[0.8, 0.0, 0.0, 0.9], [0.6, 0.0, 1.0, 0.2], [0.6, 0.0, 0.0, 0.5]]
        )
        self.num_bandits = self.bandits.shape[0]
        self.num_actions = self.bandits.shape[1]

    def update_state(self):
        """

    @return:
    @rtype:
    """
        self.state = self.np_random.randint(0, len(self.bandits))
        return self.state

    def reset(self):
        """

    @return:
    @rtype:
    """
        return self.update_state()

    def act(self, action):
        """

    @param action:
    @type action:
    @return:
    @rtype:
    """
        threshold = self.bandits[self.state, action]
        result = self.np_random.random_sample()
        if result > threshold:
            return self.update_state(), 1, False, None
        else:
            return self.update_state(), -1, False, None


if __name__ == "__main__":
    env = ContextualBanditEnvironment()
    state = env.reset()
    for i in range(10000):
        action = numpy.random.randint(env.num_actions)
        state, signal, *_ = env.act(
            action
        )  # Get our signal for taking an action given a bandit.
        print(state, action, signal)
