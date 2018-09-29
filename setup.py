#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from NeodroidPackage import NeodroidPackage

__author__ = 'cnheider'

from setuptools import setup

if __name__ == '__main__':

  neo_pkg = NeodroidPackage()

  setup(
      name=neo_pkg.package_name,
      version=neo_pkg.version,
      packages=neo_pkg.packages,
      package_data=neo_pkg.package_data,
      author=neo_pkg.author_name,
      author_email=neo_pkg.author_email,
      maintainer=neo_pkg.maintainer_name,
      maintainer_email=neo_pkg.maintainer_email,
      description=neo_pkg.description,
      license=neo_pkg.license,
      keywords=neo_pkg.keyword,
      url=neo_pkg.url,
      download_url=neo_pkg.download_url,
      install_requires=neo_pkg.requirements,
      extras_require=neo_pkg.extras,
      entry_points=neo_pkg.entry_points,
      classifiers=neo_pkg.classifiers,
      long_description_content_type=neo_pkg.readme_type,
      long_description=neo_pkg.readme,
      tests_require=neo_pkg.test_dependencies,
      include_package_data=True,
      python_requires='>=3'
      )
