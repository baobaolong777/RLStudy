import gymnasium as gym
import panda_gym
from stable_baselines3 import SAC

env = gym.make("PandaPickAndPlaceDense-v3", render_mode="human")
model = SAC.load("model/best_sac_her_panda_pickandplace_v1", env=env)

for episode in range(10):
    obs, info = env.reset()
    done = False
    total_reward = 0
    steps = 0
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps += 1
        done = terminated or truncated
    print(f"episode: {episode}, reward: {total_reward:.3f}, success: {info['is_success']}, steps: {steps}")

env.close()
