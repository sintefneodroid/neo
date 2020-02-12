#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 20/01/2020
           """

from typing import Sequence, Any

import numpy
import torch
from torch import Tensor


def non_terminal_mask(terminal: Any) -> Any:
    """

  @param terminal:
  @return:
  """
    if isinstance(terminal, bool):
        return not terminal
    if isinstance(terminal, (numpy.ndarray, Sequence)):
        if isinstance(terminal[0], Tensor):
            return [1 - t for t in terminal]
        return [numpy.invert(t) for t in terminal]
    elif isinstance(terminal, Tensor):
        return 1 - terminal
    return numpy.invert(terminal)


def non_terminal_numerical_mask(terminal: Any) -> Any:
    """

  @param terminal:
  @return:
  """
    if isinstance(terminal, bool):
        return 0 if terminal else 1
    if isinstance(terminal, tuple):
        if isinstance(terminal[0], Tensor):
            return [(1 - t).type(torch.uint8) for t in terminal]
        return [numpy.invert(t).astype(numpy.uint8) for t in terminal]
    elif isinstance(terminal, Tensor):
        return (1 - terminal).type(torch.uint8)
    return numpy.invert(terminal).astype(numpy.uint8)


if __name__ == "__main__":
    a = [False] * 3 + [True, False]

    print(non_terminal_mask(a))
    print(non_terminal_numerical_mask(a))
