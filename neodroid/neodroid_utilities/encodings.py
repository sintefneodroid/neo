#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import numpy as np


def signed_ternary_encoding(*,
                            size: int,
                            index:int):
  assert isinstance(size,int), f'size was {type(size)}'
  assert isinstance(index,int), f'index was {type(index)}'
  assert size*2 > index, f'signed size was {size*2}, index was {index}'

  a = np.zeros(size)
  if index < 0:
    return a
  elif 0 <= index < size:
    a[index] = 1
  elif size <= index < size*2:
    a[index - size] = -1
  return a


def to_one_hot(dims, index):
  if isinstance(index, np.int) or isinstance(index, np.int64) or isinstance(index, int):
    one_hot = np.zeros(dims)
    one_hot[index] = 1.
  else:
    one_hot = np.zeros((len(index), dims))
    one_hot[np.arange(len(index)), index] = 1.
  return one_hot


def agg_double_list(l):
  # l: [ [...], [...], [...] ]
  # l_i: result of each step in the i-th episode
  s = [np.sum(np.array(l_i), 0) for l_i in l]
  s_mu = np.mean(np.array(s), 0)
  s_std = np.std(np.array(s), 0)
  return s_mu, s_std


if __name__ == '__main__':
  size = 4
  index = -1
  print(signed_ternary_encoding(size=size,index=index))