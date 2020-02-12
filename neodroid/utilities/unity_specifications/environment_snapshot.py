#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable, Sequence, Iterable, Mapping, TypeVar, List

from neodroid.messaging.fbs.FBSModels.FState import FState
from neodroid.messaging.fbs.fbs_state_utilties import (
    deserialise_description,
    deserialise_observables,
    deserialise_unobservables,
)

__author__ = "Christian Heider Nielsen"

from .sensor import Sensor
from .configurable import Configurable
from .environment_description import EnvironmentDescription

EnvironmentSnapshotType = TypeVar(
    "EnvironmentSnapshotType", bound="EnvironmentSnapshot"
)


class EnvironmentSnapshot(object):
    def __init__(self, fbs_state: FState = None):
        self._fbs_state = fbs_state

    def _environment_name(self) -> str:
        if self._fbs_state:
            return self._fbs_state.EnvironmentName()

    @property
    def environment_name(self) -> str:
        if isinstance(self._environment_name, Callable):
            self._environment_name = self._environment_name()
        return self._environment_name

    def _signal(self) -> float:
        if self._fbs_state:
            return self._fbs_state.Signal()

    @property
    def signal(self) -> float:
        if isinstance(self._signal, Callable):
            self._signal = self._signal()
        return self._signal

    def _observables(self) -> List[float]:
        if self._fbs_state:
            return deserialise_observables(self._fbs_state)

    @property
    def observables(self) -> List[float]:
        if isinstance(self._observables, Callable):
            self._observables = self._observables()
        return self._observables

    def _unobservables(self) -> List[float]:
        if self._fbs_state:
            return deserialise_unobservables(self._fbs_state)

    @property
    def unobservables(self) -> List[float]:
        if isinstance(self._unobservables, Callable):
            self._unobservables = self._unobservables()
        return self._unobservables

    def _frame_number(self) -> int:
        if self._fbs_state:
            return self._fbs_state.FrameNumber()

    @property
    def frame_number(self) -> int:
        if isinstance(self._frame_number, Callable):
            self._frame_number = self._frame_number()
        return self._frame_number

    def _terminated(self) -> bool:
        if self._fbs_state:
            return self._fbs_state.Terminated()

    @property
    def terminated(self) -> bool:
        if isinstance(self._terminated, Callable):
            self._terminated = self._terminated()
        return self._terminated

    def _termination_reason(self) -> str:
        if self._fbs_state:
            return self._fbs_state.TerminationReason().decode()

    @property
    def termination_reason(self) -> str:
        if isinstance(self._termination_reason, Callable):
            self._termination_reason = self._termination_reason()
        return self._termination_reason

    def _extra_serialised_message(self) -> str:
        if self._fbs_state:
            return self._fbs_state.ExtraSerialisedMessage().decode()

    @property
    def extra_serialised_message(self) -> str:
        if isinstance(self._extra_serialised_message, Callable):
            self._extra_serialised_message = self._extra_serialised_message()
        return self._extra_serialised_message

    @property
    def description(self) -> EnvironmentDescription:
        if self._fbs_state:
            if self._fbs_state.EnvironmentDescription():
                return deserialise_description(self._fbs_state.EnvironmentDescription())

    @property
    def sensors(self) -> Mapping[str, Sensor]:
        if self.description:
            return self.description.sensors

    def sensor(self, key) -> Sensor:
        if self.description:
            return self.description.sensor(key)

    @property
    def configurables(self) -> Mapping[str, Configurable]:
        if self.description:
            return self.description.configurables

    def configurable(self, key) -> Configurable:
        if self.description:
            return self.description.configurable(key)

    def to_gym_like_output(self) -> tuple:
        return self.observables, self.signal, self.terminated, self

    @staticmethod
    def from_gym(
        environment_name, observables, signal, terminated, info=None
    ) -> EnvironmentSnapshotType:
        snapshot = EnvironmentSnapshot(None)
        snapshot._environment_name = environment_name
        snapshot._environment_name = ""
        snapshot._observables = observables
        snapshot._signal = signal
        snapshot._terminated = terminated
        snapshot._extra_serialised_message = info
        snapshot._unobservables = []
        snapshot._frame_number = 0
        snapshot._termination_reason = ""
        return snapshot

    def to_dict(self) -> dict:
        # inspect.getmembers(a)
        return dict(vars(self))

    def to_json(self) -> object:
        import json

        encoder = json.JSONEncoder()
        return encoder.encode(self.to_dict())

    def __repr__(self) -> str:
        return (
            f"<EnvironmentSnapshot>\n"
            f"<frame_number>{self.frame_number}</frame_number>\n"
            f"<signal>{self.signal}</signal>\n"
            f"<terminated>{self.terminated}</terminated>\n"
            f"{self.description}\n"
            f"{self.unobservables}\n"
            f"</EnvironmentSnapshot>\n"
        )

    def __str__(self) -> str:
        return self.__repr__()

    def __unicode__(self) -> str:
        return self.__repr__()


if __name__ == "__main__":
    es = EnvironmentSnapshot.from_gym([0, 2, 1], 0, terminated=False, info=None)
    print(es.to_json())
