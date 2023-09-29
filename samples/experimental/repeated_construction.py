#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = ""

import neodroid
from warg import IgnoreInterruptSignal

for i in range(100):
    with neodroid.connect() as env, IgnoreInterruptSignal():
        print(i)
        env.react()
