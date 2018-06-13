#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import os
import shlex
import subprocess
import sys


def launch_environment(environment_name, path_to_executables_directory, ip, port, full_screen='0',
                       screen_height=500, screen_width=500):
  path_to_executable = os.path.join(path_to_executables_directory, f'{environment_name}.exe')
  if sys.platform != 'win32':
    path_to_executable = os.path.join(path_to_executables_directory, f'{environment_name}.x86')
    # path_to_executable = os.path.join(path_to_executables_directory, f'{environment_name}.x64')
  args = shlex.split(
      f'-ip {ip}'
      f' -port {port}'
      f' -screen-fullscreen {full_screen}'
      f' -screen-height {screen_height}'
      f' -screen-width {screen_width}'
      # f' -batchmode'
      # f' -nographics'
      )
  print([path_to_executable] + args)
  return subprocess.Popen(
      [path_to_executable] + args
      )  # Figure out have to parameterise unity executable


'''
  cwd = os.getcwd()
  file_name = (file_name.strip()
               .replace('.app', '').replace('.exe', '').replace('.x86_64', '').replace('.x86', ''))
  true_filename = os.path.basename(os.path.normpath(file_name))
  launch_string = None
  if platform == 'linux' or platform == 'linux2':
    candidates = glob.glob(os.path.join(cwd, file_name) + '.x86_64')
    if len(candidates) == 0:
      candidates = glob.glob(os.path.join(cwd, file_name) + '.x86')
    if len(candidates) == 0:
      candidates = glob.glob(file_name + '.x86_64')
    if len(candidates) == 0:
      candidates = glob.glob(file_name + '.x86')
    if len(candidates) > 0:
      launch_string = candidates[0]

  elif platform == 'darwin':
    candidates = glob.glob(os.path.join(cwd, file_name + '.app', 'Contents', 'MacOS', true_filename))
    if len(candidates) == 0:
      candidates = glob.glob(os.path.join(file_name + '.app', 'Contents', 'MacOS', true_filename))
    if len(candidates) == 0:
      candidates = glob.glob(os.path.join(cwd, file_name + '.app', 'Contents', 'MacOS', '*'))
    if len(candidates) == 0:
      candidates = glob.glob(os.path.join(file_name + '.app', 'Contents', 'MacOS', '*'))
    if len(candidates) > 0:
      launch_string = candidates[0]
  elif platform == 'win32':
    candidates = glob.glob(os.path.join(cwd, file_name + '.exe'))
    if len(candidates) == 0:
      candidates = glob.glob(file_name + '.exe')
    if len(candidates) > 0:
      launch_string = candidates[0]

'''
