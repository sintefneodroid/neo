#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib

from neodroid.utilities.debugging_utilities.verbosity import VerbosityLevel
from neodroid.utilities.download_utilities.download_environment import download_environment

__author__ = 'cnheider'

import os
import shlex
import struct
import subprocess
import sys


def launch_environment(environment_name,
                       *,
                       path_to_executables_directory,
                       ip='127.0.0.1',
                       port=5252,
                       full_screen='0',
                       screen_height=500,
                       screen_width=500,
                       headless=False,
                       verbose=VerbosityLevel.Warnings):
  import stat
  system_arch = struct.calcsize("P") * 8
  if verbose >= VerbosityLevel.Information:
    print(f'\nSystem Architecture: {system_arch}')

  variation_name = f'{environment_name}' if not headless else f'{environment_name}_headless'

  if sys.platform == 'win32':
    variation_name = f'{variation_name}_win'
  elif sys.platform == 'darwin':
    variation_name = f'{variation_name}_mac'
  else:
    variation_name = f'{variation_name}_linux'

  j = pathlib.Path.joinpath(path_to_executables_directory, environment_name)
  path = pathlib.Path.joinpath(j, variation_name)

  if not pathlib.Path.exists(j):
    old_mask = os.umask(000)
    try:
      pathlib.Path.mkdir(j, 0o777, exist_ok=True)
    finally:
      os.umask(old_mask)

  if not pathlib.Path.exists(path):
    download_environment(variation_name, path_to_executables_directory=j)

  path_to_executable = pathlib.Path.joinpath(path, 'Neodroid.exe')
  if sys.platform != 'win32':
    if system_arch == 32:
      path_to_executable = pathlib.Path.joinpath(path, f'{environment_name}.x86')
    else:
      path_to_executable = pathlib.Path.joinpath(path, f'{environment_name}.x86_64')

  # Ensure file is executable
  st = pathlib.Path.stat(path_to_executable)
  pathlib.Path.chmod(path_to_executable, st.st_mode | stat.S_IEXEC)

  # new_env = os.environ.copy()
  # new_env['vblank_mode'] = '0'
  # pre_args = ['vblank_mode=0','optirun']
  post_args = shlex.split(f' -ip {ip}'
                          f' -port {port}'
                          # f' -screen-fullscreen {full_screen}'
                          # f' -screen-height {screen_height}'
                          # f' -screen-width {screen_width}'
                          # f' -batchmode'
                          # f' -nographics'
                          )
  # cmd= pre_args+[path_to_executable] + post_args
  cmd = [path_to_executable] + post_args
  if verbose >= VerbosityLevel.Information:
    print(cmd)
  return subprocess.Popen(cmd
                          # ,env=new_env
                          )


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
