#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = ""

import contextlib

import neodroid

for i in range(100):
    with neodroid.connect() as env, contextlib.suppress(KeyboardInterrupt):
        print(i)
        env.react()
