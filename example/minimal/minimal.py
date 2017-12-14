# coding=utf-8
import neodroid.wrappers.formal_wrapper as neo
from neodroid import Configuration


def main():

  _environment = neo.make('3d_grid_world_win', connect_to_running=True)
  _environment.seed(42)

  for i in range(1000):

    observations, info = _environment.configure()
    x,y,z = info.get_observer(b'GoalObserver').get_position()
    rot_x,rot_y,rot_z = info.get_observer(b'GoalObserver').get_rotation()
    observations, info = _environment.configure([Configuration('PlayerTransformX',x),Configuration('PlayerTransformY',y+i%5),Configuration('PlayerTransformZ',z)])
    _environment.act()
    for j in range(1000):
      actions = _environment.sample_action_space(binary=True,discrete=True)
      _, reward, interrupted, info = _environment.act(actions)
      if interrupted:
        print('Interrupted',reward)
        break

  #_environment.render(close=True)
  _environment.close()


if __name__ == '__main__':
  main()