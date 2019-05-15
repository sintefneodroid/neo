#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import pickle
from abc import ABC, abstractmethod

import cloudpickle


class VecEnv(ABC):
  """
  An abstract asynchronous, vectorized environment.
  :param num_envs: (int) the number of environments
  :param observation_space: (Gym Space) the observation space
  :param action_space: (Gym Space) the action space
  """

  def __init__(self, num_envs, observation_space, action_space):
    self.num_envs = num_envs
    self.observation_space = observation_space
    self.action_space = action_space

  @abstractmethod
  def reset(self):
    """
    Reset all the environments and return an array of
    observations, or a tuple of observation arrays.
    If step_async is still doing work, that work will
    be cancelled and step_wait() should not be called
    until step_async() is invoked again.
    :return: ([int] or [float]) observation
    """
    pass

  @abstractmethod
  def step_async(self, actions):
    """
    Tell all the environments to start taking a step
    with the given actions.
    Call step_wait() to get the results of the step.
    You should not call this if a step_async run is
    already pending.
    """
    pass

  @abstractmethod
  def step_wait(self):
    """
    Wait for the step taken with step_async().
    :return: ([int] or [float], [float], [bool], dict) observation, reward, done, information
    """
    pass

  @abstractmethod
  def close(self):
    """
    Clean up the environment's resources.
    """
    pass

  def step(self, actions):
    """
    Step the environments with the given action
    :param actions: ([int] or [float]) the action
    :return: ([int] or [float], [float], [bool], dict) observation, reward, done, information
    """
    self.step_async(actions)
    return self.step_wait()

  def get_images(self):
    """
    Return RGB images from each environment
    """
    raise NotImplementedError

  def render(self, *args, **kwargs):
    """
    Gym environment rendering
    :param mode: (str) the rendering type
    """
    pass

  @property
  def unwrapped(self):
    if isinstance(self, VecEnvWrapper):
      return self.venv.unwrapped
    else:
      return self


class VecEnvWrapper(VecEnv):
  """
  Vectorized environment base class
  :param venv: (VecEnv) the vectorized environment to wrap
  :param observation_space: (Gym Space) the observation space (can be None to load from venv)
  :param action_space: (Gym Space) the action space (can be None to load from venv)
  """

  def __init__(self, venv, observation_space=None, action_space=None):
    self.venv = venv
    VecEnv.__init__(self, num_envs=venv.num_envs,
                    observation_space=observation_space or venv.observation_space,
                    action_space=action_space or venv.action_space)

  def step_async(self, actions):
    self.venv.step_async(actions)

  @abstractmethod
  def reset(self):
    pass

  @abstractmethod
  def step_wait(self):
    pass

  def close(self):
    return self.venv.close()

  def render(self, *args, **kwargs):
    return self.venv.render(*args, **kwargs)

  def get_images(self):
    return self.venv.get_images()


import numpy as np


class RunningMeanStd(object):
  def __init__(self, epsilon=1e-4, shape=()):
    """
    calulates the running mean and std of a data stream
    https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Parallel_algorithm
    :param epsilon: (float) helps with arithmetic issues
    :param shape: (tuple) the shape of the data stream's output
    """
    self.mean = np.zeros(shape, 'float64')
    self.var = np.ones(shape, 'float64')
    self.count = epsilon

  def update(self, arr):
    batch_mean = np.mean(arr, axis=0)
    batch_var = np.var(arr, axis=0)
    batch_count = arr.shape[0]
    self.update_from_moments(batch_mean, batch_var, batch_count)

  def update_from_moments(self, batch_mean, batch_var, batch_count):
    delta = batch_mean - self.mean
    tot_count = self.count + batch_count

    new_mean = self.mean + delta * batch_count / tot_count
    m_a = self.var * self.count
    m_b = batch_var * batch_count
    m_2 = m_a + m_b + np.square(delta) * self.count * batch_count / (self.count + batch_count)
    new_var = m_2 / (self.count + batch_count)

    new_count = batch_count + self.count

    self.mean = new_mean
    self.var = new_var
    self.count = new_count


class VecNormalize(VecEnvWrapper):
  """
  A moving average, normalizing wrapper for vectorized environment.
  has support for saving/loading moving average,

  :param venv: (VecEnv) the vectorized environment to wrap
  :param training: (bool) Whether to update or not the moving average
  :param norm_obs: (bool) Whether to normalize observation or not (default: True)
  :param norm_reward: (bool) Whether to normalize rewards or not (default: True)
  :param clip_obs: (float) Max absolute value for observation
  :param clip_reward: (float) Max value absolute for discounted reward
  :param gamma: (float) discount factor
  :param epsilon: (float) To avoid division by zero
  """

  def __init__(self, venv, training=True, norm_obs=True, norm_reward=True,
               clip_obs=10., clip_reward=10., gamma=0.99, epsilon=1e-8):
    VecEnvWrapper.__init__(self, venv)
    self.obs_rms = RunningMeanStd(shape=self.observation_space.shape)
    self.ret_rms = RunningMeanStd(shape=())
    self.clip_obs = clip_obs
    self.clip_reward = clip_reward
    # Returns: discounted rewards
    self.ret = np.zeros(self.num_envs)
    self.gamma = gamma
    self.epsilon = epsilon
    self.training = training
    self.norm_obs = norm_obs
    self.norm_reward = norm_reward
    self.old_obs = np.array([])

  def step_wait(self):
    """
    Apply sequence of actions to sequence of environments
    actions -> (observations, rewards, news)

    where 'news' is a boolean vector indicating whether each element is new.
    """
    obs, rews, news, infos = self.venv.step_wait()
    self.ret = self.ret * self.gamma + rews
    self.old_obs = obs
    obs = self._normalize_observation(obs)
    if self.norm_reward:
      if self.training:
        self.ret_rms.update(self.ret)
      rews = np.clip(rews / np.sqrt(self.ret_rms.var + self.epsilon), -self.clip_reward, self.clip_reward)
    self.ret[news] = 0
    return obs, rews, news, infos

  def _normalize_observation(self, obs):
    """
    :param obs: (numpy tensor)
    """
    if self.norm_obs:
      if self.training:
        self.obs_rms.update(obs)
      obs = np.clip((obs - self.obs_rms.mean) / np.sqrt(self.obs_rms.var + self.epsilon), -self.clip_obs,
                    self.clip_obs)
      return obs
    else:
      return obs

  def get_original_obs(self):
    """
    returns the unnormalized observation

    :return: (numpy float)
    """
    return self.old_obs

  def reset(self):
    """
    Reset all environments
    """
    obs = self.venv.reset()
    if len(np.array(obs).shape) == 1:  # for when num_cpu is 1
      self.old_obs = [obs]
    else:
      self.old_obs = obs
    self.ret = np.zeros(self.num_envs)
    return self._normalize_observation(obs)

  def save_running_average(self, path):
    """
    :param path: (str) path to log dir
    """
    for rms, name in zip([self.obs_rms, self.ret_rms], ['obs_rms', 'ret_rms']):
      with open("{}/{}.pkl".format(path, name), 'wb') as file_handler:
        pickle.dump(rms, file_handler)

  def load_running_average(self, path):
    """
    :param path: (str) path to log dir
    """
    for name in ['obs_rms', 'ret_rms']:
      with open("{}/{}.pkl".format(path, name), 'rb') as file_handler:
        setattr(self, name, pickle.load(file_handler))
