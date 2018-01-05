# coding=utf-8

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('lunarlander', connect_to_running=True)
  _environment.seed(42)

  for i in range(1000):
    _, info = _environment.configure()
    _environment.act()
    for j in range(100):
      actions = _environment.action_space.discrete_binary_one_hot_sample()
      _, reward, terminated, info = _environment.act(actions)
      if terminated:
        print('Interrupted', reward)
        break

  _environment.close()


if __name__ == '__main__':
  main()
