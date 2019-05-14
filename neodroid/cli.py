import os
import shutil
import stat
import subprocess

import draugr
import fire
from pyfiglet import Figlet

from neodroid.utilities.download_utilities.download_environment import (available_environments,
                                                                        download_environment,
                                                                        )
from neodroid.version import get_version

margin_percentage = (0 / 6)
terminal_width = draugr.get_terminal_size().columns
margin = int(margin_percentage * terminal_width)
width = (terminal_width - 2 * margin)
underline = '_' * width
indent = " " * margin


class NeodroidCLI(object):
  default_executables_path = '/tmp/neodroid'

  def run(self, env_name: str):
    '''
    Run an environment
    '''
    fail = False
    if os.path.exists(self.default_executables_path):
      exe_path = f'{self.default_executables_path}/{env_name}/{env_name.split("_")[0]}.x86_64'

      st = os.stat(exe_path)
      os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

      if os.path.exists(exe_path):
        cmd = [f'{exe_path}']
        subprocess.Popen(cmd)
      else:
        print(f'Can not find {exe_path}')
        fail = True
    else:
      print(f'Can not find {self.default_executables_path}')
      fail = True
    if fail:
      self.fetch(env_name)
      if os.path.exists(self.default_executables_path):
        exe_path = f'{self.default_executables_path}/{env_name}/{env_name.split("_")[0]}.x86_64'

        st = os.stat(exe_path)
        os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

        if os.path.exists(exe_path):
          cmd = [f'{exe_path}']
          subprocess.Popen(cmd)
        else:
          print(f'Still can not find {exe_path}')
      else:
        print(f'Still can not find {self.default_executables_path}')

  def fetch(self, env_name: str):
    '''
    Fetches a remotely stored environment with the specified name to local storage
    '''
    exe_path = download_environment(env_name, path_to_executables_directory=self.default_executables_path)
    print(f'{indent}Installed {env_name} to {exe_path}')
    return exe_path

  def install(self, env_name: str):
    '''
    Fetches a remotely stored environment with the specified name to local storage
    '''
    return self.fetch(env_name)

  def remove(self, env_name: str):
    '''
    Removes locally stored environment with the specified name
    '''
    exe_path = f'{self.default_executables_path}/{env_name}'
    shutil.rmtree(exe_path, ignore_errors=True)
    # os.remove(exe_path)
    print(f'{indent}Removed {exe_path}')

  def update(self, env_name: str):
    '''
    Updates, fetches environment with the specified name again and replaces the previous version if present
    '''
    if os.path.exists(self.default_executables_path):
      self.remove(env_name)
      exe_path = self.fetch(env_name)
      print(f'{indent}Updated {env_name} at {exe_path}')

  def clean(self):
    '''
    Removes all locally stored environments
    '''
    if os.path.exists(self.default_executables_path):
      shutil.rmtree(self.default_executables_path, ignore_errors=True)
    print(f'{indent}cleaned, removed {self.default_executables_path}')

  def ls_local(self):
    '''
    Which environments are available locally
    '''
    envs = []
    if os.path.exists(self.default_executables_path):
      envs = os.listdir(self.default_executables_path)

    if len(envs) > 0:
      for env_key in envs:
        print(f'{indent}{env_key}')
    else:
      print(f'{indent}No environments found at {self.default_executables_path}')

  def ls_remote(self):
    '''
        Which environments are available on remote servers
    '''
    envs = available_environments()
    for k, v in envs.items():
      print(f'{indent}- {k}')

  def ls(self):
    '''
    Same as ls_local result
    '''
    self.ls_local()

  def version(self):
    '''
    Prints the version of this Neodroid installation.
    '''
    draw_cli_header()
    print(f'Version: {get_version()}')


def draw_cli_header(*,
                    title='Neodroid',
                    font='big'):
  figlet = Figlet(font=font, justify='center', width=terminal_width)
  description = figlet.renderText(title)

  print(f'{description}{indent}{underline}\n')


def main(*,
         always_draw_header=False):
  if always_draw_header:
    draw_cli_header()
  fire.Fire(NeodroidCLI, name='neodroid')


if __name__ == '__main__':
  main()
