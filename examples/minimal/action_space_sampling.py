# coding=utf-8

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('lunarlander', connect_to_running=True)
  _environment.seed(42)

  for i in range(1000):
    _, info = _environment.configure()
    _environment.act()
    for j in range(_environment.get_environment_description().get_max_episode_length()):
      actions = _environment.action_space.sample()
      _, reward, terminated, info = _environment.act(actions)
      if terminated:
        print('Interrupted', reward)
        break

  _environment.close()


if __name__ == '__main__':
  main()
