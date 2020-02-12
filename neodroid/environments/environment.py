#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from types import coroutine
from typing import Any

from neodroid import PROJECT_APP_PATH
from neodroid.utilities import EnvironmentSnapshot
from neodroid.utilities.spaces import ActionSpace, ObservationSpace, SignalSpace
from neodroid.utilities.unity_specifications.environment_description import (
    EnvironmentDescription,
)

__author__ = "Christian Heider Nielsen"

import numpy

from warg import drop_unused_kws

__all__ = ["Environment"]


class Environment(ABC):
    """
  Environment base class, this class is responsible for defining the interface of interaction. It is
  designed with the idea for constructing/connecting, configuring, resetting and reacting with an
  Environment as a Markov Decision Process(MDP). However can easily used as a stateless interface for
  collecting data, eg. from a real world camera, synthetic (Maybe domain randomised images) data or
  sampling consecutive data points (Maybe a time series of sensor values).
  """

    @drop_unused_kws
    def __init__(
        self,
        *,
        seed: int = 8,
        logging_directory: Path = PROJECT_APP_PATH.user_log,
        logging_level: Any = logging.WARNING,
        auto_reset_on_terminal_state: bool = True,
    ):
        self.seed(seed)

        logging.basicConfig(
            # format='%(asctime)s %(new_state)s',
            # datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=str(logging_directory / "neodroid_log.txt"),
            level=logging_level,
        )
        # self._module_logger = logging.getLogger(__name__)

        self._description = None
        self._auto_reset = auto_reset_on_terminal_state
        self._signal_space = None
        self._action_space = None
        self._observation_space = None
        self._environment_name = "NeodroidEnvironment"

    @property
    def environment_name(self) -> str:
        return self._environment_name

    @abstractmethod
    def configure(self, *args, **kwargs) -> EnvironmentSnapshot:
        raise NotImplementedError

    @abstractmethod
    def reset(self, *args, **kwargs) -> EnvironmentSnapshot:
        raise NotImplementedError

    @abstractmethod
    def react(self, *args, **kwargs) -> EnvironmentSnapshot:
        raise NotImplementedError

    @abstractmethod
    def display(self, *args, **kwargs) -> EnvironmentSnapshot:
        raise NotImplementedError

    @abstractmethod
    def describe(self, *args, **kwargs) -> EnvironmentSnapshot:
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
        return (
            f"<Environment>\n"
            f"  <ObservationSpace>{self.observation_space}</ObservationSpace>\n"
            f"  <ActionSpace>{self.action_space}</ActionSpace>\n"
            f"  <Description>{self.description}</Description>\n"
            f"</Environment>"
        )

    def __str__(self):
        return self.__repr__()

    @coroutine
    def coroutine_generator(self):
        """
:return:
:rtype:
"""
        return self

    def render(self):
        pass

    @staticmethod
    def seed(seed):
        """

:param seed:
:type seed:
"""
        numpy.random.seed(seed)
