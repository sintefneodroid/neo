#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import time

import numpy

from neodroid.environments.droid_environment import connect_dict

__author__ = "Christian Heider Nielsen"

from warg import add_bool_arg
from draugr.tqdm_utilities import progress_bar


def main():
    """ """
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

    for obs in progress_bar(
        connect_dict(ip=aargs.IP, port=aargs.PORT), description="env"
    ):
        pass


if __name__ == "__main__":
    main()
