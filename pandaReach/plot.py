import gymnasium as gym
import panda_gym
import matplotlib.pyplot as plt
from stable_baselines3 import PPO


env = gym.make(
    "PandaReachDense-v3"
)

model = PPO.load(
    "model/best_ppo_panda_reach"
)

episode_rewards = []
episode_steps = []
successes = []

TEST_EPISODES = 100

for episode in range(TEST_EPISODES):

    obs, info = env.reset()

    done = False

    total_reward = 0

    step_count = 0

    success = False

    while not done:

        action,_ = model.predict(
            obs,
            deterministic=True
        )

        obs,reward,terminated,truncated,info = env.step(
            action
        )

        total_reward += reward

        step_count += 1

        done = terminated or truncated

        if info["is_success"]:

            success = True

    episode_rewards.append(
        total_reward
    )

    episode_steps.append(
        step_count
    )

    successes.append(
        int(success)
    )

env.close()


plt.figure(figsize=(8,5))

plt.plot(
    episode_rewards
)

plt.xlabel(
    "Episode"
)

plt.ylabel(
    "Reward"
)

plt.title(
    "Evaluation Reward"
)

plt.grid()

plt.show()


plt.figure(figsize=(8,5))

plt.plot(
    episode_steps
)

plt.xlabel(
    "Episode"
)

plt.ylabel(
    "Steps"
)

plt.title(
    "Evaluation Episode Length"
)

plt.grid()

plt.show()


plt.figure(figsize=(8,5))

success_rate = []

for i in range(TEST_EPISODES):

    success_rate.append(
        sum(successes[:i+1])/(i+1)
    )

plt.plot(
    success_rate
)

plt.xlabel(
    "Episode"
)

plt.ylabel(
    "Success Rate"
)

plt.title(
    "Evaluation Success Rate"
)

plt.grid()

plt.show()


print(
    f"Average Reward:{sum(episode_rewards)/TEST_EPISODES:.3f}"
)

print(
    f"Average Steps:{sum(episode_steps)/TEST_EPISODES:.2f}"
)

print(
    f"Success Rate:{sum(successes)/TEST_EPISODES:.3f}"
)