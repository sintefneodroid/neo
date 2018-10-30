#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from neodroid.neodroid_utilities.environment_interface.neodroid_camera import extract_neodroid_camera_images

__author__ = 'cnheider'

# import cv2
import matplotlib.pyplot as plt
from matplotlib import animation

from neodroid.wrappers.gym_wrapper import NeodroidGymWrapper as neogym


def grab_video_frame(cap):
  ret, frame = cap.read()
  return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


frame_i = 0
time_s = time.time()

im1 = None
im2 = None
im3 = None
im4 = None
im5 = None
im6 = None
im7 = None
im8 = None

env = neogym(environment_name='dmr', connect_to_running=False)
fig = plt.figure()

def update_figures(i):
  global time_s, frame_i, im1, im2, im3, im4, im5, im6, im7, im8

  sample = env.action_space.sample()
  _, signal, terminated, info = env.step(sample)

  (image_color,
   image_depth,
   image_segmentation,
   image_instance,
   image_infrared,
   image_flow,
   image_normal,
   image_satellite) = extract_neodroid_camera_images(env)

  time_now = time.time()
  if time_s:
    fps = (1 / (time_now - time_s))
  else:
    fps = 0

  time_s = time_now

  fig.suptitle(f'Update{i}, '
               f'Frame: {frame_i}, '
               f'FPS: {fps}, '
               f'Signal: {signal}, '
               f'Terminated: {bool(terminated)}')
  if im1:
    im1.set_data(image_color)
  if im2:
    im2.set_data(image_depth)
  if im3:
    im3.set_data(image_segmentation)
  if im4:
    im4.set_data(image_instance)
  if im5:
    im5.set_data(image_infrared)
  if im6:
    im6.set_data(image_flow)
  if im7:
    im7.set_data(image_normal)
  if im8:
    im8.set_data(image_satellite)

  if terminated:
    env.reset()
    frame_i = 0
  else:
    frame_i += 1

def main():
  global im1, im2, im3, im4, im5, im6, im7, im8

  ((ax1,
    ax2,
    ax3,
    ax4),
   (ax5,
    ax6,
    ax7,
    ax8),
   *_) = fig.subplots(2, 4, sharey='all')

  env.reset()
  obs, rew, term, info = env.step(env.action_space.sample())

  (image_color,
   image_depth,
   image_segmentation,
   image_instance,
   image_infrared,
   image_flow,
   image_normal,
   image_satellite) = extract_neodroid_camera_images(env)

  ax1.set_title('RGB')
  if image_color:
    im1 = ax1.imshow(image_color)
  ax2.set_title('Depth')
  if image_depth:
    im2 = ax2.imshow(image_depth)
  ax3.set_title('Segmentation')
  if image_segmentation:
    im3 = ax3.imshow(image_segmentation)
  ax4.set_title('Instance')
  if image_instance:
    im4 = ax4.imshow(image_instance)
  ax5.set_title('Infrared')
  if image_infrared:
    im5 = ax5.imshow(image_infrared)
  ax6.set_title('Flow')
  if image_flow:
    im6 = ax6.imshow(image_flow)
  ax7.set_title('Normal')
  if image_normal:
    im7 = ax7.imshow(image_normal)
  ax8.set_title('Satellite')
  if image_satellite:
    im8 = ax8.imshow(image_satellite)



  _ = animation.FuncAnimation(fig, update_figures)
  plt.show()


if __name__ == '__main__':
  main()
