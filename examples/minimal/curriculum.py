# coding=utf-8
import neodroid.wrappers.curriculum_wrapper as neo

random_motion_horizon = 5
memory = []
starts = []


def main():
  _environment = neo.make('3d_grid_world', connect_to_running=True)
  _environment.seed(42)

  memory.extend(_environment.generate_inital_states(4,5))
  for i in range(1000):
    terminated = True
    while terminated:
      init = sample_initial_state(memory, i)
      _environment.configure(init)
      _environment.run_brownian_motion(5)
      _,_,terminated,info = _environment.observe()
      if not terminated:
        memory.append(info)

    for j in range(1000):
      actions = _environment.action_space.sample()
      observations, reward, terminated, info = _environment.act(actions)
      if terminated:
        print('Interrupted', reward)
        break

  _environment.close()

def sample_initial_state(memory, i=0):
  return memory[i]


if __name__ == '__main__':
  main()
