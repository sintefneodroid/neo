#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'


class Motion(object):

  def __init__(self, actor_name, motor_name, strength):
    self._actor_name = actor_name
    self._motor_name = motor_name
    self._strength = strength
    # Strength has a possible direction given by the sign of the float

  @property
  def actor_name(self):
    return self._actor_name

  @property
  def motor_name(self):
    return self._motor_name

  @property
  def strength(self):
    return self._strength

  def to_dict(self):
    return {
      '_actor_name':self._actor_name,
      '_motor_name':self._motor_name,
      '_strength':  self._strength,
      }

  def __repr__(self):
    return (f'<Motion>\n'
            f'<actor_name>{self._actor_name}</actor_name>\n'
            f'<motor_name>{self._motor_name}</motor_name>\n'
            f'<strength>{self._strength}</strength>\n'
            f'</Motion>\n')

  def __str__(self):
    return self.__repr__()

  def __unicode__(self):
    return self.__repr__()
