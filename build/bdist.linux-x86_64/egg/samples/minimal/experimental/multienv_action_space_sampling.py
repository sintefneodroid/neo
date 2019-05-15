#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from neodroid.models import ReactionParameters, Motion, Reaction

__author__ = 'cnheider'

import neodroid.neodroid_environments as neo


def construct_reactions(env):
  parameters = ReactionParameters(terminable=True, step=True, reset=False, configure=False,
                                  describe=False, episode_count=True)
  action1, action2 = env.action_space.sample()
  motions = [Motion('ActorActor', 'ActorTransformX_', action1),
             Motion('ActorActor', 'ActorTransformZ_', action2)]
  reactions = [Reaction(environment_name=f'EnvironmentPrototypingEnvironment',
                        parameters=parameters,
                        motions=motions)]

  for i in range(19):
    action1, action2 = env.action_space.sample()
    motions = [Motion('ActorActor', 'ActorTransformX_', action1),
               Motion('ActorActor', 'ActorTransformZ_', action2)]

    reaction = Reaction(environment_name=f'Environment(Clone){i}PrototypingEnvironment',
                        parameters=parameters,
                        motions=motions)
    reactions.append(reaction)

  return reactions


def main():
  _environments = neo.NeodroidEnvironment(name='multienv', connect_to_running=True)

  while _environments.is_connected:
    reactions = construct_reactions(_environments)
    states = _environments.react(reactions)


if __name__ == '__main__':
  main()
