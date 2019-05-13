#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import cv2

import warg
from neodroid.wrappers import NeodroidGymWrapper
from neodroid.utilities.messaging_utilities.neodroid_camera_extraction import extract_neodroid_camera

__author__ = 'cnheider'

# import cv2
import matplotlib.pyplot as plt
from matplotlib import animation


def grab_video_frame(cap):
  ret, frame = cap.read()
  return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


frame_i = 0
time_s = time.time()

image_axs = warg.NOD()

env = NeodroidGymWrapper(connect_to_running=True)
fig = plt.figure()
print_obs = False


def update_figures(i):
  global time_s, frame_i, image_axs

  sample = env.action_space.sample()
  obs, signal, terminated, info = env.step(sample)
  if print_obs:
    for obs in info.observers.values():
      print(obs)

  new_images = extract_neodroid_camera(info, ('RGB', 'ObjectSpace'),image_size=(128,128,4))

  time_now = time.time()
  if time_s:
    fps = (1 / (time_now - time_s))
  else:
    fps = 0

  time_s = time_now

  fig.suptitle(f'Update: {i}, '
               f'Frame: {frame_i}, '
               f'FPS: {fps}, '
               f'Signal: {signal}, '
               f'Terminated: {bool(terminated)}')

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
  obs, rew, term, info = env.step(acs)
  if print_obs:
    for obs in info.observers.values():
      print(obs)

  new_images = extract_neodroid_camera(info, ('RGB', 'ObjectSpace'),image_size=(None,None,4))

  xs = int(len(new_images) / 2)
  ys = 2

  axes = fig.subplots(ys, xs, sharex='all', sharey='all')

  a = axes.flatten()
  for ax, (k,v) in zip(a, new_images.items()):
    if k:
      ax.set_title(k)
      image_axs[k] = ax.imshow(v,vmin=0, vmax=255)

  _ = animation.FuncAnimation(fig, update_figures)
  plt.show()


if __name__ == '__main__':
  main()
