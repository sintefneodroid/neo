#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.environments import connect

__author__ = "Christian Heider Nielsen"

from neodroid import messaging


def main():
    _environment = connect()

    i = 0
    while _environment.is_connected:
        print(f"iter {i}")
        p = "." * (i % 100)
        i += 1
        d1 = messaging.N.Displayable("TextMeshDisplayer", f"Hello from Python{p}")
        d2 = messaging.N.Displayable("TextDisplayer", f"TextDisplayer {i}")
        reaction = messaging.N.Reaction(
            displayables=[d1, d2], serialised_message="this is a serialised_message"
        )
        info = _environment.react([reaction])
        asd = iter(info.values()).__next__()
        if asd.terminated:
            print(asd.termination_reason)


if __name__ == "__main__":
    main()
