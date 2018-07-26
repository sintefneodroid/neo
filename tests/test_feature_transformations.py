import pytest
from neodroid import utilities, Space


def inc(x):
  return x + 1


def test_answer():
  assert inc(3) == 5

@pytest.mark.slow
def test_space():
  space = Space(1,-1,1)
  assert space.min_value != 0