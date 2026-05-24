from stable_baselines3 import PPO
import gymnasium as gym
import panda_gym

env = gym.make(
    "PandaPushDense-v3"
)

obs,info = env.reset()

model = PPO("MultiInputPolicy",
            env,
            verbose = 1,
            tensorboard_log = "./pandaPush/ppo_logs/")

model.learn(
    total_timesteps=2000000,
    progress_bar=True,
    tb_log_name="push_exp2"
)
model.save("model/best_ppo_panda_push_v2")
env.close()


