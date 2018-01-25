from setuptools import setup, find_packages

packages = find_packages(exclude=['neodroid/environments'])
package_data = {
      'neodroid': ['environments/grid_world*',
                   #glob.glob('environments/**', recursive=True)
                   ],
    }

setup(
    name='Neodroid',
    version=0.3,
    packages=packages,
    include_package_data=True,
    #package_data=package_data,
    author='Christian Heider Nielsen',
    author_email='chrini13@student.aau.dk',
    description='Neodroid interface',
    long_description='Python interface for the Neodroid platform, '
                     'an API for communicating with a Unity '
                     'Game process for a feedback response loop',
    license='Apache License, Version 2.0',
    keywords='python reinforcement-learning interface api',
    url='https://github.com/sintefneodroid/neo',
    install_requires=['pyzmq', 'numpy', 'flatbuffers', 'Pillow'],
    extras_require={
            'GUI': ['kivy']
        }
)
