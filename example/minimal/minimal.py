# coding=utf-8
import neodroid.wrappers.formal_wrapper as neo

def main():

  _environment = neo.make('3d_grid_world_win', connect_to_running=False)
  _environment.seed(42)

  observations, info = _environment.configure()
  for i in range(10000):
    actions = _environment.sample_action_space(binary=True,discrete=True)
    _, reward, interrupted, info = _environment.act(actions)
    if interrupted:
      #break
      print('Interrupted')

  #_environment.render(close=True)
  _environment.close()


if __name__ == '__main__':
  main()
