from stable_baselines3 import PPO
import gymnasium as gym
import panda_gym

env = gym.make("PandaPickAndPlaceDense-v3")

obs, info = env.reset()

model = PPO("MultiInputPolicy",
            env,
            verbose=1,
            tensorboard_log="./ppo_logs/",
            # 更大的网络：256x256，默认64x64容量太小学不会抓取
            policy_kwargs=dict(net_arch=[256, 256]),
            # 鼓励探索，避免过早收敛到次优策略
            ent_coef=0.01,
            # 更低的学习率，让训练更稳定
            learning_rate=1e-4,
            # 每次收集更多经验再更新，对复杂任务更有效
            n_steps=4096,
            # 更大的batch使梯度更稳定
            batch_size=256)

model.learn(
    total_timesteps=3000000,
    progress_bar=True,
    tb_log_name="pickandplace_exp2"
)
model.save("model/best_ppo_panda_pickandplace_v3")
env.close()
