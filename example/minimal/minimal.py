# coding=utf-8

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('lunarlander', connect_to_running=True)
  _environment.seed(42)

  for i in range(1000):
    _, info = _environment.configure()
    _environment.act()
    for j in range(100):
      actions = _environment.sample_action_space()
      _, reward, interrupted, info = _environment.act(actions)
      if interrupted:
        print('Interrupted', reward)
        break

  _environment.close()


if __name__ == '__main__':
  main()
