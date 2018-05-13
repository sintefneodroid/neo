#!/usr/bin/env python3
# coding=utf-8
from neodroid.version import get_version

__author__ = 'cnheider'

from setuptools import find_packages, setup

packages = find_packages(exclude=['neodroid/environments'])
package_data = {
  'neodroid': [
    # 'environments/grid_world*',
    # glob.glob('environments/**', recursive=True)
    ]
  }


def get_readme():
  with open('README.md') as f:
    return f.read()


def get_keyword():
  with open('KEYWORDS.md') as f:
    return f.read()


setup(
    name='Neodroid',
    version=get_version(),
    packages=packages,
    include_package_data=True,
    # package_data=package_data,
    author='Christian Heider Nielsen',
    author_email='chrini13@student.aau.dk',
    description='Python interface for the Neodroid platform, '
                'an API for communicating with a Unity '
                'Game process for a feedback response loop',
    long_description=get_readme(),
    license='Apache License, Version 2.0',
    keywords=get_keyword(),
    url='https://github.com/sintefneodroid/neo',
    install_requires=[
      'pyzmq', 'numpy', 'neodroid-flatbuffers', 'Pillow', 'gym', 'tqdm', 'matplotlib', 'flatbuffers'
      ],
    extras_require={'GUI': ['kivy']},
    )
