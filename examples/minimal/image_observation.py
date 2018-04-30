#!/usr/bin/env python3
# coding=utf-8
import time

__author__ = 'cnheider'

# import cv2
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import animation

import neodroid.wrappers.gym_wrapper as neogym


def grab_video_frame(cap):
  ret, frame = cap.read()
  return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def grab_new_images(environment):
  image_color = environment.sensor('RGBCamera').observation_value
  image_depth = environment.sensor('DepthCamera').observation_value
  image_segmentation = environment.sensor('SegmentationCamera').observation_value

  image_color = Image.open(image_color)
  image_depth = Image.open(image_depth)
  image_segmentation = Image.open(image_segmentation)

  return image_color, image_depth, image_segmentation


env = neogym.make('camera_observation', connect_to_running=True)
fig = plt.figure()

ax1, ax2, ax3, *_ = fig.subplots(1, 3, sharey='all')

obs, rew, term, info = env.step(0)
print(obs)
image_color, image_depth, image_segmentation, *_ = grab_new_images(env)

ax1.set_title('RGB')
im1 = ax1.imshow(image_color)
ax2.set_title('Depth')
im2 = ax2.imshow(image_depth)
ax3.set_title('Segmentation')
im3 = ax3.imshow(image_segmentation)


def update_figures(i):
  global time_s
  _, _, _, info = env.step()
  image_color, image_depth, image_segmentation, *_ = grab_new_images(env)

  time_now = time.time()

  fps = (1/(time_now - time_s))

  time_s = time_now

  plt.title(f'FPS: {fps}')

  im1.set_data(image_color)
  im2.set_data(image_depth)
  im3.set_data(image_segmentation)


time_s = time.time()
ani = animation.FuncAnimation(fig, update_figures)
plt.show()
