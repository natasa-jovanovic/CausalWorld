from causal_world.stable_baselines.deepq.policies import MlpPolicy, CnnPolicy, LnMlpPolicy, LnCnnPolicy
from causal_world.stable_baselines.deepq.build_graph import build_act, build_train  # noqa
from causal_world.stable_baselines.deepq.dqn import DQN
from causal_world.stable_baselines.common.buffers import ReplayBuffer, PrioritizedReplayBuffer  # noqa


def wrap_atari_dqn(env):
    """
    wrap the environment in atari wrappers for DQN

    :param env: (Gym Environment) the environment
    :return: (Gym Environment) the wrapped environment
    """
    from causal_world.stable_baselines.common.atari_wrappers import wrap_deepmind
    return wrap_deepmind(env, frame_stack=True, scale=False)
