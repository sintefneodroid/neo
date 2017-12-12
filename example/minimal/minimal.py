# coding=utf-8
import neodroid.wrappers.formal_wrapper as neo
from neodroid import Configuration


def main():

  _environment = neo.make('3d_grid_world_win', connect_to_running=False)
  _environment.seed(42)

  for i in range(1000):

    observations, info = _environment.configure([Configuration('PlayerTransformY',i%6),Configuration('PlayerTransformX',-(i%3)),Configuration('PlayerTransformZ',-(i%3))])
    for j in range(100):
      actions = _environment.sample_action_space(binary=True,discrete=True)
      _, reward, interrupted, info = _environment.act(actions)
      if interrupted:
        print('Interrupted',reward)
        break

  #_environment.render(close=True)
  _environment.close()


if __name__ == '__main__':
  main()