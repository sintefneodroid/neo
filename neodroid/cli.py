import os
import shutil

from pyfiglet import Figlet
import fire
import draugr
from neodroid.neodroid_utilities.download_utilities.download_environment import (available_environments,
                                                                                 download_environment,
                                                                                 )

margin_percentage = (0 / 6)
terminal_width = draugr.get_terminal_size().columns
margin = int(margin_percentage * terminal_width)
width = (terminal_width - 2 * margin)
underline = '_' * width
indent = " " * margin

class NeodroidCLI(object):
  default_executables_path = '/tmp/neodroid'

  def install(self, env_name: str):
    exe_path = download_environment(env_name, path_to_executables_directory=self.default_executables_path)
    print(f'{indent}Installed {env_name} to {exe_path}')
    return exe_path

  def remove(self, env_name: str):
    exe_path = f'{self.default_executables_path}/{env_name}'
    shutil.rmtree(exe_path, ignore_errors=True)
    # os.remove(exe_path)
    print(f'{indent}Removed {exe_path}')

  def update(self, env_name: str):
    if os.path.exists(self.default_executables_path):
      self.remove(env_name)
      exe_path = self.install(env_name)
      print(f'{indent}Updated {env_name} at {exe_path}')

  def clean(self):
    if os.path.exists(self.default_executables_path):
      shutil.rmtree(self.default_executables_path, ignore_errors=True)
    print(f'{indent}cleaned, removed {self.default_executables_path}')

  def ls_local(self):
    envs = []
    if os.path.exists(self.default_executables_path):
      envs = os.listdir(self.default_executables_path)

    if len(envs) > 0:
      for env_key in envs:
        print(f'{indent}{env_key}')
    else:
      print(f'{indent}No environments found at {self.default_executables_path}')

  def ls_remote(self):
    envs = available_environments()
    for k, v in envs.items():
      print(f'{indent}- {k}')


def draw_cli_header(*,
                    title='Neodroid',
                    font='big'):

  figlet = Figlet(font=font, justify='center', width=terminal_width)
  description = figlet.renderText(title)

  print(f'{description}{indent}{underline}\n')


def main(*,
         draw_header=True):
  if draw_header:
    draw_cli_header()
  fire.Fire(NeodroidCLI)


if __name__ == '__main__':
  main()
