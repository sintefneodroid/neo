from neodroid.models import Reaction, Motion

def verify_reaction(input_reaction, actors):
  if actors:
    if isinstance(input_reaction, Reaction):
      is_valid_motions = all(isinstance(m, Motion) for m in
                             input_reaction.get_motions())
      if is_valid_motions:
        return input_reaction
      else:
        input_reaction.set_motions(construct_motion_from_list(
            input_reaction.get_motions(), actors))
        return input_reaction
    elif isinstance(input_reaction, list):
      is_valid_motions = all(isinstance(m, Motion) for m in
                             input_reaction)
      if is_valid_motions:
        return Reaction(False, input_reaction)
      else:
        return construct_reaction_from_list(input_reaction, actors)
    else:
      return Reaction(False, [])
  else:
    return Reaction(False, [])

def construct_reaction_from_list(input_list, actors):
  motions = construct_motion_from_list(input_list, actors)
  return Reaction(False, motions)

def construct_motion_from_list(input_list, actors):
  actor_motor_tuples = [(actor.get_name(), motor.get_name())
                        for actor in actors
                        for motor in actor.get_motors().values()]
  new_motions = [Motion(actor_motor_tuple[0], actor_motor_tuple[1], list_val)
                 for (list_val, actor_motor_tuple) in
                 zip(input_list, actor_motor_tuples)]
  return new_motions