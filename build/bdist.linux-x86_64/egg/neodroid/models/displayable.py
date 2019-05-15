#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'


# @pretty_print
class Displayable(object):

  def __init__(self, displayable_name, displayable_value):
    self._displayable_name = displayable_name
    self._displayable_value = displayable_value

  @property
  def displayable_name(self):
    return self._displayable_name

  @property
  def displayable_value(self):
    return self._displayable_value

  def to_dict(self):
    return {
      '_displayable_name': self._displayable_name,
      '_displayable_value':self._displayable_value,
      }

  def __repr__(self):
    return (
      f'<Displayable>\n'
      f'<displayable_name>{self._displayable_name}</displayable_name>\n'
      f'<displayable_value>\n{self._displayable_value}</displayable_value>\n'
      f'</Displayable>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
