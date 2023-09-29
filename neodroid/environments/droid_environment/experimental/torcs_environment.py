#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 7/15/22
           """

__all__ = []

import numpy


class Agent(object):
    def __init__(self, dim_action):
        self.dim_action = dim_action

    def act(self, ob, reward, done, vision_on):
        # print("ACT!")

        # Get an Observation from the environment.
        # Each observation vectors are numpy array.
        # focus, opponents, track sensors are scaled into [0, 1]. When the agent
        # is out of the road, sensor variables return -1/200.
        # rpm, wheelSpinVel are raw values and then needed to be preprocessed.
        # vision is given as a tensor with size of (64*64, 3) = (4096, 3) <-- rgb
        # and values are in [0, 255]
        if vision_on is False:
            # print( ob)
            # focus, speedX, speedY, speedZ, angle, damage, opponents, rpm, track, trackPos, wheelSpinVel, lap = ob
            pass
        else:
            # focus, speedX, speedY, speedZ, opponents, rpm, track, wheelSpinVel, vision = ob

            """The code below is for checking the vision input. This is very heavy for real-time Control
            So you may need to remove.
            """
            # print(vision.shape)
            """
img = np.ndarray((64,64,3))
for i in range(3):
    img[:, :, i] = 255 - vision[:, i].reshape((64, 64))

plt.imshow(img, origin='lower')
plt.draw()
plt.pause(0.001)
"""
            pass

        return numpy.tanh(numpy.random.randn(self.dim_action))  # random action


if __name__ == "__main__":
    import gym

    # import gym_donkeycar
    #    import gym_torcs
    import gym_torcs

    print(gym_torcs.__file__)

    def obs_preprocess_fn(dict_obs):
        return numpy.hstack(
            (
                dict_obs["angle"],
                dict_obs["track"],
                dict_obs["trackPos"],
                dict_obs["speedX"],
                dict_obs["speedY"],
                dict_obs["speedZ"],
                dict_obs["wheelSpinVel"],
                dict_obs["rpm"],
                # dict_obs['img'],
                dict_obs["opponents"],
            )
        )

    env = None
    try:
        env = gym.make(
            "Torcs-v0",
            # vision=False,
            # rendering=False,
            # obs_preprocess_fn=obs_preprocess_fn
        )

        o, r, done = env.reset(), 0.0, False
        while not done:
            action = numpy.tanh(numpy.random.randn(env.action_space.shape[0]))
            o, r, done, _ = env.step(action)

    except Exception as e:
        print(e)

    finally:
        env.end()
