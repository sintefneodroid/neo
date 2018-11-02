import os
import shutil

from pyfiglet import Figlet
import fire

from neodroid.neodroid_utilities.download_utilities.download_environment import (available_environments,
                                                                                 download_environment,
                                                                                 )


class NeodroidCLI(object):

  def install(self, env_name:str):
    path_ = download_environment(env_name)
    print(f'Installed {env_name} to {path_}')
    return path_

  def remove(self, env_name:str):
    path_ =  f'/tmp/{env_name}'
    rc = shutil.rmtree(path_)
    #os.rmdir(f'/tmp/{env_name}')
    #os.remove(f'/tmp/{env_name}')
    print(f'Removed {path_} with return code: {rc}')

  def update(self, env_name:str):
    path_ = self.install(env_name)

    print(f'Updated {env_name} at {path_}')

  def clean(self):
    print(f'clean')

  def ls_local(self):
    print(os.listdir('/tmp'))

  def ls_remote(self):
    envs = available_environments()
    for k,v in envs.items():
      print(f'- {k}')

def main():
  font = 'big'
  figlet = Figlet(font=font)
  description= figlet.renderText('"|"  Neodroid  "|"')
  print(description)
  fire.Fire(NeodroidCLI)

if __name__ == '__main__':
    main()