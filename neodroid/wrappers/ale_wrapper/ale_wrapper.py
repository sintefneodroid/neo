#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.wrappers import SingleEnvironment

__author__ = 'cnheider'


class NeodroidALEWrapper(SingleEnvironment):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def act(
      self,
      input_reaction=None,
      on_step_done_callback=None,
      on_reaction_sent_callback=None,
      ):
    pass

  def reset_game(self, input_configuration=None):
    pass
