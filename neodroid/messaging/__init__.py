#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import logging
from enum import Enum
from functools import wraps

from sorcery import assigned_names


class ClientEventsEnum(Enum):
    (connected, disconnected, timeout, reconnected) = assigned_names()


def message_client_event(event):
    def receive_func(func):
        @wraps(func)
        def call_func(ctx, *args, **kwargs):
            if event is ClientEventsEnum.connected:
                logging.info("Connected to server")
            elif event is ClientEventsEnum.disconnected:
                logging.info("Disconnected from server")
            elif event is ClientEventsEnum.reconnected:
                logging.info("Reconnected to server")
            elif event is ClientEventsEnum.timeout:
                logging.warning("Connection timeout")
            return func(ctx, *args, **kwargs)

        return call_func

    return receive_func
