#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

__author__ = "Christian Heider Nielsen"

import json


class ReactionParameters(object):
    def __init__(
        self,
        *,
        terminable: bool = False,
        step: bool = False,
        reset: bool = False,
        configure: bool = False,
        describe: bool = True,
        episode_count: bool = False,
    ):
        self._terminable = terminable
        self._configure = configure
        self._step = step
        if reset:
            logging.info("resetting")
        self._reset = reset
        self._describe = describe
        self._episode_count = episode_count

    @property
    def reset(self) -> bool:
        return self._reset

    @property
    def configure(self) -> bool:
        return self._configure

    @property
    def describe(self) -> bool:
        return self._describe

    @property
    def step(self) -> bool:
        return self._step

    @property
    def episode_count(self) -> bool:
        return self._episode_count

    @property
    def terminable(self) -> bool:
        return self._terminable

    @reset.setter
    def reset(self, value: bool) -> None:
        self._reset = value

    def to_dict(self) -> dict:
        return {"_reset": self._reset}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __repr__(self):
        return (
            f"<ReactionParameters>\n"
            f"<terminable>{self._terminable}</terminable>\n"
            f"<step>{self._step}</step>\n"
            f"<reset>{self._reset}</reset>\n"
            f"<configure>{self._configure}</configure>\n"
            f"<describe>{self._describe}</describe>\n"
            f"<episode_count>{self._episode_count}</episode_count>\n"
            f"</ReactionParameters>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
