#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import os
import shlex
import subprocess
import sys


def launch_environment(name, path_to_executables_directory, ip, port):
  path_to_executable = os.path.join(path_to_executables_directory,
                                    f'{name}.exe')
  if sys.platform != 'win32':
    path_to_executable = os.path.join(path_to_executables_directory,
                                      f'{name}.x86')
  args = shlex.split(
      '-ip ' + str(ip) + ' -port ' + str(port) +
      ' -screen-fullscreen 0 -screen-height 500 -screen-width 500'
      )  # -batchmode -nographics')
  print([path_to_executable] + args)
  return subprocess.Popen(
      [path_to_executable] +
      args)  # Figure out have to parameterise unity executable


'''
  cwd = os.getcwd()
  file_name = (file_name.strip()
               .replace('.app', '').replace('.exe', '').replace('.x86_64', '').replace('.x86', ''))
  true_filename = os.path.basename(os.path.normpath(file_name))
  launch_string = None
  if platform == "linux" or platform == "linux2":
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
