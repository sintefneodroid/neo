#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from math import ceil, floor, sqrt

import cv2
import numpy
from matplotlib import animation, pyplot

from neodroid.environments.droid_environment import UnityEnvironment
from neodroid.utilities.snapshot_extraction.camera_extraction import extract_all_cameras
from warg.named_ordered_dictionary import NOD

__author__ = "Christian Heider Nielsen"
__doc__ = ""


def grab_video_frame(cap):
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


idependant_frame_i = 0
time_s = time.time()

image_axs = NOD()

env = UnityEnvironment(connect_to_running=True)
fig = pyplot.figure()
print_obs = False
reset_every_step = False


def update_figures(ith_figure_update: int):
    global time_s, idependant_frame_i, image_axs

    if reset_every_step:
        info = next(iter(env.reset().values()))
        idependant_frame_i = 0
    else:
        info = next(iter(env.react().values()))
        idependant_frame_i += 1

    if print_obs:
        print(idependant_frame_i)
        for obs in info.sensors.values():
            print(obs)

    new_images = extract_all_cameras(info)

    # new_images['RGB'] = new_images['RGB'] ** 0.454545

    # print( numpy.max(new_images['RGB']))

    time_now = time.time()
    if time_s:
        fps = 1 / (time_now - time_s)
    else:
        fps = 0

    time_s = time_now

    for k, v in new_images.items():
        image_axs[k].set_data(v)

    fig.suptitle(
        f"Update: {idependant_frame_i}, "
        f"Frame: {info.frame_number}, "
        f"FPS: {fps}, "
        f"Signal: {info.signal}, "
        f"Terminated: {bool(info.terminated)}"
    )


def main():
    global image_axs

    info = next(iter(env.reset().values()))
    if print_obs:
        print(0)
        for obs in info.sensors.values():
            print(obs)

    new_images = extract_all_cameras(info)

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
