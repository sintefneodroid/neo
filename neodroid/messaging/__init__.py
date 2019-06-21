#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import logging
from enum import Enum, auto
from functools import wraps

from neodroid.messaging.fbs.fbs_reaction_utilities import *
from neodroid.messaging.fbs.fbs_state_utilties import *
from .message_client import MessageClient


class ClientEvents(Enum):
  CONNECTED = auto()
  DISCONNECTED = auto()
  TIMEOUT = auto()


def message_client_event(event):
  def receive_func(func):

    @wraps(func)
    def call_func(ctx, *args, **kwargs):
      if event is ClientEvents.CONNECTED:
        logging.info('Connected to server')
      elif event is ClientEvents.DISCONNECTED:
        logging.info('Disconnected from server')
      elif event is ClientEvents.TIMEOUT:
        logging.warning('Connection timeout')
      return func(ctx, *args, **kwargs)

    return call_func

  return receive_func
