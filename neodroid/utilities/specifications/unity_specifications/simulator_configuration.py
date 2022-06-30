#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

from warg import cached_property

from neodroid.messaging.fbs import FConfiguration

__all__ = ["SimulatorConfiguration"]


class SimulatorConfiguration(object):
    """ """

    def __init__(
        self,
        fbs_configuration: FConfiguration,
        api_version: bytes,
        simulator_info: str = "No simulator_info available",
    ):
        """

        :param fbs_configuration:
        :param api_version:
        :param simulator_info:"""
        self._fbs_configuration = fbs_configuration
        self._api_version = api_version
        self._simulator_info = simulator_info

    @property
    def simulator_configuration(self):
        """

        :return:
        :rtype:
        """
        return self._fbs_configuration

    @cached_property
    def api_version(self) -> str:
        """

        :return:
        :rtype:
        """
        return self._api_version.decode()

    @property
    def simulator_info(self) -> str:
        """

        :return:
        :rtype:
        """
        # if not isinstance(self._simulator_info, str):
        #  return self._simulator_info.decode()
        return self._simulator_info
