#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'cnheider'


def launch_environment(environment_name,
                       *,
                       path_to_executables_directory,
                       ip='127.0.0.1',
                       port=5252,
                       headless=False):
  '''


  :param environment_name:
  :param path_to_executables_directory:
  :param ip:
  :param port:
  :param headless:
  :return:
  '''
  import logging
  import pathlib

  from neodroid.utilities.launcher.download_utilities.download_environment import download_environment
  import os
  import shlex
  import struct
  import subprocess
  import sys
  import stat

  environment_name = pathlib.Path(environment_name)

  if pathlib.Path.exists(environment_name):
    path_to_executable = environment_name
  else:
    system_arch = struct.calcsize("P") * 8

    logging.info(f'System Architecture: {system_arch}')

    variation_name = f'{environment_name}' if not headless else f'{environment_name}_headless'

    if sys.platform == 'win32':
      variation_name = f'{variation_name}_win'
    elif sys.platform == 'darwin':
      variation_name = f'{variation_name}_mac'
    else:
      variation_name = f'{variation_name}_linux'

    base_name = pathlib.Path(path_to_executables_directory) / environment_name
    path = base_name / variation_name

    if not base_name.exists():
      old_mask = os.umask(000)
      try:
        base_name.mkdir(0o777, parents=True, exist_ok=True)
      finally:
        os.umask(old_mask)

    if not path.exists():
      download_environment(variation_name, path_to_executables_directory=base_name)

    path_to_executable = path / 'Neodroid.exe'
    if sys.platform != 'win32':
      if system_arch == 32:
        path_to_executable = path / f'{environment_name}.x86'
      else:
        path_to_executable = path / f'{environment_name}.x86_64'

    '''
      cwd = os.getcwd()
      file_name = (file_name.strip()
                   .replace('.app', '').replace('.exe', '').replace('.x86_64', '').replace('.x86', ''))
      true_filename = os.path.basename(os.path.normpath(file_name))
      launch_string = None
      if platform == 'linux' or platform == 'linux2':
        candidates = glob.glob(pathlib.Path.joinpath(cwd, file_name) + '.x86_64')
        if len(candidates) == 0:
          candidates = glob.glob(pathlib.Path.joinpath(cwd, file_name) + '.x86')
        if len(candidates) == 0:
          candidates = glob.glob(file_name + '.x86_64')
        if len(candidates) == 0:
          candidates = glob.glob(file_name + '.x86')
        if len(candidates) > 0:
          launch_string = candidates[0]
  
      elif platform == 'darwin':
        candidates = glob.glob(pathlib.Path.joinpath(cwd, file_name + '.app', 'Contents', 'MacOS', 
        true_filename))
        if len(candidates) == 0:
          candidates = glob.glob(pathlib.Path.joinpath(file_name + '.app', 'Contents', 'MacOS', true_filename))
        if len(candidates) == 0:
          candidates = glob.glob(pathlib.Path.joinpath(cwd, file_name + '.app', 'Contents', 'MacOS', '*'))
        if len(candidates) == 0:
          candidates = glob.glob(pathlib.Path.joinpath(file_name + '.app', 'Contents', 'MacOS', '*'))
        if len(candidates) > 0:
          launch_string = candidates[0]
      elif platform == 'win32':
        candidates = glob.glob(pathlib.Path.joinpath(cwd, file_name + '.exe'))
        if len(candidates) == 0:
          candidates = glob.glob(file_name + '.exe')
        if len(candidates) > 0:
          launch_string = candidates[0]
  
    '''

  st = path_to_executable.stat()  # Ensure file is executable
  path_to_executable.chmod( st.st_mode | stat.S_IEXEC)

  # new_env = os.environ.copy()
  # new_env['vblank_mode'] = '0'
  # pre_args = ['vblank_mode=0','optirun']
  post_args = shlex.split(f' -ip {ip}'
                          f' -port {port}'
                          # f' -batchmode'
                          # f' -nographics'
                          )
  # cmd= pre_args+[path_to_executable] + post_args
  cmd = [path_to_executable] + post_args

  logging.info(cmd)
  return subprocess.Popen(cmd
                          # ,env=new_env
                          )
