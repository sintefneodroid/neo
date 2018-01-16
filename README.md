![neodroid](images/header.png)

# Neo
Neo is a python package that enables deserialisation and an interface to the [Droid](https://github.com/sintefneodroid/droid) counterpart of the [Neodroid](https://github.com/sintefneodroid) platform

This project is very similar to Unity's own project [Unity Machine Learning Agents](https://github.com/Unity-Technologies/ml-agents). The alot of the efforts done in this project was made prior to their announcement, [Introducing: Unity Machine Learning Agents](https://blogs.unity3d.com/2017/09/19/introducing-unity-machine-learning-agents/). The entire Neodroid platform served and still serves as a tool for academic research specific to the authors interests, hence explaining to the existence and future direction of this project.

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
![neo](images/neo.png)

<!---
## Screenshots
-->

# To Do's
- [ ] Be able to select and/or parameterise an objective/evaluation (None,ReachGoal,Stabilise,..) function for an environment

# Other Components Of the Neodroid Platform

- [agent](https://github.com/sintefneodroid/agent)
- [simulation](https://github.com/sintefneodroid/simulation)
- [droid](https://github.com/sintefneodroid/droid)

# FAQ
- My iteration per second are maxed out at ~60
  - Ensure that you have disabled vsync, for optimus users you can use ```vblank_mode=0 optirun ..```.

## Other Problems
Please contact us or add an issue if have a problem that is not listed in the FAQ
