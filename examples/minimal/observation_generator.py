# coding=utf-8

import neodroid.wrappers.formal_wrapper as neo


def main():
  _environment = neo.make('lunarlander', connect_to_running=False)

  for (observation, reward, terminated, info) in _environment:
    if terminated:
      print('Interrupted', reward)

  _environment.close()


if __name__ == '__main__':
  main()
