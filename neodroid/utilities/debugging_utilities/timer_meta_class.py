import types
import time


class Timer:
  def __init__(self, func=time.perf_counter):
    self.elapsed = 0.0
    self._func = func
    self._start = None

  def start(self):
    if self._start is not None:
      raise RuntimeError('Already started')
    self._start = self._func()

  def stop(self):
    if self._start is None:
      raise RuntimeError('Not started')
    end = self._func()
    self.elapsed += end - self._start
    self._start = None

  def reset(self):
    self.elapsed = 0.0

  @property
  def running(self):
    return self._start is not None

  def __enter__(self):
    self.start()
    return self

  def __exit__(self, *args):
    self.stop()


# Below, we create the Timed metaclass that times its classes' methods
# along with the setup functions that rewrite the class methods at
# class creation times


# Function that times execution of a passed in function, returns a new function
# encapsulating the behavior of the original function
def time_func(fn, *args, **kwargs):
  def fn_composite(*args, **kwargs):
    timer = Timer()
    timer.start()
    rt = fn(*args, **kwargs)
    timer.stop()
    print("Executing %s took %s seconds." % (fn.__name__, timer.elapsed))
    return rt

  # return the composite function
  return fn_composite


# The 'Timed' metaclass that replaces methods of its classes
# with new methods 'timed' by the behavior of the composite function transformer
class Timed(type):

  def __new__(cls, name, bases, attr):
    # replace each function with
    # a new function that is timed
    # run the computation with the provided args and return the computation result
    for name, value in attr.items():
      if isinstance(value, types.FunctionType) or isinstance(value, types.MethodType):
        attr[name] = time_func(value)

    return super(Timed, cls).__new__(cls, name, bases, attr)


if __name__ == '__main__':
  class Math(metaclass=Timed):

    def multiply(self, a, b):
      product = a * b
      print(product)
      return product


  Math().multiply(5, 6)
