#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import warnings
from enum import Enum
from functools import wraps


# from enum import auto

class ClientEvents(Enum):
  CONNECTED = 1  # auto()
  DISCONNECTED = 2  # auto()
  TIMEOUT = 3  # auto()


def debug_print(msg='empty debug message'):
  print(msg)


def print_return(f):
    @wraps(f)
    def call_f(*args, **kwargs):
      call_return = f(*args, **kwargs)
      if 'verbose' in kwargs and kwargs['verbose']:
        print(call_return)
      return call_return

    return call_f

def message_client_event(event):
  def receive_f(f):
    @wraps(f)
    def call_f(ctx, *args, **kwargs):
      if event is ClientEvents.CONNECTED:
        warnings.warn('Connected to server')
      elif event is ClientEvents.DISCONNECTED:
        warnings.warn('Disconnected from server')
      elif event is ClientEvents.TIMEOUT:
        warnings.warn('Connection timeout')
      return f(ctx, *args, **kwargs)

    return call_f

  return receive_f
