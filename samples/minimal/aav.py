#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
import warg

from neodroid.utilities.environment_interface.neodroid_camera import extract_neodroid_camera_images

__author__ = 'cnheider'

# import cv2
import matplotlib.pyplot as plt
from matplotlib import animation

from neodroid.wrappers.gym_wrapper import NeodroidVectorGymWrapper as neogym


def grab_video_frame(cap):
  ret, frame = cap.read()
  return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


frame_i = 0
time_s = time.time()

image_axs = warg.NOD()

env = neogym(environment_name='aav', connect_to_running=False)
fig = plt.figure()


def update_figures(i):
  global time_s, frame_i, image_axs

  sample = env.action_space.sample()
  obs, signal, terminated, info = env.step(sample)
  print(obs)

  images = extract_neodroid_camera_images(env)

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

  if image_axs.rgb_image:
    image_axs.rgb_image.set_data(images.rgb_image)
  if image_axs.depth_image:
    image_axs.depth_image.set_data(images.depth_image)
  if image_axs.infrared_image:
    image_axs.infrared_image.set_data(images.infrared_image)
  if image_axs.flow_image:
    image_axs.flow_image.set_data(images.flow_image)
  if image_axs.normal_image:
    image_axs.normal_image.set_data(images.normal_image)
  if image_axs.satellite_image:
    image_axs.satellite_image.set_data(images.satellite_image)
  if image_axs.object_space_image:
    image_axs.object_space_image.set_data(images.object_space_image)
  if image_axs.uvs_image:
    image_axs.uvs_image.set_data(images.uvs_image)
  if image_axs.tangents_image:
    image_axs.tangents_image.set_data(images.tangents_image)

  if terminated:
    env.reset()
    frame_i = 0
  else:
    frame_i += 1


def main():
  global image_axs

  ((rgb_image,
    depth_image,
    infrared_image),
   (flow_image,
    normal_image,
    satellite_image),
   (object_space_image,
    uvs_image,
    tangents_image)) = fig.subplots(3, 3, sharey='all')

  image_axs = warg.NOD.dict_of(rgb_image,
    depth_image,
    infrared_image,
   flow_image,
    normal_image,
    satellite_image,
   object_space_image,
    uvs_image,
    tangents_image)

  env.reset()
  obs, rew, term, info = env.step(env.action_space.sample())
  print(obs)

  images = extract_neodroid_camera_images(env)

  rgb_image.set_title('RGB')
  if images.rgb_image:
    image_axs.rgb_image = rgb_image.imshow(images.rgb_image)

  depth_image.set_title('Depth')
  if images.depth_image:
    image_axs.depth_image = depth_image.imshow(images.depth_image)

  infrared_image.set_title('Infrared')
  if images.infrared_image:
    image_axs.infrared_image = infrared_image.imshow(images.infrared_image)

  flow_image.set_title('Flow')
  if images.flow_image:
    image_axs.flow_image = flow_image.imshow(images.flow_image)

  normal_image.set_title('Normal')
  if images.normal_image:
    image_axs.normal_image = normal_image.imshow(images.normal_image)

  satellite_image.set_title('Satellite')
  if images.satellite_image:
    image_axs.satellite_image = satellite_image.imshow(images.satellite_image)

  object_space_image.set_title('object_space_image')
  if images.object_space_image:
    image_axs.object_space_image = object_space_image.imshow(images.object_space_image)

  uvs_image.set_title('uvs_image')
  if images.uvs_image:
    image_axs.uvs_image = uvs_image.imshow(images.uvs_image)

  tangents_image.set_title('tangents_image')
  if images.tangents_image:
    image_axs.tangents_image = tangents_image.imshow(images.tangents_image)

  _ = animation.FuncAnimation(fig, update_figures)
  plt.show()


if __name__ == '__main__':
  main()
