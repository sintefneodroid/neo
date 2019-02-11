#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod

from neodroid.models.range import Range

__author__ = 'cnheider'


class Space():


  @property
  @abstractmethod
  def ranges(self):
    raise NotImplemented

  def __repr__(self):
    ranges_str = ''.join([str(range.__repr__()) for range in self.ranges])

    return (f'<Space>\n'
            f'<Ranges>\n{ranges_str}</Ranges>\n'
            f'</Space>\n')

