import os
import shutil

from tqdm import tqdm


class DownloadProgress(tqdm):
  last_block = 0

  def __init__(self, unit='B', unit_scale=True, min_iters=1, desc='Download', **kwargs):
    super().__init__(unit=unit, unit_scale=unit_scale, miniters=min_iters, desc=desc, **kwargs)

  def hook(self, block_num=1, block_size=1, total_size=None):
    self.total = total_size
    self.update((block_num - self.last_block) * block_size)
    self.last_block = block_num


def download_environment(name:str='mab_win', path_to_executables_directory: str = '/tmp/neodroid')-> str:
  """

  :param path_to_executables_directory:
  :return:
  :type name: object
  """
  from urllib.request import urlretrieve
  import zipfile
  download_format = 'https://drive.google.com/uc?export=download&confirm=NezD&id={FILE_ID}'
  hash_id = available_environments()[name]
  print(f'\nFetching {name} environment\n')
  formatted = download_format.format(FILE_ID=hash_id)  # +'.tmp')

  if not os.path.exists(path_to_executables_directory):
    os.makedirs(path_to_executables_directory)

  with DownloadProgress(desc=name) as progress_bar:
    zip_file_name, headers = urlretrieve(formatted,
                                     os.path.join(path_to_executables_directory,f'{name}.zip'),
                                     reporthook=progress_bar.hook)

  with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
    zip_ref.extractall(path_to_executables_directory)

  file = os.path.join(path_to_executables_directory, zip_file_name)
  #shutil.rmtree(file, ignore_errors=True)
  os.remove(file)

  return os.path.join(path_to_executables_directory, name)


def available_environments(repository='http://environments.neodroid.ml/ls'):
  from urllib.request import Request, urlopen
  import csv
  req = Request(repository, headers={'User-Agent':'Mozilla/5.0'})
  environments_m_csv = urlopen(req).read()
  environments_m_csv = environments_m_csv.decode('utf-8')
  reader = csv.reader(environments_m_csv.split('\n'), delimiter=',')
  environments_m = {row[0].strip():row[1].strip() for row in reader}
  return environments_m
