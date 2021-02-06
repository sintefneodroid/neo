#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import time

import numpy

from neodroid import connect

__author__ = "Christian Heider Nielsen"

from warg import add_bool_arg


def main():
    """"""
    parser = argparse.ArgumentParser(description="Neodroid Action Space Sampling")
    parser.add_argument(
        "--IP", "-ip", type=str, default="localhost", metavar="IP", help="IP Address"
    )
    parser.add_argument(
        "--PORT", "-port", type=int, default=6969, metavar="PORT", help="Port"
    )
    add_bool_arg(parser, "benchmark")
    add_bool_arg(parser, "verbose")
    add_bool_arg(parser, "reset")

    aargs = parser.parse_args()

    environment = connect(ip=aargs.IP, port=aargs.PORT)
    if aargs.reset:
        environment.reset()

    i = 1
    freq = 100
    time_s = time.time()
    terminated = []
    while environment.is_connected:
        action = [aas.sample() for aas in environment.action_space.values()]
        state = environment.react(action)

        for k, v in state.items():
            terminated.append(v.terminated)

        if aargs.benchmark:
            time_now = time.time()
            if i % freq == 0:
                fps = 1 / (time_now - time_s)
                print(f"fps:[{fps}]")
            time_s = time_now
        else:
            if aargs.verbose:
                a_out = state
            else:
                a = next(iter(state.values()))
                a_out = f"frame#{a.frame_number}, {a.observables}"
            print(f"snapshot#{i}, {a_out}")
        i += 1

        t = numpy.array(terminated)
        terminated = []
        if t.all():
            environment.reset()


if __name__ == "__main__":
    main()
