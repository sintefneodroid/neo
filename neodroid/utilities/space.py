#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'


class Space(object):

  def __init__(self, **kwargs):
    pass

  def sample(self):
    raise NotImplementedError

  def flat_size(self):
    raise NotImplementedError

  def size(self):
    raise NotImplementedError
