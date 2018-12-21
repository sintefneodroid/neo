import os
import shutil

from pyfiglet import Figlet
import fire

from neodroid.neodroid_utilities.download_utilities.download_environment import (available_environments,
                                                                                 download_environment,
                                                                                 )


class NeodroidCLI(object):
  default_executables_path = '/tmp/neodroid'

  def install(self, env_name: str):
    exe_path = download_environment(env_name, path_to_executables_directory=self.default_executables_path)
    print(f'Installed {env_name} to {exe_path}')
    return exe_path

  def remove(self, env_name: str):
    exe_path = f'{self.default_executables_path}/{env_name}'
    shutil.rmtree(exe_path, ignore_errors=True)
    # os.remove(exe_path)
    print(f'Removed {exe_path}')

  def update(self, env_name: str):
    if os.path.exists(self.default_executables_path):
      self.remove(env_name)
      exe_path = self.install(env_name)
      print(f'Updated {env_name} at {exe_path}')

  def clean(self):
    if os.path.exists(self.default_executables_path):
      shutil.rmtree(self.default_executables_path, ignore_errors=True)
    print('cleaned')

  def ls_local(self):
    envs = []
    if os.path.exists(self.default_executables_path):
      envs = os.listdir(self.default_executables_path)

    if len(envs) > 0:
      print(envs)
    else:
      print(f'No environments found at {self.default_executables_path}')

  def ls_remote(self):
    envs = available_environments()
    for k, v in envs.items():
      print(f'- {k}')


def main():
  title = 'Neodroid'
  font = 'big'
  figlet = Figlet(font=font, justify='center')
  description = figlet.renderText(title)
  print(f'\n{description}')
  fire.Fire(NeodroidCLI)


if __name__ == '__main__':
  main()
