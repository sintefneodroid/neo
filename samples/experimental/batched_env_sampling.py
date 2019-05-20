#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models import Motion, Reaction, ReactionParameters

__author__ = 'cnheider'

import neodroid.batched_neodroid_environments as neo


def construct_reactions(env, R):
  parameters = ReactionParameters(
      terminable=True,
      step=True,
      reset=R[0],
      configure=False,
      describe=False,
      episode_count=True)
  action1, action2 = env.action_space.sample()
  motions = [Motion('ActorActor', 'ActorTransformX_', action1),
             Motion('ActorActor', 'ActorTransformZ_', action2)]
  reactions = {f'EnvironmentPrototypingEnvironment':Reaction(
      environment_name=f'EnvironmentPrototypingEnvironment',
      parameters=parameters,
      motions=motions)
    }

  for i in range(19):

    parameters = ReactionParameters(
        terminable=True,
        step=True,
        reset=R[i + 1],
        configure=False,
        describe=False,
        episode_count=True)

    action1, action2 = env.action_space.sample()
    motions = [Motion('ActorActor', 'ActorTransformX_', action1),
               Motion('ActorActor', 'ActorTransformZ_', action2)]

    reaction = Reaction(environment_name=f'Environment(Clone){i}PrototypingEnvironment',
                        parameters=parameters,
                        motions=motions)
    reactions[f'Environment(Clone){i}PrototypingEnvironment'] = reaction

  out_reactions = {}
  for key in sorted(reactions.keys()):
    out_reactions[key] = reactions[key]

  return list(out_reactions.values())


def main():
  environments = neo.BatchedNeodroidEnvironment(connect_to_running=True)
  R = [False for _ in range(20)]
  while environments.is_connected:
    reactions = construct_reactions(environments, R)
    states, signals, terminated, info = environments.react(reactions)
    print(signals)
    print(terminated)
    R = environments.reset(terminated)


if __name__ == '__main__':
  main()
