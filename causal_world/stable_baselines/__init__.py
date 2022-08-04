import os
import warnings

from causal_world.stable_baselines.a2c import A2C
from causal_world.stable_baselines.acer import ACER
from causal_world.stable_baselines.acktr import ACKTR
from causal_world.stable_baselines.deepq import DQN
from causal_world.stable_baselines.her import HER
from causal_world.stable_baselines.ppo2 import PPO2
from causal_world.stable_baselines.td3 import TD3
from causal_world.stable_baselines.sac import SAC

# Load mpi4py-dependent algorithms only if mpi is installed.
try:
    import mpi4py
except ImportError:
    mpi4py = None

if mpi4py is not None:
    from causal_world.stable_baselines.ddpg import DDPG
    from causal_world.stable_baselines.gail import GAIL
    from causal_world.stable_baselines.ppo1 import PPO1
    from causal_world.stable_baselines.trpo_mpi import TRPO
del mpi4py

# Read version from file
version_file = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_file, "r") as file_handler:
    __version__ = file_handler.read().strip()


warnings.warn(
    "stable-baselines is in maintenance mode, please use [Stable-Baselines3 (SB3)](https://github.com/DLR-RM/stable-baselines3) for an up-to-date version. You can find a [migration guide](https://stable-baselines3.readthedocs.io/en/master/guide/migration.html) in SB3 documentation."
)
