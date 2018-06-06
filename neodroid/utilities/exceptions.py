class InvalidReactionException(Exception):
  """
  Raised when a supplied reaction is invalid.
  """

  def __init__(self):
    msg = 'The supplied reaction is invalid.'
    Exception.__init__(self, msg)