import gymnasium as gym
import panda_gym
from stable_baselines3 import PPO
env = gym.make(
    "PandaReachDense-v3",
)

obs, info = env.reset()

model = PPO("MultiInputPolicy",env,verbose=1,tensorboard_log="./ppo_logs/")

model.learn(total_timesteps=100000,
    progress_bar=True,
    tb_log_name="reach_exp1")

model.save("model/best_ppo_panda_reach_v2")

env.close()