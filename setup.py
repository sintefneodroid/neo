#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.version import get_version

__author__ = 'cnheider'

from setuptools import find_packages, setup


def get_packages():
  return find_packages(exclude=['neodroid/environments'])


def get_package_data():
  return {
    'neodroid':[
      # 'environments/grid_world*',
      # glob.glob('environments/**', recursive=True)
      ]
    }


def get_entry_points():
  return {
    'console_scripts':[
      # "name_of_executable = module.with:function_to_execute"
      'neodroid = examples.minimal.multi_armed_bandit:main',
      ]
    }


def get_extras():
  return {'GUI':['kivy']}


def get_requirements() -> list:
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


def get_description():
  return 'Python interface for the Neodroid platform,' \
         ' an API for communicating with a Unity Game ' \
         'process for a feedback response loop'


def get_readme():
  with open('README.md') as f:
    return f.read()


def get_keyword():
  with open('KEYWORDS.md') as f:
    return f.read()


def get_license():
  return 'Apache License, Version 2.0'


def get_classifiers():
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
    'Topic :: Scientific/Engineering :: Artificial Intelligence'
    'Topic :: Software Development :: Bug Tracking',
    ]


setup(
    name='Neodroid',
    version=get_version(),
    packages=get_packages(),
    include_package_data=True,
    # package_data=get_package_data(),
    author='Christian Heider Nielsen',
    author_email='chrini13@student.aau.dk',
    maintainer='Christian Heider Nielsen',
    maintainer_email='chrini13@student.aau.dk',
    description=get_description(),
    long_description=get_readme(),
    license=get_license(),
    keywords=get_keyword(),
    url='https://github.com/sintefneodroid/neo',
    download_url='https://github.com/sintefneodroid/neo/releases',
    install_requires=get_requirements(),
    extras_require=get_extras(),
    entry_points=get_entry_points(),
    classifiers=get_classifiers(),
    long_description_content_type='text/markdown',
    tests_require=['pytest'],
    python_requires='>=3'
    )
