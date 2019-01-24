#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import warg

__author__ = 'cnheider'


def extract_neodroid_camera_images(environment):
  rgb = environment.sensor('RGBCameraObserver')
  rgb_image = None
  if rgb:
    rgb_image = Image.open(rgb.observation_value)

  depth = environment.sensor('DepthCameraObserver')
  depth_image = None
  if depth:
    depth_image = Image.open(depth.observation_value)

  segmentation = environment.sensor('SegmentationCameraObserver')
  segmentation_image = None
  if segmentation:
    segmentation_image = Image.open(segmentation.observation_value)

  instance_segmentation = environment.sensor('InstanceSegmentationCameraObserver')
  instance_segmentation_image = None
  if instance_segmentation:
    instance_segmentation_image = Image.open(instance_segmentation.observation_value)

  infrared = environment.sensor('InfraredShadowCameraObserver')
  infrared_image = None
  if infrared:
    infrared_image = Image.open(infrared.observation_value)

  flow = environment.sensor('FlowCameraObserver')
  flow_image = None
  if flow:
    flow_image = Image.open(flow.observation_value)

  normal = environment.sensor('NormalCameraObserver')
  normal_image = None
  if normal:
    normal_image = Image.open(normal.observation_value)

  satellite = environment.sensor('SatelliteCameraObserver')
  satellite_image = None
  if satellite:
    satellite_image = Image.open(satellite.observation_value)

  object_space = environment.sensor('ObjectSpaceCameraObserver')
  object_space_image = None
  if object_space:
    object_space_image = Image.open(object_space.observation_value)

  world_space = environment.sensor('WorldSpaceCameraObserver')
  world_space_image = None
  if world_space:
    world_space_image = Image.open(world_space.observation_value)

  uvs = environment.sensor('UVsCameraObserver')
  uvs_image = None
  if uvs:
    uvs_image = Image.open(uvs.observation_value)

  tangents = environment.sensor('TangentsCameraObserver')
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
