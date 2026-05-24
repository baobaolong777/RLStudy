from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym
import panda_gym

# 16 并行环境，更多探索多样性
env = make_vec_env("PandaPickAndPlaceDense-v3", n_envs=16)

model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    tensorboard_log="./ppo_logs/",
    policy_kwargs=dict(net_arch=[512, 512]),
    # 适度探索，不让策略随机化爆炸
    ent_coef=0.005,
    # 学习率线性衰减，但不衰减到 0
    learning_rate=lambda f: 3e-4 * (0.05 + 0.95 * f),
    # clip_range 保持恒定 0.2，确保策略始终能更新
    clip_range=0.2,
    n_steps=4096,
    n_epochs=10,
    batch_size=1024,
    gamma=0.99,
    gae_lambda=0.95,
    # 限制 KL 散度，防止单次更新过大
    target_kl=0.02,
    max_grad_norm=0.5,
)

model.learn(
    total_timesteps=20_000_000,
    progress_bar=True,
    tb_log_name="pickandplace_exp4"
)

model.save("model/best_ppo_panda_pickandplace_v4")
env.close()
