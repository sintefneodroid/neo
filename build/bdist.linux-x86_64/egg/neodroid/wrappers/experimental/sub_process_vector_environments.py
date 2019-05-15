from multiprocessing import Pipe, Process

import numpy as np

from neodroid.wrappers.experimental.cloud_pickle_wrapper import CloudPickleWrapper
from neodroid.wrappers.experimental.vector_environments import VectorEnvironments


def worker(remote, parent_remote, env_fn_wrapper):
  parent_remote.close()
  env = env_fn_wrapper.x()
  while True:
    cmd, data = remote.recv()
    if cmd == 'step':
      ob, reward, done, info = env.act(data)
      if done:
        ob = env.reset()
      remote.send((ob, reward, done, info))
    elif cmd == 'reset':
      ob = env.reset()
      remote.send(ob)
    elif cmd == 'reset_task':
      ob = env.reset_task()
      remote.send(ob)
    elif cmd == 'close':
      remote.close()
      break
    elif cmd == 'get_spaces':
      remote.send((env.action_space, env.observation_space))
    elif cmd == 'render':
      env.render()
    else:
      raise NotImplementedError


class SubProcessVectorEnvironments(VectorEnvironments):
  def __init__(self, env_fns, render_interval):
    """ Minor addition to SubprocVecEnv, automatically renders environments
    envs: list of gym environments to run in subprocesses
    """
    self.closed = False
    nenvs = len(env_fns)
    self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nenvs)])
    self.ps = [Process(target=worker, args=(work_remote, remote, CloudPickleWrapper(env_fn)))
               for (work_remote, remote, env_fn) in zip(self.work_remotes, self.remotes, env_fns)]
    for p in self.ps:
      p.daemon = True  # if the main process crashes, we should not cause things to hang
      p.start()
    for remote in self.work_remotes:
      remote.close()

    self.remotes[0].send(('get_spaces', None))
    self.action_space, self.observation_space = self.remotes[0].recv()

    self.render_interval = render_interval
    self.render_timer = 0

  def step(self, actions):
    for remote, action in zip(self.remotes, actions):
      remote.send(('step', action))
    results = [remote.recv() for remote in self.remotes]
    obs, rews, dones, info = zip(*results)

    self.render_timer += 1
    if self.render_timer == self.render_interval:
      for remote in self.remotes:
        remote.send(('render', None))
      self.render_timer = 0

    return np.stack(obs), np.stack(rews), np.stack(dones), info

  def reset(self):
    for remote in self.remotes:
      remote.send(('reset', None))
    return np.stack([remote.recv() for remote in self.remotes])

  def reset_task(self):
    for remote in self.remotes:
      remote.send(('reset_task', None))
    return np.stack([remote.recv() for remote in self.remotes])

  def close(self):
    if self.closed:
      return

    for remote in self.remotes:
      remote.send(('close', None))
    for p in self.ps:
      p.join()
    self.closed = True

  @property
  def num_envs(self):
    return len(self.remotes)
