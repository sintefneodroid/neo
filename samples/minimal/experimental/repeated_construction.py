#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'
__doc__ = ''

import neodroid

for i in range(100):
  with neodroid.connect() as env:
    print(i)
    print(env.react())
