#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Iterable

__author__ = 'cnheider'

import numpy as np


def signed_ternary_encoding(*,
                            size: int,
                            index):
  # assert isinstance(size,(int,numpy.int64)), f'size was {type(size)}'
  # assert isinstance(index,(int,numpy.int64)), f'index was {type(index)}'
  # assert size*2 > index, f'signed size was {size*2}, index was {index}'

  if not isinstance(index, Iterable):
    index = [index]
  acs = []
  for i in index:
    a = np.zeros(size)
    if i < 0:
      return a
    elif 0 <= i < size:
      a[i] = 1
    elif size <= i < size * 2:
      a[i - size] = -1
    acs.append(a)
  return acs


def to_one_hot(dims, index):
  if not isinstance(index, Iterable):
    index = [index]
  acs = []
  for i in index:
    if isinstance(i, np.int) or isinstance(i, np.int64) or isinstance(i, int):
      one_hot = np.zeros(dims)
      one_hot[i] = 1.
    else:
      one_hot = np.zeros((len(i), dims))
      one_hot[np.arange(len(i)), i] = 1.
    acs.append(one_hot)

  return acs


def agg_double_list(l):
  # l: [ [...], [...], [...] ]
  # l_i: result of each step in the i-th episode
  s = [np.sum(np.array(l_i), 0) for l_i in l]
  s_mu = np.mean(np.array(s), 0)
  s_std = np.std(np.array(s), 0)
  return s_mu, s_std


if __name__ == '__main__':
  a_size = 4
  a_index = -1
  print(signed_ternary_encoding(size=a_size, index=a_index))
