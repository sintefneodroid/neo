#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from math import sqrt, floor, ceil
from typing import Iterable

import cv2
from matplotlib import pyplot
import numpy
from matplotlib import animation

from neodroid.environments.unity_environment import UnityEnvironment
from neodroid.environments.unity_environment.deprecated.batched_unity_environments import (
    VectorWrapper,
)
from neodroid.utilities.unity_specifications.prefabs.neodroid_camera_extraction import (
    extract_all_as_camera,
)
from warg.named_ordered_dictionary import NOD

__author__ = "Christian Heider Nielsen"
__doc__ = ""


def grab_video_frame(cap):
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


frame_i = 0
time_s = time.time()

image_axs = NOD()

env = VectorWrapper(UnityEnvironment(connect_to_running=True))
fig = pyplot.figure()
print_obs = False


def update_figures(i):
    global time_s, frame_i, image_axs

    # sample = env.action_space.sample()
    # obs, signal, terminated, info = env.react(sample).to_gym_like_output()
    obs, signal, terminated, info = env.reset().to_gym_like_output()
    if print_obs:
        print(i)
        for obs in info.sensors.values():
            print(obs)

    new_images = extract_all_as_camera(info)

    # new_images['RGB'] = new_images['RGB'] ** 0.454545

    # print( numpy.max(new_images['RGB']))

    time_now = time.time()
    if time_s:
        fps = 1 / (time_now - time_s)
    else:
        fps = 0

    time_s = time_now

    fig.suptitle(
        f"Update: {i}, "
        f"Frame: {frame_i}, "
        f"FPS: {fps}, "
        f"Signal: {signal}, "
        f"Terminated: {bool(terminated)}"
    )

    for k, v in new_images.items():
        image_axs[k].set_data(v)

    if terminated:
        env.reset()
        frame_i = 0
    else:
        frame_i += 1


def main():
    global image_axs

    env.reset()
    acs = env.action_space.sample()
    obs, rew, term, info = env.react(acs).to_gym_like_output()
    if print_obs:
        print(0)
        for obs in info.sensors.values():
            print(obs)

    new_images = extract_all_as_camera(info)

    side = sqrt(len(new_images))
    xs = ceil(side)
    ys = floor(side) + 1

    axes = fig.subplots(ys, xs, sharex="all", sharey="all")

    if isinstance(axes, numpy.ndarray):
        a = axes.flatten()
    else:
        a = [axes]
    for ax, (k, v) in zip(a, new_images.items()):
        if k:

            ax.set_facecolor("gray")
            ax.set_title(k)
            image_axs[k] = ax.imshow(v)

    _ = animation.FuncAnimation(fig, update_figures)
    pyplot.show()


if __name__ == "__main__":
    main()
