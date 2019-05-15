#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'
__doc__ = ''

# %%
import neodroid

for i in range(100):
  with neodroid.connect() as env:
    print(i)
    env.react()

# %% [markdown]
# Heading 1
# Heading 2
## Heading 2.1
## Heading 2.2
#
# $e ^ {i\pi} + 1 = 0$
#
# %%

for i in range(100):
  with neodroid.connect() as env:
    print(i)
    env.react()
