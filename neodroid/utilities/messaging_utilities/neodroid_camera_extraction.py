from io import BytesIO

import PIL
import imageio
import numpy
from PIL import Image
from skimage import io

default_camera_observer_names = ('90',
                                 '180',
                                 '270',
                                 '360'
                                 'Material',
                                 'WorldSpace',
                                 'Us',
                                 'Vs',
                                 'UVs',
                                 'Offset',
                                 'Depth',
                                 'RGB',
                                 'ObjectSpace',
                                 'Instance',
                                 'CompressedDepth',
                                 'Infrared',
                                 'Normal',
                                 'Tangents',
                                 'Flow',
                                 'Layer',
                                 'Tag',
                                 'Satellite')


def extract_neodroid_camera(state, cameras=default_camera_observer_names, image_size=(224,224,4)):
  out = dict()

  for camera in cameras:
    res = extract_camera_observation(state, camera,image_size=image_size)
    if res is not None:
      out[camera] = res

  return out


def extract_camera_observation(state, key, image_size=(224,224,4), d_type=numpy.float32):
  sensor = state.observer(key)
  if sensor:
    val = sensor.observation_value
    if isinstance(val, (bytes,BytesIO)):
      img = imageio.imread(val)
    else:
      img = numpy.array(val, dtype=d_type).reshape(*image_size)
      img = numpy.flipud(img)
      #img = numpy.nan_to_num(img)

      #img = Image.fromarray(img, mode='RGBA').transpose(PIL.Image.FLIP_TOP_BOTTOM)

    return img
  return None
