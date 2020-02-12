__all__ = ["reverse_normalise_action", "normalise_action"]


def reverse_normalise_action(self, action):
    act_k_inv = 2.0 / (self.action_space.high - self.action_space.low)
    act_b = (self.action_space.high + self.action_space.low) / 2.0
    return act_k_inv * (action - act_b)


def normalise_action(action, motion_space):
    act_k = (motion_space.max_unnorm - motion_space.min_unnorm) / 2.0
    act_b = (motion_space.max_unnorm + motion_space.min_unnorm) / 2.0
    return act_k * action + act_b
