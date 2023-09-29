#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pkg_resources
from warg import package_is_editable, get_version, clean_string

try:
    from importlib.resources import files
    from importlib.metadata import PackageNotFoundError
except:
    from importlib_metadata import PackageNotFoundError
    from importlib_resources import files

from apppath import AppPath

__project__ = "Neodroid"
__author__ = "Christian Heider Nielsen"
__version__ = "0.5.0"
__doc__ = r"""
Created on 27/04/2019

@author: cnheider

.. module:: neodroid
   :platform: Unix, Windows
   :synopsis: An API for communicating with a Unity Game process.

.. moduleauthor:: Christian Heider Nielsen <christian.heider@alexandra.dk>


"""
__all__ = ["PROJECT_APP_PATH", "PROJECT_NAME", "PROJECT_VERSION"]

PROJECT_NAME = clean_string(__project__)
PROJECT_YEAR = 2018
PROJECT_VERSION = __version__
PROJECT_AUTHOR = clean_string(__author__)
PROJECT_ORGANISATION = clean_string("Neodroid")
PROJECT_APP_PATH = AppPath(app_name=PROJECT_NAME, app_author=PROJECT_AUTHOR)
PACKAGE_DATA_PATH = Path(pkg_resources.resource_filename(PROJECT_NAME, "data"))
INCLUDE_PROJECT_READMES = False
DEFAULT_ENVIRONMENTS_PATH = (PROJECT_APP_PATH.user_cache / "environments").absolute()

try:
    DEVELOP = package_is_editable(PROJECT_NAME)
except PackageNotFoundError as e:
    DEVELOP = True

__version__ = get_version(__version__, append_time=DEVELOP)

__version_info__ = tuple(int(segment) for segment in __version__.split("."))


def get_logo() -> str:
    with open("data/.ascii") as f:
        return f.read()


def draw_logo() -> None:
    print(get_logo())


# from .environments import *

if __name__ == "__main__":
    draw_logo()
