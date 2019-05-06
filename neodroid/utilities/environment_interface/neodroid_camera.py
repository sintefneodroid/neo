#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PIL
import numpy
from PIL import Image
import warg

__author__ = 'cnheider'


def extract_neodroid_camera_images(environment):
  rgb = environment.sensor('RGB')
  rgb_image = None
  if rgb:
    rgb_image = Image.open(rgb.observation_value)

  depth = environment.sensor('Depth')
  depth_image = None
  if depth:
    depth_image = Image.open(depth.observation_value)

  segmentation = environment.sensor('Segmentation')
  segmentation_image = None
  if segmentation:
    segmentation_image = Image.open(segmentation.observation_value)

  instance_segmentation = environment.sensor('InstanceSegmentation')
  instance_segmentation_image = None
  if instance_segmentation:
    instance_segmentation_image = Image.open(instance_segmentation.observation_value)

  infrared = environment.sensor('InfraredShadow')
  infrared_image = None
  if infrared:
    infrared_image = Image.open(infrared.observation_value)

  flow = environment.sensor('Flow')
  flow_image = None
  if flow:
    flow_image = Image.open(flow.observation_value)

  normal = environment.sensor('Normal')
  normal_image = None
  if normal:
    normal_image = Image.open(normal.observation_value)

  satellite = environment.sensor('Satellite')
  satellite_image = None
  if satellite:
    satellite_image = Image.open(satellite.observation_value)

  object_space = environment.sensor('ObjectSpaceFloat')
  object_space_image = None
  if object_space:
    if isinstance(object_space.observation_value, bytes):
      object_space_image = Image.open(object_space.observation_value)
    else:
      object_space_image = Image.fromarray(numpy.array(object_space.observation_value).reshape(224,224,4),
                                           mode='RGBA').transpose(PIL.Image.FLIP_TOP_BOTTOM)

  world_space = environment.sensor('WorldSpace')
  world_space_image = None
  if world_space:
    world_space_image = Image.open(world_space.observation_value)

  uvs = environment.sensor('UVs')
  uvs_image = None
  if uvs:
    uvs_image = Image.open(uvs.observation_value)

  tangents = environment.sensor('Tangents')
  tangents_image = None
  if tangents:
    tangents_image = Image.open(tangents.observation_value)

  return warg.NOD.dict_of(rgb_image,
                          depth_image,
                          segmentation_image,
                          instance_segmentation_image,
                          infrared_image,
                          flow_image,
                          normal_image,
                          satellite_image,
                          object_space_image,
                          world_space_image,
                          uvs_image,
                          tangents_image)
