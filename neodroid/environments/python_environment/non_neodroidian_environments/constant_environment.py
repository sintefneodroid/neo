import numpy
from gym import Env

from neodroid.utilities import Range, Space


class NoRenderEnv(Env):
    def render(self, mode="human"):
        """

        @param mode:
        @type mode:
        """
        pass


class ConstantEnvironment(NoRenderEnv):
    """

    """

    def __init__(self, n_obs=1, n_actions=1):

        ranges = [
            Range(min_value=0, max_value=1, decimal_granularity=0) for i in range(n_obs)
        ]
        self.action_space = Space(ranges)
        self.observation_space = Space(
            [
                Range(min_value=0, max_value=1, decimal_granularity=0)
                for i in range(n_actions)
            ]
        )

        self.obs = self.observation_space.sample()

        self.reset()

    def reset(self):
        """

        @return:
        @rtype:
        """
        self.obs = self.observation_space.sample()
        return self.obs

    def step(self, actions):
        """

        @param actions:
        @type actions:
        @return:
        @rtype:
        """
        if actions > 0:
            return self.obs, 0, True, {}

        return self.obs, 1, False, {}

    def act(self, a):
        """

        @param a:
        @type a:
        @return:
        @rtype:
        """
        return self.step(a)

    def react(self, a):
        """

        @param a:
        @type a:
        @return:
        @rtype:
        """
        return self.act(a)


class StatefulEnvironment(ConstantEnvironment):
    def reset(self):
        """

        @return:
        @rtype:
        """
        self.obs = self.observation_space.sample()
        return [self.obs]

    def step(self, actions):
        """

        @param actions:
        @type actions:
        @return:
        @rtype:
        """
        terminated = numpy.array_equal(self.obs, [actions])
        if isinstance(terminated, numpy.ndarray):
            terminated = terminated.all()

        self.obs = [actions]

        if terminated:
            return self.obs, 0, terminated, {}

        return self.obs, 1, terminated, {}


if __name__ == "__main__":
    env = StatefulEnvironment()
    obs = env.reset()
    total = 0
    for t in range(10000):
        ac = env.action_space.sample()
        obs, signal, term, info = env.step(ac)
        total += signal
        print(ac, obs, signal, term, total)
        if term:
            obs = env.reset()
            total = 0
