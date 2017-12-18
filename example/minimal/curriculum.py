# coding=utf-8
import neodroid.wrappers.formal_wrapper as neo
from neodroid import Configuration
import numpy as np
import json

random_motion_horizon = 5
memory = []

def main():
  _environment = neo.make('3d_grid_world2', connect_to_running=True)
  _environment.seed(42)

  observations, info = _environment.configure()
  memory.append(observations)
  for i in range(1000):
    interrupted=True
    while interrupted:
      configuration = sample_initial_state3(memory, i)
      observations, info = _environment.configure(configuration)
      for j in range(random_motion_horizon):
        actions = _environment.sample_action_space(binary=True, discrete=True)
        _,_,interrupted,info=_environment.act(actions)

    for j in range(1000):
      actions = _environment.sample_action_space(binary=True, discrete=True)
      observations, reward, interrupted, info = _environment.act(actions)
      memory.append(observations)
      if interrupted:
        print('Interrupted', reward)
        break

  # _environment.render(close=True)
  _environment.close()


def sample_initial_state(info, i=1, reward=0):
  a = json.loads(info.get_observer(b'EnvironmentBoundingBox').get_data(

  ).getvalue())
  max_x,min_x = (max(a['_top_front_left'][0],a['_bottom_back_right'][0]),min(a['_top_front_left'][0],a['_bottom_back_right'][0]))
  max_y,min_y = (max(a['_top_front_left'][1],a['_bottom_back_right'][1]),min(a['_top_front_left'][1],a['_bottom_back_right'][1]))
  max_z,min_z = (max(a['_top_front_left'][2],a['_bottom_back_right'][2]),
  min(a['_top_front_left'][2], a['_bottom_back_right'][2]))
  x, y, z = info.get_observer(b'GoalObserver').get_position()
  rot_x, rot_y, rot_z = info.get_observer(b'GoalObserver').get_rotation()
  px, py, pz = (np.random.random_sample(3) - 0.5) * (i%10) + 1
  return [Configuration('PlayerTransformX', max(min_x,min(x + px, max_x))),
          Configuration('PlayerTransformY', max(min_y,min(y + py, max_y))),
          Configuration('PlayerTransformZ', max(min_z,min(z + pz, max_z)))]


def sample_initial_state2(memory, i=0):
  position = memory[i].get_observer(b'PlayerObserver').get_position()
  return [Configuration('PlayerTransformX', position[0]),
          Configuration('PlayerTransformY', position[1]),
          Configuration('PlayerTransformZ', position[2])]

def sample_initial_state3(memory, i=0):
  return memory[i]


if __name__ == '__main__':
  main()
