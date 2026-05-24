import gymnasium as gym
import panda_gym
from stable_baselines3 import SAC

env = gym.make("PandaPickAndPlaceDense-v3")

obs, info = env.reset()

model = SAC("MultiInputPolicy",
            env,
            verbose=1,
            tensorboard_log="./sac_logs/",
            buffer_size=500_000,
            batch_size=256,
            learning_rate=3e-4,
            tau=0.005,
            gamma=0.99)

model.learn(
    total_timesteps=200000,
    progress_bar=True,
    tb_log_name="pickandplace_sac_exp1"
)
model.save("model/best_sac_panda_pickandplace_v1")
env.close()
