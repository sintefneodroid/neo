from random import uniform

import gym
import beamnggym  # pip install pip install BeamNG.gym

env = gym.make("BNG-WCA-Race-Geometry-v0")
env.reset()
total_reward, done = 0, False
# Drive around randomly until finishing
while not done:
    obs, reward, done, aux = env.step((uniform(-1, 1), uniform(-1, 1)))
    total_reward += reward
print("Achieved reward:", total_reward)
