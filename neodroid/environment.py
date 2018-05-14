#!/usr/bin/env python3
# coding=utf-8
import logging
import os
from abc import abstractmethod, ABC
from types import coroutine

__author__ = 'cnheider'

import numpy as np


class Environment(ABC):

  def __init__(self,
               *,
               seed=8,
               debug_logging=False,
               logging_directory='logs',
               verbose=False,
               **kwargs):
    self.seed(seed)
    self._verbose = verbose

    self._debug_logging = debug_logging
    if self._debug_logging:
      logging.basicConfig(
          format='%(asctime)s %(new_state)s',
          filename=os.path.join(logging_directory, 'neodroid-log.txt'),
          level=logging.DEBUG,
          )
      self._logger = logging.getLogger(__name__)
      self._logger.debug('Initializing Environment')

  @abstractmethod
  def _close(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def _configure(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def _reset(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def _react(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def _observe(self, *args, **kwargs):
    raise NotImplementedError

  @abstractmethod
  def _display(self, *args, **kwargs):
    raise NotImplementedError

  @property
  @abstractmethod
  def description(self):
    return NotImplementedError

  @property
  @abstractmethod
  def observation_space(self):
    return NotImplementedError

  @property
  @abstractmethod
  def action_space(self):
    return NotImplementedError

  @property
  @abstractmethod
  def signal_space(self):
    return NotImplementedError

  def __next__(self):
    return self._react()

  def __iter__(self):
    return self

  def __str__(self):
    return f'<Environment>\n' \
           f'  <ObservationSpace>{self.observation_space}</ObservationSpace>\n' \
           f'  <ActionSpace>{self.action_space}</ActionSpace>\n' \
           f'  <Description>{self.description}</Description>\n' \
           f'</Environment>'

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
