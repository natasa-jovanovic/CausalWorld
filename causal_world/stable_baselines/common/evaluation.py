import typing
from typing import Callable, List, Optional, Tuple, Union

import gym
import numpy as np

from causal_world.stable_baselines.common.vec_env import VecEnv

if typing.TYPE_CHECKING:
    from causal_world.stable_baselines.common.base_class import BaseRLModel


def evaluate_policy(
    model: "BaseRLModel",
    env: Union[gym.Env, VecEnv],
    n_eval_episodes: int = 10,
    deterministic: bool = True,
    render: bool = False,
    callback: Optional[Callable] = None,
    reward_threshold: Optional[float] = None,
    return_episode_rewards: bool = False,
) -> Union[Tuple[float, float], Tuple[List[float], List[int]]]:
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param render: (bool) Whether to render the environment or not
    :param callback: (callable) callback function to do additional checks,
        called after each step.
    :param reward_threshold: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :param return_episode_rewards: (Optional[float]) If True, a list of reward per episode
        will be returned instead of the mean.
    :return: (float, float) Mean reward per episode, std of reward per episode
        returns ([float], [int]) when ``return_episode_rewards`` is True
    """
    if isinstance(env, VecEnv):
        assert env.num_envs == 1, "You must pass only one environment when using this function"

    is_recurrent = model.policy.recurrent

    episode_rewards, episode_lengths = [], []
    for i in range(n_eval_episodes):
        # Avoid double reset, as VecEnv are reset automatically
        if not isinstance(env, VecEnv) or i == 0:
            obs = env.reset()
            # Because recurrent policies need the same observation space during training and evaluation, we need to pad
            # observation to match training shape. See https://github.com/hill-a/stable-baselines/issues/1015
            if is_recurrent:
                zero_completed_obs = np.zeros((model.n_envs,) + model.observation_space.shape)
                zero_completed_obs[0, :] = obs
                obs = zero_completed_obs
        done, state = False, None
        episode_reward = 0.0
        episode_length = 0
        while not done:
            action, state = model.predict(obs, state=state, deterministic=deterministic)
            new_obs, reward, done, _info = env.step(action)
            if is_recurrent:
                obs[0, :] = new_obs
            else:
                obs = new_obs
            episode_reward += reward
            if callback is not None:
                callback(locals(), globals())
            episode_length += 1
            if render:
                env.render()
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    if reward_threshold is not None:
        assert mean_reward > reward_threshold, "Mean reward below threshold: {:.2f} < {:.2f}".format(mean_reward, reward_threshold)
    if return_episode_rewards:
        return episode_rewards, episode_lengths
    return mean_reward, std_reward
