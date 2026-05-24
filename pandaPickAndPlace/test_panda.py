import gymnasium as gym
import panda_gym
from stable_baselines3 import PPO

env = gym.make("PandaPickAndPlaceDense-v3")

model = PPO.load("model/best_ppo_panda_pickandplace_v2")

obs, info = env.reset()

episode = 0

while episode < 30:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        print(f"episode: {episode}, reward: {reward:.3f}, success: {info['is_success']}")
        obs, info = env.reset()
        episode += 1

env.close()
