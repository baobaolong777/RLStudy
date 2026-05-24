import gymnasium as gym
import panda_gym
from stable_baselines3 import PPO
import sys

model_path = sys.argv[1] if len(sys.argv) > 1 else "model/best_ppo_panda_pickandplace_v3"

env = gym.make("PandaPickAndPlaceDense-v3")

model = PPO.load(model_path)

TEST_EPISODES = 100
successes = []
rewards = []

for episode in range(TEST_EPISODES):
    obs, info = env.reset()
    done = False
    total_reward = 0
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated
    successes.append(int(info["is_success"]))
    rewards.append(total_reward)

env.close()

success_rate = sum(successes) / TEST_EPISODES
avg_reward = sum(rewards) / TEST_EPISODES

print(f"Success Rate: {success_rate:.3f} ({sum(successes)}/{TEST_EPISODES})")
print(f"Average Reward: {avg_reward:.3f}")
