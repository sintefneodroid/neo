import numpy as np
from PIL import Image


def extract_neodroid_camera(state):
  rgb_im = extract_camera_observation(state, 'RGBCameraObserver')

  seg_im = extract_camera_observation(state, 'SegmentationCameraObserver')

  instance_seg_im = extract_camera_observation(state, 'InstanceSegmentationCameraObserver')

  depth_im = extract_camera_observation(state, 'DepthCameraObserver')

  infrared_im = extract_camera_observation(state, 'InfraredCameraObserver')

  normal_im = extract_camera_observation(state, 'NormalCameraObserver')

  flow_im = extract_camera_observation(state, 'FlowCameraObserver')

  sat_im = extract_camera_observation(state, 'SatelliteCameraObserver')

  return rgb_im, seg_im, instance_seg_im, depth_im, infrared_im, normal_im, flow_im, sat_im


def extract_camera_observation(state, str):
  sat = state.observer(str)
  if sat:
    sat_im = Image.open(sat.observation_value)
    sat_im = sat_im.convert('RGB')
    sat_im = np.asarray(sat_im)

    return sat_im
  return None