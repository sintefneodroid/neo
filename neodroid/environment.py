#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
from abc import ABC, abstractmethod
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


  def configure(self, *args, **kwargs):
    return self._configure(*args, **kwargs)

  def reset(self, *args, **kwargs):
    return self._reset(*args, **kwargs)

  def react(self, *args, **kwargs):
    return self._react(*args, **kwargs)

  def observe(self, *args, **kwargs):
    return self._describe(*args, **kwargs)

  def display(self, *args, **kwargs):
    return self._display(*args, **kwargs)

  def describe(self, *args, **kwargs):
    self._describe(*args, **kwargs)

  def is_solved(self, *args, **kwargs):
    return self._is_solved()

  def _is_solved(self, *args, **kwargs):
    raise False



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
  def _describe(self, *args, **kwargs):
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

  def sample_action(self):
    return self.action_space.sample()

  def __next__(self):
    state = self._react()
    while state:
      state = self._react()
      yield state
    while 1:
      raise StopIteration

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
