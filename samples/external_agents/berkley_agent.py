#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 10/01/2020
           """

import gym
import torch
from garage.np.baselines import LinearFeatureBaseline
from garage.tf.algos import PPO
from garage.tf.envs import TfEnv
from garage.tf.policies import GaussianMLPPolicy
from torch.nn import functional as F  # NOQA

from garage.envs import normalize
from garage.envs.base import GarageEnv
from garage.experiment import LocalRunner, run_experiment
from garage.np.exploration_strategies import OUStrategy
from garage.replay_buffer import SimpleReplayBuffer
from garage.torch.algos import DDPG
from garage.torch.policies import DeterministicMLPPolicy
from garage.torch.q_functions import ContinuousMLPQFunction

from garage.experiment import run_experiment
from garage.np.baselines import LinearFeatureBaseline
from garage.tf.algos import TRPO
from garage.tf.envs import TfEnv
from garage.tf.experiment import LocalTFRunner
from garage.tf.policies import CategoricalMLPPolicy

# ENV = 'LunarLander-v2'
ENV = "CartPole-v1"


def run_ddpg(snapshot_config, *_):
    """Set up environment and algorithm and run the task.
  Args:
      snapshot_config (garage.experiment.SnapshotConfig): The snapshot
          configuration used by LocalRunner to create the snapshotter.
          If None, it will create one with default settings.
      _ : Unused parameters
  """
    runner = LocalRunner(snapshot_config)
    env = GarageEnv(normalize(gym.make(ENV)))

    action_noise = OUStrategy(env.spec, sigma=0.2)

    policy = DeterministicMLPPolicy(
        env_spec=env.spec,
        hidden_sizes=[64, 64],
        hidden_nonlinearity=F.relu,
        output_nonlinearity=torch.tanh,
    )

    qf = ContinuousMLPQFunction(
        env_spec=env.spec, hidden_sizes=[64, 64], hidden_nonlinearity=F.relu
    )

    replay_buffer = SimpleReplayBuffer(
        env_spec=env.spec, size_in_transitions=int(1e6), time_horizon=100
    )

    policy_optimizer = (torch.optim.Adagrad, {"lr": 1e-4, "lr_decay": 0.99})

    ddpg = DDPG(
        env_spec=env.spec,
        policy=policy,
        qf=qf,
        replay_buffer=replay_buffer,
        n_epoch_cycles=20,
        n_train_steps=50,
        min_buffer_size=int(1e4),
        exploration_strategy=action_noise,
        target_update_tau=1e-2,
        discount=0.9,
        optimizer=policy_optimizer,
    )

    runner.setup(algo=ddpg, env=env)

    runner.train(n_epochs=500, batch_size=100)


def run_ppo(snapshot_config, *_):
    """Set up environment and algorithm and run the task.
  Args:
      snapshot_config (garage.experiment.SnapshotConfig): The snapshot
          configuration used by LocalRunner to create the snapshotter.
          If None, it will create one with default settings.
      _ : Unused parameters
  """
    env = TfEnv(env_name=ENV)

    runner = LocalRunner(snapshot_config)

    policy = GaussianMLPPolicy(
        env.spec,
        hidden_sizes=[64, 64],
        hidden_nonlinearity=torch.tanh,
        output_nonlinearity=None,
    )

    baseline = LinearFeatureBaseline(env_spec=env.spec)

    algo = PPO(
        env_spec=env.spec,
        policy=policy,
        baseline=baseline,
        max_path_length=100,
        discount=0.99,
        center_adv=False,
    )

    runner.setup(algo, env)
    runner.train(n_epochs=100, batch_size=10000)


def run_tpro(snapshot_config, *_):
    """Wrap TRPO training task in the run_task function."""
    with LocalTFRunner(snapshot_config=snapshot_config) as runner:
        env = TfEnv(env_name=ENV)

        policy = CategoricalMLPPolicy(
            name="policy", env_spec=env.spec, hidden_sizes=(32, 32)
        )

        baseline = LinearFeatureBaseline(env_spec=env.spec)

        algo = TRPO(
            env_spec=env.spec,
            policy=policy,
            baseline=baseline,
            max_path_length=100,
            discount=0.99,
            max_kl_step=0.01,
        )

        runner.setup(algo, env)
        runner.train(n_epochs=100, batch_size=4000)


if __name__ == "__main__":

    run_experiment(run_tpro, snapshot_mode="last", seed=1)
