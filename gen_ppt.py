from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

IMG_BASE = os.path.abspath("png")

def add_bg(slide, color=RGBColor(0x1a, 0x1a, 0x2e)):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def add_rect(slide, l, t, w, h, c):
    s = slide.shapes.add_shape(1, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = c; s.line.fill.background()

def txt(slide, text, l, t, w, h, size=18, color=RGBColor(0xFF,0xFF,0xFF), bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.text_frame.word_wrap = True
    p = box.text_frame.paragraphs[0]
    p.text = text; p.font.size = Pt(size); p.font.color.rgb = color; p.font.bold = bold; p.alignment = align

def pic(slide, path, l, t, w=None, h=None):
    return slide.shapes.add_picture(path, l, t, w, h)

reach_dir = os.path.join(IMG_BASE, "Reach")
ppo_dir = os.path.join(IMG_BASE, "ppo_PickAndPlace")
sac_dir = os.path.join(IMG_BASE, "sac_her_PickAndPlace")
reach_imgs = sorted([f for f in os.listdir(reach_dir) if f.endswith(".png")])
ppo_imgs = sorted([f for f in os.listdir(ppo_dir) if f.endswith(".png")])
sac_imgs = sorted([f for f in os.listdir(sac_dir) if f.endswith(".png")])

# ====== Slide 1: Cover ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, Inches(2.5), prs.slide_width, Inches(0.06), RGBColor(0x00,0xD2,0xFF))
txt(s, "基于 PPO 与 SAC+HER 的机械臂\n强化学习对比实验", Inches(1), Inches(1.2), Inches(11), Inches(1.5), size=40, bold=True, align=PP_ALIGN.CENTER)
txt(s, "Panda PickAndPlace 任务 · Franka Panda 机械臂仿真", Inches(1), Inches(2.8), Inches(11), Inches(0.8), size=20, color=RGBColor(0xAA,0xAA,0xCC), align=PP_ALIGN.CENTER)
txt(s, "2026", Inches(1), Inches(4.2), Inches(11), Inches(0.6), size=18, color=RGBColor(0x88,0x88,0xAA), align=PP_ALIGN.CENTER)

# ====== Slide 2: Background ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00,0xD2,0xFF))
txt(s, "实验背景", Inches(0.6), Inches(0.3), Inches(8), Inches(0.7), size=32, bold=True)
for i, item in enumerate([
    "任务环境：Franka Panda 机械臂仿真 (panda_gym + PyBullet)",
    "技术栈：Stable-Baselines3 · Gymnasium",
    "核心任务：PandaPickAndPlaceDense-v3",
    "任务流程：接近物体 → 抓取 → 抬起 → 移动 → 放置",
    "难点：多阶段复杂度，一步错则整体失败",
]):
    txt(s, f"▸ {item}", Inches(0.8), Inches(1.3 + i*0.65), Inches(11), Inches(0.5), size=17, color=RGBColor(0xCC,0xCC,0xDD))

# ====== Slide 3: PPO algorithm ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xE8,0x6C,0x00))
txt(s, "算法一：PPO (Proximal Policy Optimization)", Inches(0.6), Inches(0.3), Inches(10), Inches(0.7), size=28, bold=True)
for i, item in enumerate([
    "On-policy 算法：当前策略采数据 → 更新策略 → 丢弃数据",
    "有 rollout buffer（临时存储一批经验），但更新即清空",
    "优势：训练稳定，适合单阶段简单任务",
    "劣势：样本效率低，多阶段任务表现不佳",
]):
    txt(s, f"• {item}", Inches(0.8), Inches(1.2 + i*0.55), Inches(11), Inches(0.5), size=16, color=RGBColor(0xCC,0xCC,0xDD))
txt(s, "关键：PPO 没有持久化的 replay buffer，无法做 HER", Inches(0.8), Inches(3.8), Inches(11), Inches(0.5), size=18, color=RGBColor(0xE8,0x6C,0x00), bold=True)

# ====== Slide 4: PPO Reach results (2x2 all images) ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xE8,0x6C,0x00))
txt(s, "PPO — PandaReach 训练曲线", Inches(0.6), Inches(0.15), Inches(10), Inches(0.5), size=26, bold=True)
positions = [(0.5,0.9,6.0,2.9), (6.8,0.9,6.0,2.9), (0.5,4.0,6.0,2.9), (6.8,4.0,6.0,2.9)]
for i, fn in enumerate(reach_imgs):
    pic(s, os.path.join(reach_dir, fn), Inches(positions[i][0]), Inches(positions[i][1]), w=Inches(6))
txt(s, "PandaReachDense-v3 — PPO 4 万步达到 100% 成功率，单阶段任务表现优异", Inches(0.5), Inches(7.0), Inches(12), Inches(0.4), size=15, color=RGBColor(0x88,0x88,0xAA), align=PP_ALIGN.CENTER)

# ====== Slide 5: SAC+HER algorithm ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00,0xCC,0x66))
txt(s, "算法二：SAC + HER", Inches(0.6), Inches(0.3), Inches(8), Inches(0.7), size=28, bold=True)
add_rect(s, Inches(0.6), Inches(1.1), Inches(5.5), Inches(0.04), RGBColor(0x00,0xD2,0xFF))
txt(s, "SAC (Soft Actor-Critic)", Inches(0.6), Inches(1.3), Inches(5), Inches(0.4), size=22, bold=True)
for i, item in enumerate(["Off-policy 算法，有持久化 replay buffer", "最大熵框架：在奖励和探索之间取得平衡", "历史数据可反复使用，样本效率高"]):
    txt(s, f"• {item}", Inches(0.8), Inches(1.9 + i*0.45), Inches(5), Inches(0.4), size=16, color=RGBColor(0xCC,0xCC,0xDD))
add_rect(s, Inches(7.0), Inches(1.1), Inches(5.5), Inches(0.04), RGBColor(0x00,0xD2,0xFF))
txt(s, "HER (Hindsight Experience Replay)", Inches(7.0), Inches(1.3), Inches(6), Inches(0.4), size=22, bold=True)
for i, item in enumerate(["将失败轨迹\"重标目标\"转化为有用经验", "例：没抓到物体 → 目标改为手的位置", "失败 = 下一次学习的正样本"]):
    txt(s, f"• {item}", Inches(7.2), Inches(1.9 + i*0.45), Inches(5.5), Inches(0.4), size=16, color=RGBColor(0xCC,0xCC,0xDD))
add_rect(s, Inches(0.6), Inches(3.6), Inches(12), Inches(0.04), RGBColor(0xFF,0xFF,0xFF))
txt(s, "SAC 提供 replay buffer → HER 重标目标 → 失败轨迹变废为宝，两者天然互补", Inches(0.6), Inches(3.8), Inches(12), Inches(0.5), size=18, color=RGBColor(0x00,0xCC,0x66), bold=True, align=PP_ALIGN.CENTER)

# ====== Slide 6: Comparison table ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xFF,0xD7,0x00))
txt(s, "实验结果对比：PPO vs SAC+HER", Inches(0.6), Inches(0.2), Inches(10), Inches(0.6), size=28, bold=True)
tbl = s.shapes.add_table(5, 3, Inches(1.5), Inches(1.2), Inches(10.3), Inches(3.5)).table
tbl.columns[0].width = Inches(3.3); tbl.columns[1].width = Inches(3.5); tbl.columns[2].width = Inches(3.5)
for c, h in enumerate(["指标", "PPO", "SAC+HER"]):
    cell = tbl.cell(0,c); cell.text = h
    for p in cell.text_frame.paragraphs: p.font.size=Pt(20); p.font.bold=True; p.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); p.alignment=PP_ALIGN.CENTER
for r, row in enumerate([["训练总步数","760 万","100 万"],["100 轮测试成功率","4% (4/100)","99~100%"],["平均完成步数","50（全部超时）","8.5 步"],["最快完成","无一成功","5 步"]]):
    for c, v in enumerate(row):
        cell = tbl.cell(r+1,c); cell.text = v
        for p in cell.text_frame.paragraphs: p.font.size=Pt(18); p.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); p.alignment=PP_ALIGN.CENTER

# ====== Slide 7: SAC+HER evaluation curves ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00,0xCC,0x66))
txt(s, "SAC+HER — 评估曲线 (100 轮测试)", Inches(0.6), Inches(0.15), Inches(10), Inches(0.5), size=26, bold=True)
positions = [(0.5,0.9,6.0,2.9), (6.8,0.9,6.0,2.9), (0.5,4.0,6.0,2.9), (6.8,4.0,6.0,2.9)]
for i, fn in enumerate(sac_imgs[:4]):
    pic(s, os.path.join(sac_dir, fn), Inches(positions[i][0]), Inches(positions[i][1]), w=Inches(6))
txt(s, "100 轮评估：成功率 100%，平均 8.5 步完成，5 步即可成功", Inches(0.5), Inches(7.0), Inches(12), Inches(0.4), size=15, color=RGBColor(0x88,0x88,0xAA), align=PP_ALIGN.CENTER)

# ====== Slide 8: PPO failure analysis (text only) ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xE8,0x6C,0x00))
txt(s, "PPO 为什么在 PickAndPlace 上失败？", Inches(0.6), Inches(0.3), Inches(10), Inches(0.7), size=28, bold=True)
items = [
    ("On-policy 本质", "失败轨迹采集完就丢弃，无法反复利用。与 off-policy 不同，PPO 没有持久化的 replay buffer"),
    ("多阶段任务的困境", "接近→抓→抬→移→放，5 个环节每步都可能失败，整体成功率=各环节成功率乘积"),
    ("稀疏正面信号", "在 760 万步训练中，完整成功的轨迹极少，策略几乎学不到\"怎么做才对\""),
    ("结论", "PPO 理论上可能学会，但需要 5000 万步以上，代价远超实际需求"),
]
for i, (title, desc) in enumerate(items):
    y = 1.2 + i * 1.4
    add_rect(s, Inches(0.6), Inches(y), Inches(0.12), Inches(1.0), RGBColor(0xE8,0x6C,0x00))
    add_rect(s, Inches(1.0), Inches(y), Inches(11.5), Inches(1.0), RGBColor(0x25,0x25,0x40))
    txt(s, title, Inches(1.3), Inches(y+0.05), Inches(10), Inches(0.4), size=20, color=RGBColor(0xE8,0x6C,0x00), bold=True)
    txt(s, desc, Inches(1.3), Inches(y+0.45), Inches(10.5), Inches(0.5), size=15, color=RGBColor(0xCC,0xCC,0xDD))

# ====== Slide 9: PPO PickAndPlace curves (dedicated full page, BIG) ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xE8,0x6C,0x00))
txt(s, "PPO — PandaPickAndPlace 训练曲线", Inches(0.6), Inches(0.15), Inches(10), Inches(0.5), size=26, bold=True)
positions = [(0.5,0.9,6.2,2.8), (6.7,0.9,6.2,2.8), (0.5,4.0,6.2,2.8), (6.7,4.0,6.2,2.8)]
for i, fn in enumerate(ppo_imgs[:4]):
    pic(s, os.path.join(ppo_dir, fn), Inches(positions[i][0]), Inches(positions[i][1]), w=Inches(6.2))
txt(s, "760 万步训练 — 成功率仅 4%，50 步全部超时 — On-policy 不适合多阶段任务", Inches(0.5), Inches(7.0), Inches(12), Inches(0.4), size=15, color=RGBColor(0x88,0x88,0xAA), align=PP_ALIGN.CENTER)

# ====== Slide 10: SAC+HER success analysis (text only) ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00,0xCC,0x66))
txt(s, "SAC+HER 为什么成功？", Inches(0.6), Inches(0.3), Inches(10), Inches(0.7), size=28, bold=True)
items = [
    ("持久化 Replay Buffer", "SAC 的 replay buffer 保存所有历史轨迹（含失败的），可反复回放学习\n新旧数据融合，样本效率远超 on-policy"),
    ("HER 重标目标", "把没抓到的轨迹 → 目标改成手的位置 → 就变成了\"差一点就成功\"的正样本\n失败不再是浪费，而是下一次学习的基础"),
    ("样本效率对比", "40 万步 → 87% 成功率\n100 万步 → 99~100% 成功率\n而 PPO 760 万步仅 4%"),
    ("结论", "Off-policy + HER 天然适合多阶段任务，是近三年 RL 领域的重要成果"),
]
for i, (title, desc) in enumerate(items):
    y = 1.2 + i * 1.4
    add_rect(s, Inches(0.6), Inches(y), Inches(0.12), Inches(1.0), RGBColor(0x00,0xCC,0x66))
    add_rect(s, Inches(1.0), Inches(y), Inches(11.5), Inches(1.0), RGBColor(0x25,0x25,0x40))
    txt(s, title, Inches(1.3), Inches(y+0.05), Inches(10), Inches(0.4), size=20, color=RGBColor(0x00,0xCC,0x66), bold=True)
    txt(s, desc, Inches(1.3), Inches(y+0.45), Inches(10.5), Inches(0.5), size=15, color=RGBColor(0xCC,0xCC,0xDD))

# ====== Slide 11: Video ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xFF,0x69,0xB4))
txt(s, "演示视频对比", Inches(0.6), Inches(0.2), Inches(6), Inches(0.6), size=28, bold=True)
tbl = s.shapes.add_table(2, 4, Inches(0.5), Inches(1.2), Inches(12.3), Inches(2.0)).table
for c, h in enumerate(["","PPO","SAC+HER","Reach (PPO)"]):
    cell = tbl.cell(0,c); cell.text = h
    for p in cell.text_frame.paragraphs: p.font.size=Pt(18); p.font.bold=True; p.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); p.alignment=PP_ALIGN.CENTER
for text, col in [("PickAndPlace",0),("❌ 10轮全失败\n50步超时",1),("✅ 10轮全成功\n平均8步",2),("✅ 10轮全成功\n最快1步",3)]:
    cell = tbl.cell(1,col); cell.text = text
    for p in cell.text_frame.paragraphs: p.font.size=Pt(16); p.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); p.alignment=PP_ALIGN.CENTER
txt(s, "视频文件路径（PPT 中插入 → 视频 → 此设备）：", Inches(0.6), Inches(3.5), Inches(12), Inches(0.4), size=16, color=RGBColor(0xAA,0xAA,0xCC))
txt(s, "• demo/reach_demo/ — Reach PPO 成功（1-2步完成）", Inches(0.8), Inches(4.1), Inches(11), Inches(0.4), size=15, color=RGBColor(0xCC,0xCC,0xDD))
txt(s, "• demo/ppo_pickandplace_demo/ — PPO PickAndPlace 全部失败", Inches(0.8), Inches(4.6), Inches(11), Inches(0.4), size=15, color=RGBColor(0xCC,0xCC,0xDD))
txt(s, "• demo/sac_her_demo/ — SAC+HER PickAndPlace 全部成功", Inches(0.8), Inches(5.1), Inches(11), Inches(0.4), size=15, color=RGBColor(0xCC,0xCC,0xDD))

# ====== Slide 12: Summary ======
s = prs.slides.add_slide(prs.slide_layouts[6]); add_bg(s)
add_rect(s, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xFF,0xD7,0x00))
txt(s, "总结", Inches(0.6), Inches(0.2), Inches(5), Inches(0.6), size=32, bold=True)
for i, (t, d, c, extra) in enumerate([
    ("PPO", "单阶段任务（Reach）表现优异，100% 成功 ✅", RGBColor(0xE8,0x6C,0x00), "多阶段任务（PickAndPlace）样本效率严重不足，仅 4% ❌"),
    ("SAC+HER", "Off-policy + 失败重标目标，天然适合多阶段复杂任务", RGBColor(0x00,0xCC,0x66), "100 万步达 99% 成功率，样本效率远超 PPO"),
    ("实验结论", "算法选择应匹配任务特性", RGBColor(0x00,0xD2,0xFF), "HER 是近三年解决稀疏奖励 / 多阶段问题的重要突破"),
]):
    y = 1.0 + i * 1.8
    add_rect(s, Inches(0.6), Inches(y), Inches(0.12), Inches(1.5), c)
    add_rect(s, Inches(1.0), Inches(y), Inches(11.5), Inches(1.5), RGBColor(0x25,0x25,0x40))
    txt(s, t, Inches(1.3), Inches(y+0.1), Inches(3), Inches(0.5), size=24, color=c, bold=True)
    txt(s, d, Inches(1.3), Inches(y+0.55), Inches(10.5), Inches(0.4), size=15, color=RGBColor(0xCC,0xCC,0xDD))
    txt(s, extra, Inches(1.3), Inches(y+0.95), Inches(10.5), Inches(0.4), size=15, color=RGBColor(0xCC,0xCC,0xDD))
add_rect(s, Inches(0.6), Inches(6.8), Inches(12), Inches(0.04), RGBColor(0x00,0xD2,0xFF))
txt(s, "HER 论文：Hindsight Experience Replay (Andrychowicz et al., 2017)", Inches(0.6), Inches(6.9), Inches(12), Inches(0.4), size=14, color=RGBColor(0x88,0x88,0xAA), align=PP_ALIGN.CENTER)

output_path = os.path.abspath("汇报PPT_PPO_vs_SAC_HER.pptx")
prs.save(output_path)
print(f"PPT saved: {output_path} (12 slides)")
