# Borrowed for PyTorch repo
# This script outputs relevant system environment info
# Run it with `python collect_env.py`.
import re
import subprocess
import sys
from collections import namedtuple

import neodroid as neo

PY3 = sys.version_info >= (3, 0)

# System Environment Information
SystemEnv = namedtuple('SystemEnv', [
  'neo_version',
  'is_debug_build',
  'os',
  'python_version',
  'pip_version',  # 'pip' or 'pip3'
  'pip_packages',
  ])


def run(command):
  '''Returns (return-code, stdout, stderr)'''
  p = subprocess.Popen(command, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, shell=True)
  output, err = p.communicate()
  rc = p.returncode
  if PY3:
    output = output.decode('ascii')
    err = err.decode('ascii')
  return rc, output.strip(), err.strip()


def run_and_read_all(run_lambda, command):
  '''Runs command using run_lambda; reads and returns entire output if rc is 0'''
  rc, out, _ = run_lambda(command)
  if rc is not 0:
    return None
  return out


def run_and_parse_first_match(run_lambda, command, regex):
  '''Runs command using run_lambda, returns the first regex match if it exists'''
  rc, out, _ = run_lambda(command)
  if rc is not 0:
    return None
  match = re.search(regex, out)
  if match is None:
    return None
  return match.group(1)


def get_platform():
  if sys.platform.startswith('linux'):
    return 'linux'
  elif sys.platform.startswith('win32'):
    return 'win32'
  elif sys.platform.startswith('cygwin'):
    return 'cygwin'
  elif sys.platform.startswith('darwin'):
    return 'darwin'
  else:
    return sys.platform


def get_mac_version(run_lambda):
  return run_and_parse_first_match(run_lambda, 'sw_vers -productVersion', r'(.*)')


def get_windows_version(run_lambda):
  return run_and_read_all(run_lambda, 'wmic os get Caption | findstr /v Caption')


def get_lsb_version(run_lambda):
  return run_and_parse_first_match(run_lambda, 'lsb_release -a', r'Description:\t(.*)')


def check_release_file(run_lambda):
  return run_and_parse_first_match(run_lambda, 'cat /etc/*-release',
                                   r'PRETTY_NAME="(. *)"')


def get_os(run_lambda):
  platform = get_platform()

  if platform is 'win32' or platform is 'cygwin':
    return get_windows_version(run_lambda)

  if platform == 'darwin':
    version = get_mac_version(run_lambda)
    if version is None:
      return None
    return 'Mac OSX {}'.format(version)

  if platform == 'linux':
    # Ubuntu/Debian based
    desc = get_lsb_version(run_lambda)
    if desc is not None:
      return desc

    # Try reading /etc/*-release
    desc = check_release_file(run_lambda)
    if desc is not None:
      return desc

    return platform

  # Unknown platform
  return platform


def get_pip_packages(run_lambda):
  # People generally have `pip` as `pip` or `pip3`
  def run_with_pip(pip):
    return run_and_read_all(run_lambda, pip + ' list - -format=legacy | grep "neo\ | numpy"')

  if not PY3:
    return 'pip', run_with_pip('pip')

  # Try to figure out if the user is running pip or pip3.
  out2 = run_with_pip('pip')
  out3 = run_with_pip('pip3')

  number_of_pips = len([x for x in [out2, out3] if x is not None])
  if number_of_pips is 0:
    return 'pip', out2

  if number_of_pips == 1:
    if out2 is not None:
      return 'pip', out2
    return 'pip3', out3

  # num_pips is 2. Return pip3 by default b/c that most likely
  # is the one associated with Python 3
  return 'pip3', out3


def get_env_info():
  run_lambda = run
  pip_version, pip_list_output = get_pip_packages(run_lambda)

  return SystemEnv(
      neo_version=neo.__version__,
      is_debug_build=neo.version.debug,
      python_version='{}.{}'.format(
          sys.version_info[0], sys.version_info[1]),
      pip_version=pip_version,
      pip_packages=pip_list_output,
      os=get_os(run_lambda),
      )


env_info_fmt = '''
Neo version: {neo_version}
Is debug build: {is_debug_build}
OS: {os}
Python version: {python_version}
Versions of relevant libraries:
{pip_packages}
'''.strip()


def pretty_str(env_info):
  def replace_all_none_objects(dct, replacement='Could not collect'):
    for key in dct.keys():
      if dct[key] is not None:
        continue
      dct[key] = replacement
    return dct

  def replace_bools(dct, true='Yes', false='No'):
    for key in dct.keys():
      if dct[key] is True:
        dct[key] = true
      elif dct[key] is False:
        dct[key] = false
    return dct

  def prepend(text, tag='[prepend]'):
    lines = text.split('\n')
    updated_lines = [tag + line for line in lines]
    return '\n'.join(updated_lines)

  def replace_if_empty(text, replacement='No relevant packages'):
    if text is not None and len(text) == 0:
      return replacement
    return text

  def maybe_start_on_next_line(string):
    # If `string` is multiline, prepend a \n to it.
    if string is not None and len(string.split('\n')) > 1:
      return '\n{}\n'.format(string)
    return string

  mutable_dict = env_info._asdict()

  # Replace True with Yes, False with No
  mutable_dict = replace_bools(mutable_dict)

  # Replace all None objects with 'Could not collect'
  mutable_dict = replace_all_none_objects(mutable_dict)

  # If either of these are '', replace with 'No relevant packages'
  mutable_dict['pip_packages'] = replace_if_empty(
      mutable_dict['pip_packages'])

  if mutable_dict['pip_packages']:
    mutable_dict['pip_packages'] = prepend(mutable_dict['pip_packages'],
                                           '[{}] '.format(env_info.pip_version))
  return env_info_fmt.format(**mutable_dict)


def get_pretty_env_info():
  return pretty_str(get_env_info())


def main():
  print('Collecting environment information...')
  output = get_pretty_env_info()
  print(output)


if __name__ == '__main__':
  main()
