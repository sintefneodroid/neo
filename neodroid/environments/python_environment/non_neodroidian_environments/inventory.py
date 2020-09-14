#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 20/02/2020
           """

import logging

import gym
import numpy
from gym import spaces, utils
from gym.utils import seeding

logger = logging.getLogger(__name__)


class InventoryEnv(gym.Env, utils.EzPickle):
    """Inventory control with lost sales environment

This environment corresponds to the version of the inventory control
with lost sales problem described in Example 1.1 in Algorithms for
Reinforcement Learning by Csaba Szepesvari (2010).
https://sites.ualberta.ca/~szepesva/RLBook.html
"""

    def step(self, action):
        return self._step(action)

    def reset(self):
        return self._reset()

    def render(self, mode="human"):
        pass

    def __init__(self, n: int = 100, k=5, c=2, h=2, p=3, lam=8):
        super().__init__()
        self.n = n
        self.action_space = spaces.Discrete(n)
        self.observation_space = spaces.Discrete(n)
        self.max = n
        self.state = n
        self.k = k
        self.c = c
        self.h = h
        self.p = p
        self.lam = lam

        # Set seed
        self._seed()

        # Start the first round
        self._reset()

    def demand(self):
        return numpy.random.poisson(self.lam)

    def transition(self, x, a, d):
        m = self.max
        return max(min(x + a, m) - d, 0)

    def reward(self, x, a, y):
        k = self.k
        m = self.max
        c = self.c
        h = self.h
        p = self.p
        r = (
            -k * (a > 0)
            - c * max(min(x + a, m) - x, 0)
            - h * x
            + p * max(min(x + a, m) - y, 0)
        )
        return r

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        assert self.action_space.contains(action)
        obs = self.state
        demand = self.demand()
        obs2 = self.transition(obs, action, demand)
        self.state = obs2
        reward = self.reward(obs, action, obs2)
        done = 0
        return obs2, reward, done, {}

    def _reset(self):
        return self.state


if __name__ == "__main__":
    s = InventoryEnv()
    print(s.step(s.action_space.sample()))
    print(s.step(s.action_space.sample()))
    print(s.step(s.action_space.sample()))
    print(s.step(s.action_space.sample()))
