#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.version import get_version

__author__ = 'cnheider'

from setuptools import find_packages, setup


class NeodroidPackage:
  @property
  def packages(self):
    return find_packages(
        exclude=[
          'neodroid/environments'
          ]
        )

  @property
  def package_data(self):
    return {
      'neodroid':[
        'environments/mab/*',
        # glob.glob('environments/**', recursive=True)
        ]
      }

  @property
  def entry_points(self):
    return {
      'console_scripts':[
        # "name_of_executable = module.with:function_to_execute"
        'neodroid = examples.minimal.multi_armed_bandit:main',
        ]
      }

  @property
  def extras(self):
    return {
      'GUI':['kivy']
      }

  @property
  def requirements(self) -> list:
    return [
      'pyzmq',
      'numpy',
      'neodroid-flatbuffers',
      # 'flatbuffers',
      'Pillow',
      'gym',
      'tqdm',
      'matplotlib',
      'cloudpickle'
      ]

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
    return get_version()


neo_pkg = NeodroidPackage()

setup(
    name='Neodroid',
    version=neo_pkg.version,
    packages=neo_pkg.packages,
    include_package_data=True,
    package_data=neo_pkg.package_data,
    author='Christian Heider Nielsen',
    author_email='chrini13@student.aau.dk',
    maintainer='Christian Heider Nielsen',
    maintainer_email='chrini13@student.aau.dk',
    description=neo_pkg.description,
    license=neo_pkg.license,
    keywords=neo_pkg.keyword,
    url='https://github.com/sintefneodroid/neo',
    download_url='https://github.com/sintefneodroid/neo/releases',
    install_requires=neo_pkg.requirements,
    extras_require=neo_pkg.extras,
    entry_points=neo_pkg.entry_points,
    classifiers=neo_pkg.classifiers,
    long_description_content_type='text/markdown',
    long_description=neo_pkg.readme,
    tests_require=['pytest'],
    python_requires='>=3'
    )
