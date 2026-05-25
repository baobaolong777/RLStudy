import gymnasium as gym
import panda_gym
import matplotlib.pyplot as plt
from stable_baselines3 import SAC

env = gym.make("PandaPickAndPlaceDense-v3")
model = SAC.load("model/best_sac_her_panda_pickandplace_v1", env=env)

episode_rewards = []
episode_steps = []
successes = []

TEST_EPISODES = 100

for episode in range(TEST_EPISODES):
    obs, info = env.reset()
    done = False
    total_reward = 0
    step_count = 0

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        step_count += 1
        done = terminated or truncated

    episode_rewards.append(total_reward)
    episode_steps.append(step_count)
    successes.append(int(info["is_success"]))

env.close()

avg_reward = sum(episode_rewards) / TEST_EPISODES
avg_steps = sum(episode_steps) / TEST_EPISODES
success_rate = sum(successes) / TEST_EPISODES

# 1. Reward 曲线
plt.figure(figsize=(9, 5))
plt.plot(episode_rewards)
plt.axhline(avg_reward, color="r", linestyle="--", label=f"Avg: {avg_reward:.3f}")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("SAC+HER Evaluation Reward")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("sac_her_reward.png", dpi=150)
plt.show()

# 2. Steps 曲线
plt.figure(figsize=(9, 5))
plt.plot(episode_steps)
plt.axhline(avg_steps, color="r", linestyle="--", label=f"Avg: {avg_steps:.1f}")
plt.xlabel("Episode")
plt.ylabel("Steps")
plt.title("SAC+HER Evaluation Episode Length")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("sac_her_steps.png", dpi=150)
plt.show()

# 3. Success Rate 累积曲线
plt.figure(figsize=(9, 5))
cumulative_rate = []
for i in range(TEST_EPISODES):
    cumulative_rate.append(sum(successes[:i + 1]) / (i + 1))
plt.plot(cumulative_rate)
plt.axhline(success_rate, color="r", linestyle="--", label=f"Final: {success_rate:.3f}")
plt.xlabel("Episode")
plt.ylabel("Success Rate")
plt.title("SAC+HER Evaluation Success Rate")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("sac_her_success_rate.png", dpi=150)
plt.show()

print(f"Average Reward: {avg_reward:.3f}")
print(f"Average Steps: {avg_steps:.1f}")
print(f"Success Rate: {success_rate:.3f} ({sum(successes)}/{TEST_EPISODES})")
