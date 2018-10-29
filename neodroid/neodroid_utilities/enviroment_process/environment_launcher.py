#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cnheider'

import os
import shlex
import struct
import subprocess
import sys
import tqdm


def launch_environment(environment_name,
                       *,
                       path_to_executables_directory,
                       ip='127.0.0.1',
                       port=5252,
                       full_screen='0',
                       screen_height=500,
                       screen_width=500,
                       headless=False):
  system_arch = struct.calcsize("P") * 8
  print(f'\nSystem Architecture: {system_arch}')


  variation_name = f'{environment_name}' if not headless else f'{environment_name}_headless'


  if sys.platform == 'win32':
    variation_name= f'{variation_name}_win'
  elif sys.platform == 'darwin':
    variation_name = f'{variation_name}_mac'
  else:
    variation_name = f'{variation_name}_linux'

  j = os.path.join(
        path_to_executables_directory,environment_name)
  path = os.path.join(j ,variation_name)

  if not os.path.exists(j):
    old_mask = os.umask(000)
    try:
      os.makedirs(j, 0o777, exist_ok=True)
    finally:
      os.umask(old_mask)

  if not os.path.exists(path):
    download_environment(variation_name,path_to_executables_directory=j)

  path_to_executable = os.path.join(path,'Neodroid.exe')
  if sys.platform != 'win32':
    if system_arch == 32:
      path_to_executable = os.path.join(path, f'{environment_name}.x86')
    else:
      path_to_executable = os.path.join(path, f'{environment_name}.x86_64')

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


def available_environments(repository='http://boot.ml/environments'):
  from urllib.request import Request, urlopen
  import csv
  req = Request(repository, headers={'User-Agent': 'Mozilla/5.0'})
  environments_m_csv = urlopen(req).read()
  environments_m_csv = environments_m_csv.decode('utf-8')
  reader = csv.reader(environments_m_csv.split('\n'), delimiter=',')
  environments_m = {row[0]: row[1] for row in reader}
  return environments_m


class DownloadProgress(tqdm.tqdm):
  last_block = 0

  def __init__(self, unit='B', unit_scale=True, min_iters=1, desc='Download', **kwargs):
    super().__init__(unit=unit, unit_scale=unit_scale, miniters=min_iters, desc=desc, **kwargs)

  def hook(self, block_num=1, block_size=1, total_size=None):
    self.total = total_size
    self.update((block_num - self.last_block) * block_size)
    self.last_block = block_num


def download_environment(name='mab_win', path_to_executables_directory='/tmp'):
  from urllib.request import urlretrieve
  import zipfile
  download_format = 'https://drive.google.com/uc?export=download&confirm=NezD&id={FILE_ID}'
  formatted = download_format.format(FILE_ID=available_environments()[name])#+'.tmp')

  with DownloadProgress(desc=name) as progress_bar:
    file_name, headers = urlretrieve(formatted,
                                     #os.path.join(path_to_executables_directory,f'{name}.tmp'),
                                     progress_bar.hook)

  with zipfile.ZipFile(file_name, "r") as zip_ref:
    zip_ref.extractall(path_to_executables_directory)


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

if __name__ == '__main__':
  available_environments()
