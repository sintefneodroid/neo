#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image

__author__ = 'cnheider'


def extract_neodroid_camera_images(environment):
  rgb = environment.sensor('RGBCameraObserver')
  rgb_im = None
  if rgb:
    rgb_im = Image.open(rgb.observation_value)

  depth = environment.sensor('DepthCameraObserver')
  depth_im = None
  if depth:
    depth_im = Image.open(depth.observation_value)

  segmentation = environment.sensor('SegmentationCameraObserver')
  segmentation_im = None
  if segmentation:
    segmentation_im = Image.open(segmentation.observation_value)
  print(environment.sensor('SegmentationSegmentationObserver'))

  instance_segmentation = environment.sensor('InstanceSegmentationCameraObserver')
  instance_segmentation_im = None
  if instance_segmentation:
    instance_segmentation_im = Image.open(instance_segmentation.observation_value)
  print(environment.sensor('InstanceSegmentationSegmentationObserver'))

  infrared = environment.sensor('InfraredShadowCameraObserver')
  infrared_im = None
  if infrared:
    infrared_im = Image.open(infrared.observation_value)

  flow = environment.sensor('FlowCameraObserver')
  flow_im = None
  if flow:
    flow_im = Image.open(flow.observation_value)

  normal = environment.sensor('NormalCameraObserver')
  normal_im = None
  if normal:
    normal_im = Image.open(normal.observation_value)

  satellite = environment.sensor('SatelliteCameraObserver')
  satellite_im = None
  if satellite:
    satellite_im = Image.open(satellite.observation_value)

  object_space = environment.sensor('ObjectSpaceCameraObserver')
  object_space_im = None
  if object_space:
    object_space_im = Image.open(object_space.observation_value)

  uvs = environment.sensor('UVsCameraObserver')
  uvs_im = None
  if uvs:
    uvs_im = Image.open(uvs.observation_value)

  tangents = environment.sensor('TangentsCameraObserver')
  tangents_im = None
  if tangents:
    tangents_im = Image.open(tangents.observation_value)

  return rgb_im, depth_im, segmentation_im, instance_segmentation_im, infrared_im, flow_im, normal_im, \
         satellite_im, object_space_im, uvs_im, tangents_im
