#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from samples.example_algorithms import UCB1

__author__ = 'cnheider'

import neodroid.wrappers.formal_wrapper as neo
from neodroid import messaging, ReactionParameters


def construct_displayables(normed, tries,totals):
  d1 = messaging.N.Displayable('BeliefBarLeftDisplayer', normed[0])
  d2 = messaging.N.Displayable('BeliefBarMiddleDisplayer', normed[1])
  d3 = messaging.N.Displayable('BeliefBarRightDisplayer', normed[2])
  d12 = messaging.N.Displayable('BeliefTextLeftDisplayer', normed[0])
  d22 = messaging.N.Displayable('BeliefTextMiddleDisplayer', normed[1])
  d32 = messaging.N.Displayable('BeliefTextRightDisplayer', normed[2])
  d13 = messaging.N.Displayable('CountTextLeftDisplayer', f'{totals[0]} / {tries[0]}')
  d23 = messaging.N.Displayable('CountTextMiddleDisplayer', f'{totals[1]} / {tries[1]}')
  d33 = messaging.N.Displayable('CountTextRightDisplayer', f'{totals[2]} / {tries[2]}')
  return [d1, d2, d3, d12, d22, d32, d13, d23, d33]


def main(connect_to_running=False):
  _environment = neo.make('mab', connect_to_running=connect_to_running)

  num_arms = _environment.action_space.num_discrete_actions

  beliefs = [1 / num_arms] * num_arms
  totals = [0] * num_arms
  tries = [0] * num_arms
  normed = [1 / num_arms] * num_arms

  ucb1 = UCB1(num_arms)

  i = 0
  while _environment.is_connected:
    action_0 = ucb1.select_arm()

    index_0 = int(action_0)

    motions = [messaging.N.Motion('MultiArmedBanditKillableActor',
                                  'MultiArmedBanditMotor',
                                  action_0)]

    i += 1

    reaction = messaging.N.Reaction(
        motions=motions,
        displayables=construct_displayables(normed, tries,totals),
        parameters=ReactionParameters(step=True, episode_count=True),
        serialised_message='this is a serialised_message'
        )

    _, reward, terminated, info = _environment.act(reaction)

    print(reward)

    ucb1.update_belief(action_0, reward)

    tries[index_0] += 1
    totals[index_0] += reward
    beliefs[index_0] = float(totals[index_0]) / tries[index_0]

    for i in range(len(beliefs)):
      normed[i] = beliefs[i] / (sum(beliefs) + sys.float_info.epsilon)


    if terminated:
      print(info.termination_reason)


if __name__ == '__main__':
  main(connect_to_running=True)
