# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

RL 强化学习项目，使用 Franka Panda 机械臂仿真环境。

## 项目结构

```
RLStudy/
├── pandaReach/        # PandaReachDense-v3：机械臂到达目标点任务
│   ├── train_panda.py   # PPO 训练脚本
│   ├── test_panda.py    # 加载模型运行测试
│   ├── test_env.py      # 随机策略测试环境
│   ├── plot.py          # 加载模型评估 + 画图（reward/steps/success rate）
│   └── model/           # 训练好的模型（.zip）
├── pandaPush/         # PandaPushDense-v3：机械臂推动物体任务
│   ├── train_panda.py   # PPO 训练脚本
│   └── model/           # 训练好的模型（.zip）
└── baodonghao/        # 个人练习目录（当前为空）
```

## 技术栈

- `gymnasium` - 强化学习环境接口
- `panda_gym` - Panda 机械臂仿真环境（v3 版本）
- `stable_baselines3` - PPO 算法实现
- 可视化工具：matplotlib（评估画图）、tensorboard（训练日志）

## 常用命令

```bash
# 训练
python pandaReach/train_panda.py
python pandaPush/train_panda.py

# 查看训练日志
tensorboard --logdir pandaReach/ppo_logs/

# 测试已训练的模型
python pandaReach/test_panda.py

# 评估模型并画图
python pandaReach/plot.py

# 测试环境（随机动作）
python pandaReach/test_env.py
```
