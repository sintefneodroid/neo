from tqdm import tqdm


class DownloadProgress(tqdm):
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
  hash_id =available_environments()[name]
  formatted = download_format.format(FILE_ID=hash_id)#+'.tmp')

  with DownloadProgress(desc=name) as progress_bar:
    file_name, headers = urlretrieve(formatted,
                                     #os.path.join(path_to_executables_directory,f'{name}.tmp'),
                                     reporthook=progress_bar.hook)

  with zipfile.ZipFile(file_name, "r") as zip_ref:
    zip_ref.extractall(path_to_executables_directory)

def available_environments(repository='http://environments.neodroid.ml/ls'):
  from urllib.request import Request, urlopen
  import csv
  req = Request(repository, headers={'User-Agent': 'Mozilla/5.0'})
  environments_m_csv = urlopen(req).read()
  environments_m_csv = environments_m_csv.decode('utf-8')
  reader = csv.reader(environments_m_csv.split('\n'), delimiter=',')
  environments_m = {row[0].strip(): row[1].strip() for row in reader}
  return environments_m