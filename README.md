<!--![header](.github/images/header.png)-->

<p align="center">
  <img src=".github/images/header.png" alt='header' />
</p>

<h1 align="center">Neo</h1>

<!--# Neo-->

Neo is a python package that enables deserialisation, serialisation and an interface to the [Droid](https://github.com/sintefneodroid/droid) counterpart of the [Neodroid](https://github.com/sintefneodroid) platform.

---

_[Neodroid](https://github.com/sintefneodroid) is developed with support from Research Council of Norway Grant #262900. ([https://www.forskningsradet.no/prosjektbanken/#/project/NFR/262900](https://www.forskningsradet.no/prosjektbanken/#/project/NFR/262900))_

---

<table>
  <tr>
    <td>
      <a href='https://travis-ci.org/sintefneodroid/neo'>
        <img src='https://travis-ci.org/sintefneodroid/neo.svg?branch=master' alt='Build Status' />
      </a>
    </td>
    <td>
      <a href='https://coveralls.io/github/sintefneodroid/neo?branch=master'>
        <img src='https://coveralls.io/repos/github/sintefneodroid/neo/badge.svg?branch=master' alt='Coverage Status' />
      </a>
    </td>
    <td>
      <a href='https://github.com/sintefneodroid/neo/issues'>
        <img src='https://img.shields.io/github/issues/sintefneodroid/neo.svg?style=flat' alt='GitHub Issues' />
      </a>
    </td>
    <td>
      <a href='https://documentation.neodroid.ml/?badge=latest'>
        <img src='https://readthedocs.org/projects/neodroid/badge/?version=latest' alt='Documentation Status' />
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <a href='https://github.com/sintefneodroid/neo/network'>
        <img src='https://img.shields.io/github/forks/sintefneodroid/neo.svg?style=flat' alt='GitHub Forks' />
      </a>
    </td>
      <td>
      <a href='https://github.com/sintefneodroid/neo/stargazers'>
        <img src='https://img.shields.io/github/stars/sintefneodroid/neo.svg?style=flat' alt='GitHub Stars' />
      </a>
    </td>
      <td>
      <a href='https://github.com/sintefneodroid/neo/blob/master/LICENSE.md'>
        <img src='https://img.shields.io/github/license/sintefneodroid/neo.svg?style=flat' alt='GitHub License' />
      </a>
    </td>
    <td>
      <a href="https://pyup.io/repos/github/sintefneodroid/neo/">
        <img src="https://pyup.io/repos/github/sintefneodroid/neo/python-3-shield.svg" alt="Python 3" />
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <a href='https://pypi.python.org/pypi/Neodroid'>
        <img src='https://pypip.in/v/neodroid/badge.png' alt='Pypi Version' />
      </a>
    </td>
      <td>
      <a href='https://pypi.python.org/pypi/Neodroid'>
        <img src='https://pypip.in/d/neodroid/badge.png' alt='Pypi Downloads' />
      </a>
    </td>
    <td>
      <a href='https://pypi.python.org/pypi/Neodroid'>
        <img src='https://pypip.in/wheel/neodroid/badge.png' alt='Pypi Wheel' />
      </a>
    </td>
    <td>
      <a href="https://pyup.io/repos/github/sintefneodroid/neo/">
        <img src="https://pyup.io/repos/github/sintefneodroid/neo/shield.svg" alt="Updates" />
      </a>
    </td>
  </tr>
</table>

<p align="center" width="100%">
  <a href="https://www.python.org/">
  <img alt="python" src="https://raw.githubusercontent.com/sintefneodroid/neo/master/.github/images/python.svg" height="40" align="left">
  </a>
  <a href="https://github.com/google/flatbuffers">
  <img alt="flatbuffers" src="https://raw.githubusercontent.com/sintefneodroid/neo/master/.github/images/flatbuffers.svg" height="40"  align="center">
  </a>
  <a href="https://github.com/zeromq/pyzmq" >
  <img alt="pyzmq" src="https://media.githubusercontent.com/media/sintefneodroid/neo/master/.github/images/pyzmq.png" height="40" align="right">
  </a>
</p>

## Installation
```bash
pip3 install -U neodroid
```

## Usage
```py
import neodroid as neo
```

<!---
 ## Features
-->

## Examples
We have included some  example applications in this repository.

### Observation Generator

### Random Agent

### Curriculum

### An Example Implementation Of Using An Interface

The application displays data received from the example application of the [Droid](https://github.com/sintefneodroid/droid) project repository.
![neo](.github/images/neo.png)

<!---
## Screenshots
-->

# To Do's
- [ ] Be able to select and/or parameterise an objective/evaluation (None,ReachGoal,Stabilise,..) function for an environment


# Contributing
See guidelines for contributing [here](.github/CONTRIBUTING.md).

# Licensing

This project is licensed under the Apache V2 License. See [LICENSE](LICENSE.md) for more information.

# Citation

For citation you may use the following bibtex entry:
````
@misc{neodroid,
  author = {Heider, Christian},
  title = {Neodroid Platform},
  year = {2018},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/sintefneodroid}},
}
````
# Other Components Of the Neodroid Platform

- [agent](https://github.com/sintefneodroid/agent)
- [simulation](https://github.com/sintefneodroid/simulation)
- [droid](https://github.com/sintefneodroid/droid)

# FAQ
- My iterations per second are maxed out at ~60..
  - Ensure that you have disabled vsync, for bumblebee users on linux you can use ```vblank_mode=0 optirun ..```.
- Why was this tool created, what does it serve and not just use Unity's own RL framework?
  - This project is very similar to Unity's own project [Unity Machine Learning Agents](https://github.com/Unity-Technologies/ml-agents). The most of the efforts done in this project were made prior to their announcement, [Introducing: Unity Machine Learning Agents](https://blogs.unity3d.com/2017/09/19/introducing-unity-machine-learning-agents/). The entire Neodroid platform served and still serves as a tool for academic research specific to the authors interests, hence explaining to the existence and future direction of this project.

## Other Problems
Please contact us or add an issue if have a problem that is not listed in the FAQ

# Authors

* **Christian Heider Nielsen** - [cnheider](https://github.com/cnheider)

Here other [contributors](https://github.com/sintefneodroid/neo/contributors) to this project are listed.
