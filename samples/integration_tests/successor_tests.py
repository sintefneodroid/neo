#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/06/2020
           """

from draugr.tqdm_utilities import progress_bar

if __name__ == "__main__":

    def mixed():
        import neodroid

        a = [-1]
        with neodroid.connect() as env:
            env.reset()
            for i in progress_bar(range(1, 1000)):
                snapshot = next(iter(env.react().values()))
                if i != snapshot.frame_number or a == snapshot.observables:
                    print(i)
                    print(snapshot.observables)
                    print(snapshot.frame_number)
                    print("Not expected!")

                a = snapshot.observables

        print("Done")

    def increasing():
        import neodroid

        a = [-1]
        with neodroid.connect() as env:
            env.reset()
            for i in progress_bar(range(1, 1000)):
                snapshot = next(iter(env.react().values()))
                if i != snapshot.frame_number or a > snapshot.observables:
                    print(i)
                    print(a)
                    print(snapshot.observables)
                    print(snapshot.frame_number)
                    print("Not expected!")

                a = snapshot.observables

        print("Done")

    def decreasing():
        import neodroid

        a = [-1]
        with neodroid.connect() as env:
            env.reset()
            for i in progress_bar(range(1, 1000)):
                snapshot = next(iter(env.react().values()))
                if i != snapshot.frame_number or a < snapshot.observables:
                    print(i)
                    print(snapshot.observables)
                    print(snapshot.frame_number)
                    print("Not expected!")

                a = snapshot.observables

        print("Done")

    mixed()
    # increasing()
    # decreasing()
