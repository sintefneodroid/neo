#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from warg.arguments import add_bool_arg

from neodroid.utilities import Displayable
from ucb1 import UCB1

__author__ = "Christian Heider Nielsen"

import neodroid.environments.unity.single_unity_environment as neo


def construct_displayables(normed, tries, totals):
    d1 = Displayable("BeliefBarLeftDisplayer", normed[0])
    d2 = Displayable("BeliefBarMiddleDisplayer", normed[1])
    d3 = Displayable("BeliefBarRightDisplayer", normed[2])
    d12 = Displayable("BeliefTextLeftDisplayer", normed[0])
    d22 = Displayable("BeliefTextMiddleDisplayer", normed[1])
    d32 = Displayable("BeliefTextRightDisplayer", normed[2])
    d13 = Displayable("CountTextLeftDisplayer", f"{totals[0]} / {tries[0]}")
    d23 = Displayable("CountTextMiddleDisplayer", f"{totals[1]} / {tries[1]}")
    d33 = Displayable("CountTextRightDisplayer", f"{totals[2]} / {tries[2]}")
    return [d1, d2, d3, d12, d22, d32, d13, d23, d33]


def main(connect_to_running=False):
    parser = argparse.ArgumentParser(prog="mab")
    add_bool_arg(
        parser,
        "connect_to_running",
        dest="CONNECT_TO_RUNNING",
        default=connect_to_running,
        help="Connect to already running simulation or start an instance",
    )
    args = parser.parse_args()

    _environment = neo.SingleUnityEnvironment(
        environment_name="mab", connect_to_running=args.CONNECT_TO_RUNNING
    )

    num_arms = _environment.action_space.num_binary_discrete_actions
    print(num_arms)
    totals = [0] * num_arms

    ucb1 = UCB1(num_arms)

    i = 0
    while _environment.is_connected:
        action = int(ucb1.select_arm())

        i += 1

        _, signal, terminated, info = _environment.react(action).to_gym_like_output()

        ucb1.update_belief(action, signal)

        totals[action] += signal

        _environment.display(
            displayables=construct_displayables(
                ucb1.normalised_values, ucb1.counts, totals
            )
        )

        if terminated:
            print(info.termination_reason)
            _environment.reset()


if __name__ == "__main__":
    main(connect_to_running=True)
