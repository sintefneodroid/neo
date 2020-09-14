import time

import neodroid

__all__ = [
    "default_camera_observer_names",
    "extract_all_cameras",
    "extract_camera_observation",
    "extract_from_cameras",
]

default_camera_observer_names = (
    "Material",
    "WorldSpace",
    "Us",
    "Vs",
    "UVs",
    "Offset",
    "Depth",
    "RGB",
    "ObjectSpace",
    "Instance",
    "CompressedDepth",
    "Infrared",
    "Normal",
    "Tangents",
    "Flow",
    "Layer",
    "OcclusionMask",
    "Tag",
    "Diffuse",
    "Satellite",
)


def extract_from_cameras(state, cameras=default_camera_observer_names):
    """

  @param state:
  @type state:
  @param cameras:
  @type cameras:
  @return:
  @rtype:
  """
    out = dict()

    for camera in cameras:
        res = extract_camera_observation(state, camera)
        if res is not None:
            out[camera] = res

    return out


def extract_all_cameras(state):
    """

  @param state:
  @type state:
  @return:
  @rtype:
  """
    out = dict()

    for camera in state.sensors.keys():
        res = extract_camera_observation(state, camera)
        if res is not None:
            out[camera] = res

    return out


def extract_camera_observation(state, key):
    """

  @param state:
  @type state:
  @param key:
  @type key:
  @return:
  @rtype:
  """
    sensor = state.sensor(key)
    if sensor and sensor.is_image:
        img = sensor.value
        return img
    """
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
"""
    return None


if __name__ == "__main__":

    environments = neodroid.connect()
    environments.reset()

    i = 0
    freq = 100
    time_s = time.time()
    while environments.is_connected:
        states = environments.react()
        state = next(iter(states.values()))
        extract_all_cameras(state)
        terminated = state.terminated

        if terminated:
            environments.reset()
