#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.environments.unity_environment.deprecated.single_unity_environment import (
    SingleUnityEnvironment,
)

__author__ = "Christian Heider Nielsen"


class NeodroidALEWrapper(SingleUnityEnvironment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def act(
        self,
        input_reaction=None,
        on_step_done_callback=None,
        on_reaction_sent_callback=None,
    ):
        pass

    def reset_game(self, input_configuration=None):
        pass
