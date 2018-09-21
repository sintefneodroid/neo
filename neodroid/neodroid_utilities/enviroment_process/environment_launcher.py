#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import os
import shlex
import struct
import subprocess
import sys


def launch_environment(environment_name,
                       path_to_executables_directory,
                       ip,
                       port,
                       full_screen='0',
                       screen_height=500,
                       screen_width=500,
                       headless=False):
  system_arch = struct.calcsize("P") * 8
  print(system_arch)
  path = os.path.join(path_to_executables_directory, f'{environment_name}')

  env_name = f'{environment_name}' if not headless else f'{environment_name}_headless'

  path_to_executable = os.path.join(path,
                                    f'{env_name}.exe')
  if sys.platform != 'win32':
    if system_arch == 32:
      path_to_executable = os.path.join(path, f'{env_name}.x86')
    else:
      path_to_executable = os.path.join(path, f'{env_name}.x86_64')

  # new_env = os.environ.copy()
  # new_env['vblank_mode'] = '0'
  # pre_args = ['vblank_mode=0','optirun']
  post_args = shlex.split(
      f' -ip {ip}'
      f' -port {port}'
      # f' -screen-fullscreen {full_screen}'
      # f' -screen-height {screen_height}'
      # f' -screen-width {screen_width}'
      # f' -batchmode'
      # f' -nographics'
      )
  # cmd= pre_args+[path_to_executable] + post_args
  cmd = [path_to_executable] + post_args
  print(cmd)
  return subprocess.Popen(
      cmd
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
