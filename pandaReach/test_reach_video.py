import gymnasium as gym
import panda_gym
from stable_baselines3 import PPO
import cv2
import os

OUTPUT_DIR = "reach_demo"
os.makedirs(OUTPUT_DIR, exist_ok=True)

env = gym.make("PandaReachDense-v3", render_mode="rgb_array")
model = PPO.load("pandaReach/model/best_ppo_panda_reach")

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = 30

for episode in range(10):
    obs, info = env.reset()
    done = False
    total_reward = 0
    frames = []

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated
        frames.append(env.render())

    video_path = os.path.join(OUTPUT_DIR, f"episode_{episode}.mp4")
    h, w = frames[0].shape[:2]
    writer = cv2.VideoWriter(video_path, fourcc, fps, (w, h))
    for f in frames:
        writer.write(cv2.cvtColor(f, cv2.COLOR_RGB2BGR))
    writer.release()

    success = "SUCCESS" if info["is_success"] else "FAIL"
    print(f"episode: {episode}, reward: {total_reward:.3f}, {success}, steps: {len(frames)}, video: {video_path}")

env.close()
print(f"\n所有视频已保存到 {OUTPUT_DIR}/")
