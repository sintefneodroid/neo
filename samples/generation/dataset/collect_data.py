#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.environments.unity_environment import connect

__author__ = "Christian Heider Nielsen"
__doc__ = (
    "Small sample program for connecting to environment and collecting observations"
)

if __name__ == "__main__":

    def main(generate_num=10):

        if generate_num > 0:
            with connect() as env:
                for i, state in enumerate(env):
                    if i >= generate_num:
                        break

                    state = next(iter(state.values()))
                    label = state.sensor("String").value
                    ray = state.sensor("Ray").value
                    image = state.sensor("RGB").value

                    print(label, ray, image)

    main()
