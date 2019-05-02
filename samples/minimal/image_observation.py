#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import cv2
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

env = neogym(environment_name='dmr', connect_to_running=True)
fig = plt.figure()


def update_figures(i):
  global time_s, frame_i, image_axs

  sample = env.action_space.sample()
  obs, signal, terminated, info = env.step(sample)
  for obs in info.observers.values():
    print(obs)

  new_images = extract_neodroid_camera_images(env)

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

  if image_axs.rgb_image and new_images.rgb_image:
    image_axs.rgb_image.set_data(new_images.rgb_image)

  if image_axs.depth_image and new_images.depth_image:
    image_axs.depth_image.set_data(new_images.depth_image)

  if image_axs.infrared_image and new_images.infrared_image:
    image_axs.infrared_image.set_data(new_images.infrared_image)

  if image_axs.flow_image and new_images.flow_image:
    image_axs.flow_image.set_data(new_images.flow_image)

  if image_axs.normal_image and new_images.normal_image:
    image_axs.normal_image.set_data(new_images.normal_image)

  if image_axs.satellite_image and new_images.satellite_image:
    image_axs.satellite_image.set_data(new_images.satellite_image)

  if image_axs.object_space_image and new_images.object_space_image:
    image_axs.object_space_image.set_data(new_images.object_space_image)

  if image_axs.uvs_image and new_images.uvs_image:
    image_axs.uvs_image.set_data(new_images.uvs_image)

  if image_axs.tangents_image and new_images.tangents_image:
    image_axs.tangents_image.set_data(new_images.tangents_image)

  if image_axs.world_space_image and new_images.world_space_image:
    image_axs.world_space_image.set_data(new_images.world_space_image)

  if image_axs.segmentation_image and new_images.segmentation_image:
    image_axs.segmentation_image.set_data(new_images.segmentation_image)

  if image_axs.instance_segmentation_image and new_images.instance_segmentation_image:
    image_axs.instance_segmentation_image.set_data(new_images.instance_segmentation_image)

  if terminated:
    env.reset()
    frame_i = 0
  else:
    frame_i += 1


def main():
  global image_axs

  ((rgb_image,
    depth_image,
    infrared_image,
    world_space_image),
   (flow_image,
    normal_image,
    satellite_image,
    segmentation_image),
   (object_space_image,
    uvs_image,
    tangents_image,
    instance_segmentation_image)) = fig.subplots(3, 4, sharey='all')

  image_axs = warg.NOD.dict_of(rgb_image,
                               depth_image,
                               infrared_image,
                               flow_image,
                               normal_image,
                               satellite_image,
                               object_space_image,
                               uvs_image,
                               tangents_image,
                               world_space_image,
                               segmentation_image,
                               instance_segmentation_image)

  env.reset()
  acs = env.action_space.sample()
  obs, rew, term, info = env.step(acs)

  for obs in info.observers.values():
    print(obs)

  new_images = extract_neodroid_camera_images(env)

  rgb_image.set_title('RGB')
  if new_images.rgb_image:
    image_axs.rgb_image = rgb_image.imshow(new_images.rgb_image)

  depth_image.set_title('Depth')
  if new_images.depth_image:
    image_axs.depth_image = depth_image.imshow(new_images.depth_image)

  infrared_image.set_title('Infrared')
  if new_images.infrared_image:
    image_axs.infrared_image = infrared_image.imshow(new_images.infrared_image)

  flow_image.set_title('Flow')
  if new_images.flow_image:
    image_axs.flow_image = flow_image.imshow(new_images.flow_image)

  normal_image.set_title('Normal')
  if new_images.normal_image:
    image_axs.normal_image = normal_image.imshow(new_images.normal_image)

  satellite_image.set_title('Satellite')
  if new_images.satellite_image:
    image_axs.satellite_image = satellite_image.imshow(new_images.satellite_image)

  object_space_image.set_title('ObjectSpace')
  if new_images.object_space_image:
    image_axs.object_space_image = object_space_image.imshow(new_images.object_space_image)

  uvs_image.set_title('UVs')
  if new_images.uvs_image:
    image_axs.uvs_image = uvs_image.imshow(new_images.uvs_image)

  tangents_image.set_title('Tangents')
  if new_images.tangents_image:
    image_axs.tangents_image = tangents_image.imshow(new_images.tangents_image)

  world_space_image.set_title('WorldSpace')
  if new_images.world_space_image:
    image_axs.world_space_image = world_space_image.imshow(new_images.world_space_image)

  segmentation_image.set_title('Segmentation')
  if new_images.segmentation_image:
    image_axs.segmentation_image = segmentation_image.imshow(new_images.segmentation_image)

  instance_segmentation_image.set_title('Instance')
  if new_images.instance_segmentation_image:
    image_axs.instance_segmentation_image = instance_segmentation_image.imshow(
      new_images.instance_segmentation_image)

  _ = animation.FuncAnimation(fig, update_figures)
  plt.show()


if __name__ == '__main__':
  main()
