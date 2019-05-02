import numpy as np
from PIL import Image

default_camera_observer_names = ('RGBCameraObserver',
                                 'SegmentationCameraObserver',
                                 'InstanceSegmentationCameraObserver',
                                 'DepthCameraObserver',
                                 'InfraredCameraObserver',
                                 'NormalCameraObserver',
                                 'FlowCameraObserver',
                                 'LayerSegmentationCameraObserver',
                                 'TagSegmentationCameraObserver',
                                 'SatelliteCameraObserver')


def extract_neodroid_camera(state, cameras=default_camera_observer_names):
  out = dict()

  for camera in cameras:
    res = extract_camera_observation(state, camera)
    if res is not None:
      out[camera] = res

  return out


def extract_camera_observation(state, str):
  sat = state.observer(str)
  if sat:
    sat_im = Image.open(sat.observation_value)
    sat_im = sat_im.convert('RGB')
    sat_im = np.asarray(sat_im)

    return sat_im
  return None
