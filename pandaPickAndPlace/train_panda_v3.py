from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym
import panda_gym

# 8 个并行环境，每次收集 16384 步经验，多样性远超单环境
env = make_vec_env("PandaPickAndPlaceDense-v3", n_envs=8)

model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    tensorboard_log="./ppo_logs/",
    policy_kwargs=dict(net_arch=[512, 512]),
    # 大幅提升探索，给策略"试错"的空间
    ent_coef=0.1,
    # 学习率从 3e-4 线性衰减到 0，前期快学后期稳
    learning_rate=lambda f: 3e-4 * f,
    # clip_range 也衰减，前期允许大更新，后期精细调整
    clip_range=lambda f: 0.2 * f,
    n_steps=2048,       # 每环境 2048 步，8 环境 = 16384 步/更新
    n_epochs=20,        # 每批数据多学几轮
    batch_size=512,     # 更大 batch
    gamma=0.995,        # 更看重远期奖励（抓取放下的奖励在后面）
    gae_lambda=0.98,    # 优势估计更平滑
)

model.learn(
    total_timesteps=10_000_000,
    progress_bar=True,
    tb_log_name="pickandplace_exp3"
)

model.save("model/best_ppo_panda_pickandplace_v3")

env.close()
