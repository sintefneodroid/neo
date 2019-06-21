#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from types import coroutine

from neodroid.interfaces.environment_models import EnvironmentDescription
from neodroid.interfaces.spaces import ActionSpace, ObservationSpace, SignalSpace
from neodroid.version import PROJECT_APP_PATH
from warg.app_path import AppPath

__author__ = 'cnheider'

import numpy as np


class Environment(ABC):

  def __init__(self,
               *,
               seed=8,
               logging_directory=PROJECT_APP_PATH.user_log,
               logging_level=logging.WARNING,
               **kwargs):
    self.seed(seed)

    logging.basicConfig(  # format='%(asctime)s %(new_state)s',
        # datefmt='%m/%d/%Y %I:%M:%S %p',
        filename=logging_directory / 'neodroid_log.txt',
        level=logging_level
        )
    # self._module_logger = logging.getLogger(__name__)

    self._description = None
    self._action_space = None
    self._observation_space = None

  @abstractmethod
  def configure(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def reset(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def react(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def display(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def describe(self, *args, **kwargs):
    raise NotImplementedError

  @property
  @abstractmethod
  def description(self) -> EnvironmentDescription:
    raise NotImplementedError

  @property
  @abstractmethod
  def observation_space(self) -> ObservationSpace:
    raise NotImplementedError

  @property
  @abstractmethod
  def action_space(self) -> ActionSpace:
    raise NotImplementedError

  @property
  @abstractmethod
  def signal_space(self) -> SignalSpace:
    raise NotImplementedError

  def __next__(self):
    state = self.react()
    while state:
      state = self.react()
      yield state
    while 1:
      raise StopIteration

  def __iter__(self):
    return self

  def __repr__(self):
    return (f'<Environment>\n'
      f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n'
      f'  <ActionSpace>{self.action_space}</ActionSpace>\n'
      f'  <Description>{self.description}</Description>\n'
      f'</Environment>')

  def __str__(self):
    return self.__repr__()

  @coroutine
  def coroutine_generator(self):
    '''
    :return:
    :rtype:
    '''
    return self

  @staticmethod
  def seed(seed):
    '''

:param seed:
:type seed:
'''
    np.random.seed(seed)
