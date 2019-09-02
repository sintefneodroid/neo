import numpy

from .camera_observation_wrapper import CameraObservationWrapper
from .observation_wrapper import ObservationWrapper


def make(environment_name, **kwargs):
  return CameraObservationWrapper(environment_name=environment_name, **kwargs)


def connect():
  return CameraObservationWrapper(connect_to_running=True)


def seed(s):
  numpy.random.random(s)
