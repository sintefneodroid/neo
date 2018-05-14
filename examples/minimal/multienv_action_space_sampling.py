#!/usr/bin/env python3
# coding=utf-8
from neodroid.models import Reaction, Motion, ReactionParameters

__author__ = 'cnheider'

import neodroid.neodroid_environments as neo

def construct_reactions(env):

  reactions = []

  for i in range(19):
    action1,action2 = env.action_space.sample()
    action1 = float(action1[0])
    action2 = float(action2[0])
    motions = [Motion('ActorActor','ActorTransformX_',action1),
                                                        Motion('ActorActor','ActorTransformZ_',action2)]
    parameters = ReactionParameters(terminable=True, step=True, reset=False, configure=False,
                                      describe=False, episode_count=True)
    reaction = Reaction(environment_name=f'Environment(Clone){i}PrototypingEnvironment',
                        parameters=parameters,
                        motions=motions)
    reactions.append(reaction)

  return reactions


def main():
  _environment = neo.NeodroidEnvironments(connect_to_running=True)

  while _environment.is_connected:
    reactions = construct_reactions(_environment)
    states = _environment.react(reactions)


if __name__ == '__main__':
  main()
