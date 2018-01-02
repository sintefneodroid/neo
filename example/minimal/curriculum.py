# coding=utf-8
import neodroid.wrappers.curriculum_wrapper as neo

random_motion_horizon = 5
memory = []
starts = []


def main():
  _environment = neo.make('3d_grid_world2', connect_to_running=True)
  _environment.seed(42)

  #observations, info = _environment.configure()
  #memory.append(info.get_state_configuration())
  memory.append(_environment.generate_inital_states())
  for i in range(1000):
    #interrupted = True
    #while interrupted:
    configuration = sample_initial_state(memory, i).get_state_configuration()
    _environment.configure(configuration)
    #  _environment.run_brownian_motion(5)
    #  _,_,interrupted,_ = _environment.observe()
    #  print(interrupted)


    for j in range(1000):
      actions = [1]
      observations, reward, interrupted, info = _environment.act(actions)
      memory.append(info)
      if interrupted:
        print('Interrupted', reward)
        break

  # _environment.render(close=True)
  _environment.close()


def sample_initial_state(memory, i=0):
  return memory[i]


if __name__ == '__main__':
  main()
