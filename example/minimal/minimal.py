# coding=utf-8
import neodroid.wrappers.formal_wrapper as neo

def main():

  _environment = neo.make('attached_reacher_coordinates',connect_to_running=True)
  _environment.seed(42)

  observations, info = _environment.configure()
  for i in range(10000):
    actions = _environment.sample_action_space() * 100
    _, _, _, info = _environment.act(actions)

  _environment.render(close=True)
  _environment.close()


if __name__ == '__main__':
  main()
