#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def python_version_check():
  import sys

  assert sys.version_info.major == 3 and sys.version_info.minor >= 6, (
    f'This project is utilises language features only present Python 3.6 and greater. '
    f'You are running {sys.version_info}.')


python_version_check()

__author__ = 'cnheider'

import os
import pathlib
import re

from setuptools import find_packages

_v = pathlib.Path(os.path.dirname(__file__)) / "neodroid" / "__init__.py"
with open(_v, "r") as f:
  content = f.read()

  version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", content, re.M).group(
      1)  # get version string from module

  project_name = re.search(r"PROJECT_NAME = ['\"]([^'\"]*)['\"]", content, re.M).group(
      1)  # get project name string from module


class NeodroidPackageMeta(type):

  @property
  def test_dependencies(self) -> list:
    return [
      'pytest',
      'mock'
      ]

  @property
  def setup_dependencies(self) -> list:
    return [
      'pytest-runner'
      ]

  @property
  def package_name(self) -> str:
    return project_name

  @property
  def url(self) -> str:
    return 'https://github.com/sintefneodroid/neo'

  @property
  def download_url(self):
    return self.url + '/releases'

  @property
  def readme_type(self):
    return 'text/markdown'

  @property
  def packages(self):
    return find_packages(
        exclude=[
          # 'neodroid/environments'
          ]
        )

  @property
  def author_name(self):
    return 'Christian Heider Nielsen'

  @property
  def author_email(self):
    return 'christian.heider@alexandra.dk'

  @property
  def maintainer_name(self):
    return self.author_name

  @property
  def maintainer_email(self):
    return self.author_email

  @property
  def package_data(self):
    # data = glob.glob('environments/mab/**', recursive=True)
    return {
      'neodroid':[
        # *data
        # 'environments/mab/**',
        # 'environments/mab/**_Data/*',
        # 'environments/mab/windows/*'
        # 'environments/mab/windows/*_Data/*'
        ]
      }

  @property
  def entry_points(self):
    return {
      'console_scripts':[
        # "name_of_executable = module.with:function_to_execute"
        'neodroid = entry_points.cli:main',
        'neodroid-sample = samples.action_space_sampling:main',
        'neodroid-img = samples.image_observation_plot:main',
        'neodroid-mab = samples.mab.multi_armed_bandit:main',
        'neodroid-kb = samples.keyboard.qweasd_input:main',
        'neodroid-gui = samples.gui_client.main:main'
        ]
      }

  @property
  def extras(self) -> dict:

    path = pathlib.Path(__file__).parent
    requirements_gui = []
    with open(path / 'requirements_gui.txt') as f:
      requirements = f.readlines()

      for requirement in requirements:
        requirements_gui.append(requirement.strip())

    requirements_tests = []
    with open(path / 'requirements_tests.txt') as f:
      requirements = f.readlines()

      for requirement in requirements:
        requirements_tests.append(requirement.strip())

    requirements_docs = []
    with open(path / 'requirements_docs.txt') as f:
      requirements = f.readlines()

      for requirement in requirements:
        requirements_docs.append(requirement.strip())

    requirements_dev = []
    with open(path / 'requirements_dev.txt') as f:
      requirements = f.readlines()

      for requirement in requirements:
        requirements_dev.append(requirement.strip())

    these_extras = {
      'gui':  requirements_gui,
      'tests':requirements_tests,
      # 'docs':requirements_docs,
      'dev':  requirements_dev

      # 'mab':['neodroid-linux-mab; platform_system == "Linux"',
      #       'neodroid-win-mab platform_system == "Windows"']

      }

    all_dependencies = []

    for group_name in these_extras:
      all_dependencies += these_extras[group_name]
    these_extras['all'] = all_dependencies

    return these_extras

  @property
  def requirements(self) -> list:
    path = pathlib.Path(__file__).parent
    requirements_out = []
    with open(path / 'requirements.txt') as f:
      requirements = f.readlines()

      for requirement in requirements:
        requirements_out.append(requirement.strip())

    return requirements_out

  @property
  def description(self):
    return 'Python interface for the Neodroid platform,' \
           ' an API for communicating with a Unity Game ' \
           'process for a feedback response loop'

  @property
  def readme(self):
    with open('README.md') as f:
      return f.read()

  @property
  def keyword(self):
    with open('KEYWORDS.md') as f:
      return f.read()

  @property
  def license(self):
    return 'Apache License, Version 2.0'

  @property
  def classifiers(self):
    return [
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
      'Natural Language :: English',
      # 'Topic :: Scientific/Engineering :: Artificial Intelligence'
      # 'Topic :: Software Development :: Bug Tracking',
      ]

  @property
  def version(self):
    return version


class NeodroidPackage(metaclass=NeodroidPackageMeta):
  pass


from setuptools import setup

if __name__ == '__main__':

  pkg = NeodroidPackage

  setup(name=pkg.package_name,
        version=pkg.version,
        packages=pkg.packages,
        package_data=pkg.package_data,
        author=pkg.author_name,
        author_email=pkg.author_email,
        maintainer=pkg.maintainer_name,
        maintainer_email=pkg.maintainer_email,
        description=pkg.description,
        license=pkg.license,
        keywords=pkg.keyword,
        url=pkg.url,
        download_url=pkg.download_url,
        install_requires=pkg.requirements,
        extras_require=pkg.extras,
        entry_points=pkg.entry_points,
        classifiers=pkg.classifiers,
        long_description_content_type=pkg.readme_type,
        long_description=pkg.readme,
        tests_require=pkg.test_dependencies,
        setup_requires=pkg.setup_dependencies,
        include_package_data=True,
        python_requires='>=3'
        )
