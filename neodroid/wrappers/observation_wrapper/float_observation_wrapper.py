#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from warnings import warn

from neodroid.environments.unity_environment import SingleUnityEnvironment

__author__ = "Christian Heider Nielsen"


class FloatObservationWrapper(SingleUnityEnvironment):
    def __next__(self):
        if not self._is_connected_to_server:
            return
        return self.fetch_new_frame(None)

    def randomise(self, input_reaction, **kwargs):
        return self.fetch_new_frame(input_reaction, **kwargs)

    def observer(self, key):
        if self._last_snapshots:
            return self._sensor(key)
        warn("No message available")
        return None

    def configure(self, *args, **kwargs):
        message = super().reset(*args, **kwargs)
        if message:
            return message.observables, message
        return None, None

    def fetch_new_frame(self, *args, **kwargs):
        message = super().observe(*args, **kwargs)
        if message:
            return (message.observables, message.signal, message.terminated, message)
        return None, None, None, None

    def quit(self, *args, **kwargs):
        return self.close(*args, **kwargs)
