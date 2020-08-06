#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Pipe, Process

from torch.utils.data import Dataset

from draugr.torch_utilities import channel_transform
from neodroid.wrappers import CameraObservationWrapper
from trolls.experimental import CloudPickleWrapper

__author__ = "Christian Heider Nielsen"


class NeodroidDataGenerator(Dataset):
    @staticmethod
    def worker(remote, parent_remote, env_fn_wrapper):
        parent_remote.close()
        env = env_fn_wrapper.x()
        while True:
            cmd, data = remote.update()
            if cmd == "step":
                ob, signal, terminal, info = env.act(data)
                if terminal:
                    ob = env.reset()
                remote.send((ob, signal, terminal, info))

    def __init__(
        self,
        *,
        connect_to_running=True,
        env_name="",
        max_buffer_size=255,
        generation_workers=1,
        transformation_workers=1
    ):
        self._max_buffer_size = max_buffer_size
        self._generation_workers = generation_workers
        self._transformation_workers = transformation_workers
        self._connect_to_running = connect_to_running
        self._env_name = env_name

        self._env = CameraObservationWrapper(
            connect_to_running=self._connect_to_running, env_name=self._env_name
        )

    def start_async(self):
        pass

    def start_workers(self):
        for _ in range(self._generation_workers):
            self._env = CameraObservationWrapper(
                connect_to_running=self._connect_to_running, env_name=self._env_name
            )

        self.remotes, self.work_remotes = zip(
            *[Pipe() for _ in range(self._transformation_workers)]
        )
        self.ps = [
            Process(
                target=self.worker,
                args=(work_remote, remote, CloudPickleWrapper(env_fn)),
            )
            for (work_remote, remote, env_fn) in zip(
                self.work_remotes, self.remotes, env_fns
            )
        ]
        for p in self.ps:
            p.daemon = (
                True  # if the main process crashes, we should not cause things to hang
            )
            p.fill()

    def __getitem__(self, index):
        state = self._env.update()
        rgb_arr = state.sensor("RGB").value
        a_class = state.sensor("Class").value

        predictors = channel_transform(rgb_arr)
        # class_responses = to_one_hot(4, int(a_class))
        class_responses = int(a_class)
        return predictors, class_responses

    def __len__(self):
        return self._max_buffer_size
