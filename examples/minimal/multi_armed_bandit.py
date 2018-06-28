#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import numpy as np

import neodroid.wrappers.formal_wrapper as neo
from neodroid import messaging, ReactionParameters


def main():
  _environment = neo.make('multi_armed_bandit', connect_to_running=True)

  i = 0
  while _environment.is_connected:
    actions = _environment.action_space.sample()
    i += 1
    d1 = messaging.N.Displayable('BeliefBarLeftDisplayer', 0.5)
    d2 = messaging.N.Displayable('BeliefBarMiddleDisplayer', 0.2)
    d3 = messaging.N.Displayable('BeliefBarRightDisplayer', 0.3)
    d12 = messaging.N.Displayable('BeliefTextLeftDisplayer', 0.5)
    d22 = messaging.N.Displayable('BeliefTextMiddleDisplayer', 0.2)
    d32 = messaging.N.Displayable('BeliefTextRightDisplayer', 0.3)
    reaction = messaging.N.Reaction(
        motions=actions,
        displayables=[d1, d2, d3, d12, d22, d32],
        parameters=ReactionParameters(step=True,episode_count=True),
        serialised_message='this is a serialised_message'
        )
    _, reward, terminated, info = _environment.act(input_reaction=reaction)
    print(reward)
    if terminated:
      print(info.termination_reason)


if __name__ == '__main__':
  main()
