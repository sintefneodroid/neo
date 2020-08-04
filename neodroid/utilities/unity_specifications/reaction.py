#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict, List, Optional, Sequence

from neodroid.utilities.unity_specifications.unobservables import Unobservables

__author__ = "Christian Heider Nielsen"

import json

from .reaction_parameters import ReactionParameters


class Reaction(object):
    """

  """

    def __init__(
        self,
        *,
        parameters: ReactionParameters = None,
        motions: Sequence = (),
        configurations: Sequence = (),
        unobservables: Unobservables = None,
        displayables: Sequence = None,
        environment_name: str = "None",
        serialised_message: str = "",
    ):
        """

The environment_name argument lets you specify which environments to react in, 'all' means all environment
receives the same reaction.

"""

        self._serialised_message = serialised_message
        self._environment_name = environment_name
        if not parameters:
            parameters = ReactionParameters()
        self._parameters = parameters
        self._configurations = configurations
        self._motions = motions
        self._unobservables = unobservables
        self._displayables = displayables

    @property
    def environment_name(self) -> str:
        """

    @return:
    @rtype:
    """
        return self._environment_name

    @property
    def parameters(self) -> ReactionParameters:
        """

    @return:
    @rtype:
    """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: ReactionParameters) -> None:
        self._parameters = parameters

    @property
    def motions(self) -> Sequence:
        """

    @return:
    @rtype:
    """
        return self._motions

    @motions.setter
    def motions(self, motions: Sequence) -> None:
        self._motions = motions

    @property
    def configurations(self) -> Sequence:
        """

    @return:
    @rtype:
    """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations: Sequence) -> None:
        self._configurations = configurations

    @property
    def displayables(self) -> Sequence:
        """

    @return:
    @rtype:
    """
        return self._displayables

    @displayables.setter
    def displayables(self, displayables: Sequence) -> None:
        self._displayables = displayables

    @property
    def unobservables(self) -> Optional[Unobservables]:
        """

    @return:
    @rtype:
    """
        return self._unobservables

    @unobservables.setter
    def unobservables(self, unobservables: Optional[Unobservables]):
        self._unobservables = unobservables

    @property
    def string_serialised_message(self) -> str:
        """

    @return:
    @rtype:
    """
        return self._serialised_message

    @string_serialised_message.setter
    def string_serialised_message(self, message: str) -> None:
        self._serialised_message = message

    def to_dict(self) -> Dict[str, List]:
        """

    @return:
    @rtype:
    """
        return {
            "_configurations": [
                configuration.to_dict() for configuration in self._configurations
            ],
            "_motions": [motion.to_dict() for motion in self._motions],
        }

    def to_json(self) -> str:
        """

    @return:
    @rtype:
    """
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        return (
            f"<Reaction>\n"
            f"<environment_name>{self.environment_name}</environment_name>\n"
            f"<configurations>\n{self.configurations}</configurations>\n"
            f"<motions>\n{self.motions}</motions>\n"
            f"<parameters>\n{self.parameters}</parameters>\n"
            f"<configurations>\n{self.configurations}</configurations>\n"
            f"<displayables>\n{self.displayables}</displayables>\n"
            f"<unobservables>\n{self.unobservables}</unobservables>\n"
            f"<serialised_message>{self.string_serialised_message}</serialised_message>\n"
            f"</Reaction>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
