# coding=utf-8

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('grid_world', connect_to_running=False)

  while _environment.is_connected:
    actions = _environment.action_space.sample()
    _, reward, terminated, info = _environment.act(actions)

if __name__ == '__main__':
  main()
