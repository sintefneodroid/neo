#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
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
  rgb = environment.sensor('RGBCamera').observation_value
  rgb_im = Image.open(rgb)

  depth = environment.sensor('DepthCamera').observation_value
  depth_im = Image.open(depth)

  segmentation = environment.sensor('SegmentationCamera').observation_value
  segmentation_im = Image.open(segmentation)

  instance_segmentation = environment.sensor('InstanceSegmentationCamera').observation_value
  instance_segmentation_im = Image.open(instance_segmentation)

  infrared = environment.sensor('InfraredShadowCamera').observation_value
  infrared_im = Image.open(infrared)

  flow = environment.sensor('FlowCamera').observation_value
  flow_im = Image.open(flow)

  normal = environment.sensor('NormalCamera').observation_value
  normal_im = Image.open(normal)

  satellite = environment.sensor('SatelliteCamera').observation_value
  satellite_im = Image.open(satellite)

  return rgb_im, depth_im, segmentation_im, instance_segmentation_im, infrared_im, flow_im, normal_im, \
         satellite_im


env = neogym.make(environment_name='obs', connect_to_running=True)
fig = plt.figure()

(ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), *_ = fig.subplots(2, 4, sharey='all')
frame_i = 0
env.reset()
obs, rew, term, info = env.step()
image_color, image_depth, image_segmentation, image_instance, image_infrared, image_flow, image_normal, \
image_satellite \
  = grab_new_images(env)

ax1.set_title('RGB')
im1 = ax1.imshow(image_color)
ax2.set_title('Depth')
im2 = ax2.imshow(image_depth)
ax3.set_title('Segmentation')
im3 = ax3.imshow(image_segmentation)
ax4.set_title('Instance')
im4 = ax4.imshow(image_instance)
ax5.set_title('Infrared')
im5 = ax5.imshow(image_infrared)
ax6.set_title('Flow')
im6 = ax6.imshow(image_flow)
ax7.set_title('Normal')
im7 = ax7.imshow(image_normal)
ax8.set_title('Satellite')
im8 = ax8.imshow(image_satellite)


def update_figures(i):
  global time_s, frame_i
  _, signal, terminated, info = env.step()
  image_color, image_depth, image_segmentation, image_instance, image_infrared, image_flow, image_normal, \
  image_satellite \
    = grab_new_images(env)

  time_now = time.time()

  fps = (1 / (time_now - time_s))

  time_s = time_now

  fig.suptitle(f'Frame: {frame_i}, FPS: {fps}, Signal: {signal}, Terminated: {bool(terminated)}')

  im1.set_data(image_color)
  im2.set_data(image_depth)
  im3.set_data(image_segmentation)
  im4.set_data(image_instance)
  im5.set_data(image_infrared)
  im6.set_data(image_flow)
  im7.set_data(image_normal)
  im8.set_data(image_satellite)

  if terminated:
    env.reset()
    frame_i = 0
  else:
    frame_i += 1


time_s = time.time()
ani = animation.FuncAnimation(fig, update_figures)
plt.show()
