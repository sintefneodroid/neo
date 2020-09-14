#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.environments.droid_environment.deprecated.single_unity_environment import (
    SingleUnityEnvironment,
)

__author__ = "Christian Heider Nielsen"


class NeodroidFormalWrapper(SingleUnityEnvironment):
    def __next__(self):
        if not self._is_connected_to_server:
            return
        return self.act(None)

    def act(self, input_reaction, **kwargs):
        message = super().react(in_reaction=input_reaction, **kwargs)
        first_environment = message
        if first_environment:
            return (
                first_environment.observables,
                first_environment.signal,
                first_environment.terminated,
                first_environment,
            )
        raise ValueError("Did not receive any message.")

    def step(self, input_reaction, **kwargs):
        return self.act(input_reaction, **kwargs)

    def realise(self):
        pass

    def observer(self, key):
        if self._last_snapshots:
            return self.sensor(key)
        warn("No message available")
        return None

    def configure(self, *args, **kwargs):
        message = super().reset(*args, **kwargs)
        if message:
            return message.observables, message
        return None, None

    def observe(self, *args, **kwargs):
        message = super().observe(*args, **kwargs)
        if message:
            return (message.observables, message.signal, message.terminated, message)
        return None, None, None, None

    def quit(self, *args, **kwargs):
        return self.close(*args, **kwargs)
