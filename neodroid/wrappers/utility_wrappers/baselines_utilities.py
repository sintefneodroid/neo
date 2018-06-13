from baselines.common.atari_wrappers import make_atari, wrap_deepmind


def make_env(env_name, rank, seed):
  env = make_atari(env_name)
  env.seed(seed + rank)
  env = wrap_deepmind(env, episode_life=False, clip_rewards=False)
  return env
