import os
import shutil
import stat
import subprocess
from pathlib import Path

import fire
from pyfiglet import Figlet

import draugr
from neodroid.utilities.launcher.download_utilities.download_environment import (available_environments,
                                                                                 download_environment,
                                                                                 )
from neodroid.version import DEFAULT_ENVIRONMENTS_PATH, get_version

margin_percentage = (0 / 6)
terminal_width = draugr.get_terminal_size().columns
margin = int(margin_percentage * terminal_width)
width = (terminal_width - 2 * margin)
underline = '_' * width
indent = " " * margin
sponsors = 'SINTEF Ocean, Alexandra Institute, Norges Forskningsråd'


class NeodroidCLI(object):

  def run(self, env_name: str) -> None:
    '''
    Run an environment
    '''
    fail = False
    if os.path.exists(DEFAULT_ENVIRONMENTS_PATH):
      exe_path = f'{DEFAULT_ENVIRONMENTS_PATH}/{env_name}/{env_name.split("_")[0]}.x86_64'

      st = os.stat(exe_path)
      os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

      if os.path.exists(exe_path):
        cmd = [f'{exe_path}']
        subprocess.Popen(cmd)
      else:
        print(f'Can not find {exe_path}')
        fail = True
    else:
      print(f'Can not find {DEFAULT_ENVIRONMENTS_PATH}')
      fail = True
    if fail:
      self.fetch(env_name)
      if os.path.exists(DEFAULT_ENVIRONMENTS_PATH):
        exe_path = f'{DEFAULT_ENVIRONMENTS_PATH}/{env_name}/{env_name.split("_")[0]}.x86_64'

        st = os.stat(exe_path)
        os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

        if os.path.exists(exe_path):
          cmd = [f'{exe_path}']
          subprocess.Popen(cmd)
        else:
          print(f'Still can not find {exe_path}')
      else:
        print(f'Still can not find {DEFAULT_ENVIRONMENTS_PATH}')

  @staticmethod
  def fetch(env_name: str) -> Path:
    '''
    Fetches a remotely stored environment with the specified name to local storage
    '''
    exe_path = download_environment(env_name, path_to_executables_directory=DEFAULT_ENVIRONMENTS_PATH)
    print(f'{indent}Installed {env_name} to {exe_path}')
    return exe_path

  def install(self, env_name: str) -> Path:
    '''
    Fetches a remotely stored environment with the specified name to local storage
    '''
    return self.fetch(env_name)

  @staticmethod
  def remove(env_name: str) -> None:
    '''
    Removes locally stored environment with the specified name
    '''
    exe_path = f'{DEFAULT_ENVIRONMENTS_PATH}/{env_name}'
    shutil.rmtree(exe_path, ignore_errors=True)
    # os.remove(exe_path)
    print(f'{indent}Removed {exe_path}')

  def update(self, env_name: str) -> None:
    '''
    Updates, fetches environment with the specified name again and replaces the previous version if present
    '''
    if os.path.exists(DEFAULT_ENVIRONMENTS_PATH):
      self.remove(env_name)
      exe_path = self.fetch(env_name)
      print(f'{indent}Updated {env_name} at {exe_path}')

  @staticmethod
  def clean(self) -> None:
    '''
    Removes all locally stored environments
    '''
    if os.path.exists(DEFAULT_ENVIRONMENTS_PATH):
      shutil.rmtree(DEFAULT_ENVIRONMENTS_PATH, ignore_errors=True)
    print(f'{indent}cleaned, removed {DEFAULT_ENVIRONMENTS_PATH}')

  def ls_local(self) -> None:
    '''
    Which environments are available locally
    '''
    envs = []
    if os.path.exists(DEFAULT_ENVIRONMENTS_PATH):
      envs = os.listdir(DEFAULT_ENVIRONMENTS_PATH)

    if len(envs) > 0:
      for env_key in envs:
        print(f'{indent}{env_key}')
    else:
      print(f'{indent}No environments found at {DEFAULT_ENVIRONMENTS_PATH}')

  @staticmethod
  def ls_remote() -> None:
    '''
        Which environments are available on remote servers
    '''
    envs = available_environments()
    for k, v in envs.items():
      print(f'{indent}- {k}')

  def ls(self) -> None:
    '''
    Same as ls_local result
    '''
    self.ls_local()

  @staticmethod
  def version() -> None:
    '''
    Prints the version of this Neodroid installation.
    '''
    draw_cli_header()
    print(f'Version: {get_version()}')

  @staticmethod
  def sponsors() -> None:
    print(sponsors)


def draw_cli_header(*,
                    title='Neodroid',
                    font='big'):
  figlet = Figlet(font=font, justify='center', width=terminal_width)
  description = figlet.renderText(title)

  print(f'{description}{underline}\n')


def main(*,
         always_draw_header=False):
  if always_draw_header:
    draw_cli_header()
  fire.Fire(NeodroidCLI, name='neodroid')


if __name__ == '__main__':
  main()
