# coding=utf-8
import neodroid.wrappers.formal_wrapper as neo
from neodroid import Configuration
import numpy as np
import json


def main():
  _environment = neo.make('3d_grid_world_win', connect_to_running=True)
  _environment.seed(42)

  for i in range(1000):

    observations, info = _environment.configure()
    while info.get_interrupted():
      print('Configuring')
      configuration = sample_initial_state(info, i)
      print(configuration)
      observations, info = _environment.configure(configuration)
      _,_,_,info=_environment.act()

    for j in range(1000):
      actions = _environment.sample_action_space(binary=True, discrete=True)
      _, reward, interrupted, info = _environment.act(actions)
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


if __name__ == '__main__':
  main()
