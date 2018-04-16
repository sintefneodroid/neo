#!/usr/bin/env python3
# coding=utf-8
__author__ = 'cnheider'

import datetime
import os

from setuptools import find_packages, setup

packages = find_packages(exclude=['neodroid/environments'])
package_data = {
  'neodroid': ['environments/grid_world*',
               # glob.glob('environments/**', recursive=True)
               ],
  }

def get_readme():
    with open('README.md') as f:
        return f.read()
    return ''

def get_keyword():
    with open('KEYWORDS') as f:
        return f.read()
    return ''

def version():
  version = os.getenv('VERSION', None)
  if version:
    # Most git tags are prefixed with 'v' (example: v1.2.3) this is
    # never desirable for artifact repositories, so we strip the
    # leading 'v' if it's present.
    return version[1:] if version.startswith('v') else version
  else:
    # Default version is an ISO8601 compiliant datetime. PyPI doesn't allow
    # the colon ':' character in its versions, and time is required to allow
    # for multiple publications to master in one day. This datetime string
    # uses the "basic" ISO8601 format for both its date and time components
    # to avoid issues with the colon character (ISO requires that date and
    # time components of a date-time string must be uniformly basic or
    # extended, which is why the date component does not have dashes.
    #
    # Publications using datetime versions should only be made from master
    # to represent the HEAD moving forward.
    version = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    print(f'VERSION environment variable not set, using datetime instead: {version}')

  return version


setup(
    name='Neodroid',
    version=version(),
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
    install_requires=['pyzmq',
                      'numpy',
                      'neodroid-flatbuffers',
                      'Pillow',
                      'gym'],
    extras_require={
      'GUI': ['kivy']
      }
    )
