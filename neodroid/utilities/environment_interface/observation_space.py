#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'


class ObservationSpace(object):

  def __init__(self, valid_inputs):
    self._valid_inputs = valid_inputs

  @property
  def shape(self):
    return [len(self._valid_inputs)]
