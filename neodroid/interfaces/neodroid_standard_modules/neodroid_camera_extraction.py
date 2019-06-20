import time

import neodroid

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
                                 'OcclusionMask',
                                 'Tag',
                                 'Satellite')


def extract_neodroid_camera(state, cameras=default_camera_observer_names):
  out = dict()

  for camera in cameras:
    res = extract_camera_observation(state, camera)
    if res is not None:
      out[camera] = res

  return out


def extract_all_as_camera(state):
  out = dict()

  for camera in state.sensors.keys():
    res = extract_camera_observation(state, camera)
    if res is not None:
      out[camera] = res

  return out


def extract_camera_observation(state,
                               key):
  sensor = state.sensor(key)
  if sensor:
    img = sensor.value
    return img
  '''
  if isinstance(img, (bytes, BytesIO)):
    img = img#imageio.imread(img)
  else:
    if image_size[0] is None or image_size[1] is None:
      # TODO: support inference of only one dimension based on knowns
      symmetric_size = int(math.sqrt((len(img) / image_size[-1])))
      image_size = list(image_size)
      image_size[0] = image_size[1] = symmetric_size

    img = numpy.array(img, dtype=d_type).reshape(*image_size)
    img = numpy.flipud(img)
    # img = numpy.nan_to_num(img)

    # img = Image.fromarray(img, mode='RGBA').transpose(PIL.Image.FLIP_TOP_BOTTOM)

    return img
  '''
  return None


if __name__ == '__main__':

  environments = neodroid.connect()
  environments.reset()

  i = 0
  freq = 100
  time_s = time.time()
  while environments.is_connected:
    actions = environments.action_space._sample()
    states = environments.react(actions)
    state = next(iter(states.values()))
    extract_all_as_camera(state)
    terminated = state.terminated

    if terminated:
      environments.reset()
