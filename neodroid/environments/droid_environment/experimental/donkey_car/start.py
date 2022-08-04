#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 7/7/22
           """

__all__ = []

import gym
import numpy


# SET UP ENVIRONMENT
# You can also launch the simulator separately
# in that case, you don't need to pass a `conf` object
exe_path = f"donkey_sim.exe"
port = 9091

conf = {"exe_path": exe_path, "port": port}

env = gym.make("donkey-generated-track-v0", conf=conf)

# PLAY
obs = env.reset()
for t in range(100):
    action = numpy.array([0.0, 0.5])  # drive straight with small speed
    # execute the action
    obs, reward, done, info = env.step(action)

# Exit the scene
env.close()
