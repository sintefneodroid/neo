#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'


# Copied from https://github.com/ghliu/pytorch-ddpg/blob/master/random_process.py


# [reference] https://github.com/matthiasplappert/keras-rl/blob/master/rl/random.py

class RandomProcess(object):
  def reset(self):
    raise NotImplementedError

  def sample(self):
    raise NotImplementedError
