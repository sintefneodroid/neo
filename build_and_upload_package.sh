#!/usr/bin/env bash
rm -rf dist build */*.egg-info *.egg-info
python2 setup.py bdist
python2 setup.py bdist_wheel
python3 setup.py bdist
python3 setup.py bdist_wheel
twine upload dist/*