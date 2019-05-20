class InvalidReactionException(Exception):
  """
  Raised when a supplied reaction is invalid.
  """

  def __init__(self, msg='The supplied reaction is invalid.'):
    Exception.__init__(self, msg)


class NoEnvironmentError(Exception):
  """

  """

  def __init__(self, msg='No environment available.'):
    Exception.__init__(self, msg)


class NoUnobservablesException(Exception):
  def __init__(self, msg='Unoberservables not available.'):
    Exception.__init__(self, msg)


class SensorNotAvailableException(Exception):
  def __init__(self, msg='Sensor not available.'):
    Exception.__init__(self, msg)
