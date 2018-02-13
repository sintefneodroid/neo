from functools import wraps
import warnings

from enum import Enum
#from enum import auto

class ClientEvents(Enum):
   CONNECTED = 1#auto()
   DISCONNECTED =2# auto()
   TIMEOUT = 3#auto()


def debug_print(msg='empty debug message'):
  print(msg)

def message_client_event(event):
  def receive_f(f):
    @wraps(f)
    def call_f(ctx, *args, **kwds):
      if event is ClientEvents.CONNECTED:
        warnings.warn('Connected to server')
      elif event is ClientEvents.DISCONNECTED:
        warnings.warn('Disconnected from server')
      elif event is ClientEvents.TIMEOUT:
        warnings.warn('Connection timeout')
      return f(ctx, *args, **kwds)
    return call_f
  return receive_f