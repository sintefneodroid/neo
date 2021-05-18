__author__ = "Christian Heider Nielsen"
__doc__ = r"""
"""

__all__ = ["reverse_normalise_action", "normalise_action"]


from trolls.spaces import ActionSpace, Range


def reverse_normalise_action(*, action: float, action_space: ActionSpace) -> float:
    """

    TODO: INCONSISTENT ACTION SPACE AND RANGE ABSTRACTION LEVEL, normalise_action

    :param action:
    :type action:
    :return:
    :rtype:
    """
    act_k_inv = 2.0 / (action_space.high - action_space.low)
    act_b = (action_space.high + action_space.low) / 2.0
    return act_k_inv * (action - act_b)


def normalise_action(*, action: float, motion_space: Range) -> float:
    """

    TODO: INCONSISTENT ACTION SPACE AND RANGE ABSTRACTION LEVEL, reverse_normalise_action

    :param action:
    :type action:
    :param motion_space:
    :type motion_space:
    :return:
    :rtype:
    """
    act_k = (motion_space.max_unnorm - motion_space.min_unnorm) / 2.0
    act_b = (motion_space.max_unnorm + motion_space.min_unnorm) / 2.0
    return act_k * action + act_b
