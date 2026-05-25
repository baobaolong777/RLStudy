from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

IMG_BASE = os.path.abspath("png")
DEMO_BASE = os.path.abspath("demo")

def add_bg(slide, color=RGBColor(0x1a, 0x1a, 0x2e)):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, color, alpha=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)  # 1 = rectangle
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text(slide, text, left, top, width, height, size=18, color=RGBColor(0xFF, 0xFF, 0xFF), bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return txBox

def add_image(slide, path, left, top, width=None, height=None):
    if width and height:
        return slide.shapes.add_picture(path, left, top, width, height)
    elif width:
        return slide.shapes.add_picture(path, left, top, width=width)
    elif height:
        return slide.shapes.add_picture(path, left, top, height=height)
    else:
        return slide.shapes.add_picture(path, left, top)

# ========== Slide 1: 封面 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_bg(slide)

add_rect(slide, 0, Inches(2.5), prs.slide_width, Inches(0.06), RGBColor(0x00, 0xD2, 0xFF))
add_text(slide, "基于 PPO 与 SAC+HER 的机械臂\n强化学习对比实验", Inches(1), Inches(1.2), Inches(11), Inches(1.5),
         size=40, color=RGBColor(0xFF, 0xFF, 0xFF), bold=True, align=PP_ALIGN.CENTER)
add_text(slide, "Panda PickAndPlace 任务 · Franka Panda 机械臂仿真", Inches(1), Inches(2.8), Inches(11), Inches(0.8),
         size=20, color=RGBColor(0xAA, 0xAA, 0xCC), align=PP_ALIGN.CENTER)
add_text(slide, "2026", Inches(1), Inches(4.2), Inches(11), Inches(0.6),
         size=18, color=RGBColor(0x88, 0x88, 0xAA), align=PP_ALIGN.CENTER)

# ========== Slide 2: 实验背景 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00, 0xD2, 0xFF))
add_text(slide, "实验背景", Inches(0.6), Inches(0.3), Inches(5), Inches(0.8),
         size=32, color=RGBColor(0x00, 0xD2, 0xFF), bold=True)

items = [
    ("任务环境", "Franka Panda 机械臂仿真 (panda_gym)"),
    ("实验平台", "Stable-Baselines3 · PyBullet 物理引擎"),
    ("递进任务", "Reach（到达）→ Push（推动）→ PickAndPlace（抓取放置）"),
    ("核心任务", "PandaPickAndPlaceDense-v3\n多阶段：接近→抓取→抬起→移动→放置\n一类失败则整体失败，是典型的复杂多阶段任务"),
]
y = 1.3
for title, desc in items:
    add_rect(slide, Inches(0.6), Inches(y), Inches(0.12), Inches(0.12), RGBColor(0x00, 0xD2, 0xFF))
    add_text(slide, title, Inches(1.0), Inches(y - 0.05), Inches(3), Inches(0.4),
             size=18, color=RGBColor(0x00, 0xD2, 0xFF), bold=True)
    add_text(slide, desc, Inches(1.0), Inches(y + 0.35), Inches(11), Inches(0.8),
             size=16, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 1.5

# ========== Slide 3: PPO ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xE8, 0x6C, 0x00))
add_text(slide, "算法介绍：PPO", Inches(0.6), Inches(0.3), Inches(5), Inches(0.8),
         size=32, color=RGBColor(0xE8, 0x6C, 0x00), bold=True)

# Add Reach images
reach_images = sorted([f for f in os.listdir(os.path.join(IMG_BASE, "Reach")) if f.endswith(".png")])
x_pos = [0.5, 6.8]
for i, img_name in enumerate(reach_images[:2]):
    path = os.path.join(IMG_BASE, "Reach", img_name)
    add_image(slide, path, Inches(x_pos[i]), Inches(1.3), width=Inches(6))

add_text(slide, "PandaReach 训练曲线（PPO, 4万步达100%成功率）", Inches(0.5), Inches(4.8), Inches(6), Inches(0.4),
         size=14, color=RGBColor(0x88, 0x88, 0xAA), align=PP_ALIGN.CENTER)
add_text(slide, "PandaReach 成功率先升至100%", Inches(6.8), Inches(4.8), Inches(6), Inches(0.4),
         size=14, color=RGBColor(0x88, 0x88, 0xAA), align=PP_ALIGN.CENTER)

items_ppo = [
    "On-policy 算法：采集一批数据 → 更新策略 → 丢弃",
    "适合单阶段任务（如 Reach），100% 成功",
    "样本效率低，每步数据只用一次",
]
y = 5.4
for item in items_ppo:
    add_text(slide, f"• {item}", Inches(0.6), Inches(y), Inches(11), Inches(0.4),
             size=16, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 0.5

# ========== Slide 4: SAC+HER ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00, 0xCC, 0x66))
add_text(slide, "算法介绍：SAC + HER", Inches(0.6), Inches(0.3), Inches(6), Inches(0.8),
         size=32, color=RGBColor(0x00, 0xCC, 0x66), bold=True)

add_text(slide, "SAC (Soft Actor-Critic)", Inches(0.6), Inches(1.3), Inches(5), Inches(0.4),
         size=22, color=RGBColor(0x00, 0xD2, 0xFF), bold=True)
sac_items = [
    "Off-policy 算法，有 replay buffer",
    "最大熵框架：在奖励和探索之间平衡",
    "历史数据可反复使用，样本效率高",
]
y = 1.8
for item in sac_items:
    add_text(slide, f"• {item}", Inches(0.8), Inches(y), Inches(5), Inches(0.4),
             size=16, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 0.5

add_text(slide, "HER (Hindsight Experience Replay)", Inches(6.5), Inches(1.3), Inches(6), Inches(0.4),
         size=22, color=RGBColor(0x00, 0xD2, 0xFF), bold=True)
her_items = [
    "把失败轨迹\"重新标目标\"变成有用经验",
    "例如：没抓到物体 → 目标改为手的位置",
    "失败=下一次学习的正样本",
]
y = 1.8
for item in her_items:
    add_text(slide, f"• {item}", Inches(6.7), Inches(y), Inches(6), Inches(0.4),
             size=16, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 0.5

add_rect(slide, Inches(0.6), Inches(3.8), Inches(12), Inches(0.04), RGBColor(0xFF, 0xFF, 0xFF))
add_text(slide, "SAC 提供 replay buffer + 高样本效率，HER 将失败转化为有用经验 → 天然互补", Inches(0.6), Inches(4.0), Inches(12), Inches(0.5),
         size=18, color=RGBColor(0x00, 0xCC, 0x66), bold=True, align=PP_ALIGN.CENTER)

# ========== Slide 5: 对比结果 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xFF, 0xD7, 0x00))
add_text(slide, "实验结果对比：PickAndPlace", Inches(0.6), Inches(0.3), Inches(8), Inches(0.8),
         size=32, color=RGBColor(0xFF, 0xD7, 0x00), bold=True)

# 表格
from pptx.util import Inches, Pt
rows, cols = 5, 3
tbl = slide.shapes.add_table(rows, cols, Inches(0.8), Inches(1.3), Inches(11.5), Inches(3.5)).table
tbl.columns[0].width = Inches(4)
tbl.columns[1].width = Inches(3.75)
tbl.columns[2].width = Inches(3.75)

headers = ["指标", "PPO", "SAC + HER"]
data = [
    ["训练步数", "760 万", "100 万"],
    ["测试成功率", "4%", "99%"],
    ["平均完成步数", "50（超时）", "8.5 步"],
    ["完成1轮所需步数（最快）", "50 步全部失败", "5 步成功"],
]

for c, h in enumerate(headers):
    cell = tbl.cell(0, c)
    cell.text = h
    for p in cell.text_frame.paragraphs:
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = PP_ALIGN.CENTER

for r, row_data in enumerate(data):
    for c, val in enumerate(row_data):
        cell = tbl.cell(r + 1, c)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(16)
            p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            p.alignment = PP_ALIGN.CENTER

# 下方放图
sac_her_dir = os.path.join(IMG_BASE, "sac_her_PickAndPlace")
sac_images = sorted([f for f in os.listdir(sac_her_dir) if f.endswith(".png")])
for i, img_name in enumerate(sac_images[:4]):
    path = os.path.join(sac_her_dir, img_name)
    add_image(slide, path, Inches(0.5 + i * 3.2), Inches(5.0), width=Inches(3))

# ========== Slide 6: 视频对比 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xFF, 0x69, 0xB4))
add_text(slide, "演示视频对比", Inches(0.6), Inches(0.3), Inches(6), Inches(0.8),
         size=32, color=RGBColor(0xFF, 0x69, 0xB4), bold=True)

cols_vid = ["任务", "PPO", "SAC+HER", "Reach (PPO)"]
rows_vid = ["效果"]
tbl2 = slide.shapes.add_table(2, 4, Inches(0.8), Inches(1.5), Inches(11.5), Inches(2.0)).table
for c, h in enumerate(cols_vid):
    cell = tbl2.cell(0, c)
    cell.text = h
    for p in cell.text_frame.paragraphs:
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = PP_ALIGN.CENTER

cell = tbl2.cell(1, 0)
cell.text = "PickAndPlace"
for p in cell.text_frame.paragraphs:
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.CENTER
cell = tbl2.cell(1, 1)
cell.text = "❌ 全部失败\n50步超时"
for p in cell.text_frame.paragraphs:
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.CENTER
cell = tbl2.cell(1, 2)
cell.text = "✅ 100%成功\n平均8.5步"
for p in cell.text_frame.paragraphs:
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.CENTER
cell = tbl2.cell(1, 3)
cell.text = "✅ 100%成功\n最快1步"
for p in cell.text_frame.paragraphs:
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    p.alignment = PP_ALIGN.CENTER

add_text(slide, "视频文件路径（PPT 中可插入视频）：", Inches(0.8), Inches(3.8), Inches(11), Inches(0.4),
         size=16, color=RGBColor(0xAA, 0xAA, 0xCC))

video_info = [
    "Reach 成功演示：demo/reach_demo/",
    "PPO PickAndPlace 失败演示：demo/ppo_pickandplace_demo/",
    "SAC+HER PickAndPlace 成功演示：demo/sac_her_demo/",
]
y = 4.4
for info in video_info:
    add_text(slide, f"• {info}", Inches(1.0), Inches(y), Inches(11), Inches(0.4),
             size=15, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 0.5

add_text(slide, "操作：插入 → 视频 → 此设备 → 选择对应 mp4 文件", Inches(0.8), Inches(5.8), Inches(11), Inches(0.4),
         size=14, color=RGBColor(0x88, 0x88, 0xAA))

# PPO PickAndPlace images on right
ppo_dir = os.path.join(IMG_BASE, "ppo_PickAndPlace")
ppo_images = sorted([f for f in os.listdir(ppo_dir) if f.endswith(".png")])
for i, img_name in enumerate(ppo_images[:2]):
    path = os.path.join(ppo_dir, img_name)
    if i == 0:
        add_image(slide, path, Inches(6.5), Inches(4.0), width=Inches(3))

# ========== Slide 7: 分析 - 为什么 PPO 不行 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xE8, 0x6C, 0x00))
add_text(slide, "分析：为什么 PPO 不行", Inches(0.6), Inches(0.3), Inches(8), Inches(0.8),
         size=32, color=RGBColor(0xE8, 0x6C, 0x00), bold=True)

analysis_ppo = [
    "On-policy 本质：失败轨迹采集完就丢弃，信息浪费严重",
    "PickAndPlace 是多阶段任务（接近→抓→抬→移→放），每步都可能失败",
    "单次失败概率高 → 完整成功轨迹极少 → 策略几乎学不到正面信息",
    "增加训练步数到 2000 万可能有效，但成本过高",
]
y = 1.5
for item in analysis_ppo:
    add_text(slide, f"▸ {item}", Inches(0.8), Inches(y), Inches(11), Inches(0.5),
             size=18, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 0.8

add_text(slide, "PPO on PickAndPlace：760万步 → 4% 成功率", Inches(0.8), Inches(5.0), Inches(6), Inches(0.5),
         size=24, color=RGBColor(0xE8, 0x6C, 0x00), bold=True)

ppo_dir = os.path.join(IMG_BASE, "ppo_PickAndPlace")
ppo_images = sorted([f for f in os.listdir(ppo_dir) if f.endswith(".png")])
for i, img_name in enumerate(ppo_images[2:4]):
    path = os.path.join(ppo_dir, img_name)
    add_image(slide, path, Inches(7.5), Inches(4.0 + (i - 2) * 1.8), width=Inches(5))

# ========== Slide 8: 为什么 SAC+HER 行 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0x00, 0xCC, 0x66))
add_text(slide, "分析：为什么 SAC+HER 行", Inches(0.6), Inches(0.3), Inches(8), Inches(0.8),
         size=32, color=RGBColor(0x00, 0xCC, 0x66), bold=True)

analysis_sac = [
    "SAC 的 replay buffer 存下所有历史轨迹，反复回放学习",
    "HER 将失败轨迹重新解释为目标接近样本，变废为宝",
    "40 万步即达 87% 成功率，100 万步 99%~100%",
    "样本效率远超 PPO：约 1/10 步数达到远超 PPO 的效果",
]
y = 1.5
for item in analysis_sac:
    add_text(slide, f"▸ {item}", Inches(0.8), Inches(y), Inches(11), Inches(0.5),
             size=18, color=RGBColor(0xCC, 0xCC, 0xDD))
    y += 0.8

add_text(slide, "SAC+HER on PickAndPlace：100万步 → 99% 成功率", Inches(0.8), Inches(5.0), Inches(8), Inches(0.5),
         size=24, color=RGBColor(0x00, 0xCC, 0x66), bold=True)

sac_her_dir = os.path.join(IMG_BASE, "sac_her_PickAndPlace")
sac_images = sorted([f for f in os.listdir(sac_her_dir) if f.endswith(".png")])
for i, img_name in enumerate(sac_images[:4]):
    path = os.path.join(sac_her_dir, img_name)
    add_image(slide, path, Inches(7.5 + (i % 2) * 2.8), Inches(4.0 + (i // 2) * 1.6), width=Inches(2.6))

# ========== Slide 9: 总结 ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_rect(slide, 0, 0, Inches(0.12), prs.slide_height, RGBColor(0xFF, 0xD7, 0x00))
add_text(slide, "总结", Inches(0.6), Inches(0.3), Inches(5), Inches(0.8),
         size=32, color=RGBColor(0xFF, 0xD7, 0x00), bold=True)

summary_items = [
    ("PPO", "适合简单单阶段任务（如 Reach），稳定可控\n在多阶段复杂任务上样本效率严重不足", RGBColor(0xE8, 0x6C, 0x00)),
    ("SAC + HER", "off-policy + HER 天然适合多阶段任务\n样本效率高，是近三年 RL 领域重要成果", RGBColor(0x00, 0xCC, 0x66)),
    ("实验结论", "算法选择应匹配任务特性\nHER 有效解决了稀疏奖励和多阶段问题", RGBColor(0x00, 0xD2, 0xFF)),
]

for i, (title, desc, color) in enumerate(summary_items):
    y = 1.3 + i * 1.8
    add_rect(slide, Inches(0.6), Inches(y), Inches(0.12), Inches(0.6), color)
    add_text(slide, title, Inches(1.0), Inches(y), Inches(4), Inches(0.5),
             size=22, color=color, bold=True)
    add_text(slide, desc, Inches(1.0), Inches(y + 0.55), Inches(11), Inches(0.8),
             size=16, color=RGBColor(0xCC, 0xCC, 0xDD))

add_rect(slide, Inches(0.6), Inches(6.5), Inches(12), Inches(0.04), RGBColor(0x00, 0xD2, 0xFF))
add_text(slide, "HER 论文：Hindsight Experience Replay (Andrychowicz et al., 2017)", Inches(0.6), Inches(6.7), Inches(11), Inches(0.4),
         size=14, color=RGBColor(0x88, 0x88, 0xAA), align=PP_ALIGN.CENTER)

# Save
output_path = os.path.abspath("汇报PPT_PPO_vs_SAC_HER.pptx")
prs.save(output_path)
print(f"PPT saved to: {output_path}")
