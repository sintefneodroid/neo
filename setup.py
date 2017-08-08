from setuptools import setup, find_packages
import glob
setup(
    name='Neodroid',
    version=0.1,
    packages=find_packages(),

    package_data={
        'neodroid': ['environments/**','environments/*/*','environments/*/*/*','environments/*/*/*/*','environments/*/*/*/*/*','environments/*/*/*/*/*/*','environments/*/*/*/*/*/*/*'],
    },

    author='Christian Heider Nielsen',
    author_email='chrini13@student.aau.dk',
    description='Neodroid interface',
    long_description='Python interface for the Neodroid platform, an API for communicating with a Unity Game process for a feedback response loop',
    license='Apache License, Version 2.0',
    keywords='python reinforcement-learning interface api',
    url='https://github.com/sintefneodroid/neo',
)