#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from draugr import generator_batch
from neodroid.environments.unity_environment import SingleUnityEnvironment
from neodroid.exceptions.exceptions import SensorNotAvailableException
from neodroid.utilities.unity_specifications.prefabs.neodroid_camera_extraction import (
    extract_neodroid_camera,
)

__author__ = "Christian Heider Nielsen"


class MixedObservationWrapper(SingleUnityEnvironment):
    def __init__(self, auto_reset=True, reset_always=True, **kwargs):
        super().__init__(**kwargs)
        self._auto_reset = auto_reset
        self.reset_always = reset_always

        self.reset()

    def __next__(self):
        if not self._is_connected_to_server:
            return
        return self.fetch_new_frame(None)

    def update(self):
        return super().react()

    def fetch_new_frame(self, *args, **kwargs):
        if not self.reset_always:
            message = super().react(*args, **kwargs)
            if message.terminated and self._auto_reset:
                super().reset()
                message = self.fetch_new_frame()
        else:
            message = self.reset()

        if message:
            return [
                *extract_neodroid_camera(message).values(),
                message.sensor("Class").value,
            ]
        return None


if __name__ == "__main__":
    env = MixedObservationWrapper()
    data_iter = generator_batch(iter(env), 3)

    for a in data_iter:
        print(a)
        break
