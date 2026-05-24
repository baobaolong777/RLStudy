import gymnasium as gym
import panda_gym
from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.her import HerReplayBuffer

# 4 个并行环境
env = make_vec_env("PandaPickAndPlaceDense-v3", n_envs=4)

model = SAC(
    "MultiInputPolicy",
    env,
    verbose=1,
    tensorboard_log="./sac_logs/",
    replay_buffer_class=HerReplayBuffer,
    replay_buffer_kwargs=dict(
        n_sampled_goal=4,
        goal_selection_strategy="future",
    ),
    buffer_size=500_000,
    batch_size=512,
    learning_rate=3e-4,
    tau=0.05,
    gamma=0.95,
    policy_kwargs=dict(net_arch=[256, 256, 256]),
    gradient_steps=-1,
    # HER 需要等第一个 episode 结束后才能采样
    learning_starts=1000,
)

model.learn(
    total_timesteps=2_000_000,
    progress_bar=True,
    tb_log_name="pickandplace_sac_her_exp1"
)

model.save("model/best_sac_her_panda_pickandplace_v1")
env.close()
