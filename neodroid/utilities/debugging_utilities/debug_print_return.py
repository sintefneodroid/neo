from functools import wraps


def print_return_value(f: callable) -> callable:
  @wraps(f)
  def call_f(*args, **kwargs):
    call_return = f(*args, **kwargs)
    if 'verbose' in kwargs and kwargs['verbose']:
      print(call_return)
    return call_return

  return call_f
