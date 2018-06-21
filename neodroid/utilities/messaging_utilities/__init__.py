from enum import Enum
from functools import wraps
from warnings import warn


class ClientEvents(Enum):
  CONNECTED = 1  # auto()
  DISCONNECTED = 2  # auto()
  TIMEOUT = 3  # auto()


def message_client_event(event):
  def receive_func(func):

    @wraps(func)
    def call_func(ctx, *args, **kwargs):
      if event is ClientEvents.CONNECTED:
        warn('Connected to server')
      elif event is ClientEvents.DISCONNECTED:
        warn('Disconnected from server')
      elif event is ClientEvents.TIMEOUT:
        warn('Connection timeout')
      return func(ctx, *args, **kwargs)

    return call_func

  return receive_func
