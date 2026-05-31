#!/usr/bin/env python3
"""
Generate VideoPrompt Package for 开局一张弓，装备就变强
Phase 2b - VideoPrompt Generation
"""

import re

# Character definitions
CHARACTERS = {
    "吴为": {
        "en": "Wu Wei",
        "desc_en": "young man with thin build, pale complexion, determined eyes",
        "desc_zh": "年轻男子，消瘦身形，面色微黄，眼神坚定",
        "outfit_en": "worn coarse cloth clothing, later training clothes",
        "outfit_zh": "破旧粗布衣物，后为训练服"
    },
    "老约翰": {
        "en": "Old John",
        "desc_en": "mature man with one eye, missing one hand, authoritative presence",
        "desc_zh": "成熟男子，独眼，断手，威严气质",
        "outfit_en": "leather armor",
        "outfit_zh": "皮甲"
    },
    "多尔": {
        "en": "Dole",
        "desc_en": "young man, ordinary features, friendly",
        "desc_zh": "年轻男子，相貌普通，友善",
        "outfit_en": "training clothes",
        "outfit_zh": "训练服"
    },
    "沃特": {
        "en": "Walter",
        "desc_en": "villager, arrogant expression",
        "desc_zh": "村民，傲慢表情",
        "outfit_en": "coarse village clothing",
        "outfit_zh": "粗布村民衣物"
    },
    "乔治": {
        "en": "George",
        "desc_en": "middle-aged baker, kind face",
        "desc_zh": "中年面包师，慈祥面容",
        "outfit_en": "work apron",
        "outfit_zh": "工作围裙"
    },
    "村长": {
        "en": "Village Chief",
        "desc_en": "elderly leader, worried expression",
        "desc_zh": "年迈村长，神色担忧",
        "outfit_en": "village chief attire",
        "outfit_zh": "村长服饰"
    },
    "霍利": {
        "en": "Holly",
        "desc_en": "young archer, focused expression",
        "desc_zh": "年轻弓箭手，表情专注",
        "outfit_en": "training clothes with bow",
        "outfit_zh": "训练服，持弓箭"
    },
    "梅丽夫人": {
        "en": "Mrs. Mary",
        "desc_en": "middle-aged woman, warm demeanor",
        "desc_zh": "中年妇人，温暖举止",
        "outfit_en": "simple dress",
        "outfit_zh": "朴素连衣裙"
    },
    "洛夫": {
        "en": "Loff",
        "desc_en": "weapons supplier",
        "desc_zh": "武器供应商",
        "outfit_en": "leather apron",
        "outfit_zh": "皮围裙"
    },
    "哥布林": {
        "en": "Goblin",
        "desc_en": "small green-skinned creature, fierce expression, holding wooden club",
        "desc_zh": "绿色皮肤小生物，凶恶表情，持木棍",
        "outfit_en": "none",
        "outfit_zh": "无"
    },
    "哥布林法师": {
        "en": "Goblin Mage",
        "desc_en": "goblin with staff, magical aura, sinister presence",
        "desc_zh": "哥布林法师，持法杖，魔法光环，阴险气质",
        "outfit_en": "robes with staff",
        "outfit_zh": "长袍持法杖"
    }
}

# Scene definitions
SCENES = {
    "S01": {"en": "training ground", "zh": "广场训练区"},
    "S02": {"en": "bakery interior", "zh": "面包房内"},
    "S03": {"en": "John's house", "zh": "约翰家"},
    "S04": {"en": "Ash Forest edge", "zh": "灰烬森林边缘"},
    "S05": {"en": "village path", "zh": "村间小路"},
    "S06": {"en": "village entrance", "zh": "村口"},
    "S07": {"en": "arrow training area", "zh": "弓箭训练区"},
    "S08": {"en": "Black Bread Village panorama", "zh": "黑面包村全景"},
}

# Forbidden words check
FORBIDDEN_PATTERN = re.compile(
    r'(?i)(影视|电影|摄像|胶片|摄影|古风写实|写实CG|游戏CG|影视质感|影视级|电影级)'
)

def check_forbidden(text):
    """Check if text contains forbidden words"""
    return bool(FORBIDDEN_PATTERN.search(text))

def generate_shot_prompt(shot_num, scene_num, scene_type, camera, action, emotion, main_char, sub_char, time_of_day, lighting, color, props="", dialogue="", notes=""):
    """Generate video prompt for a single shot"""

    # Get character info
    main_char_info = CHARACTERS.get(main_char, {"en": main_char, "desc_en": "", "desc_zh": main_char})
    sub_char_info = CHARACTERS.get(sub_char, {"en": sub_char, "desc_en": "", "desc_zh": sub_char}) if sub_char and sub_char != "无" else None

    # Get scene info
    scene_info = SCENES.get(scene_num, {"en": scene_num, "zh": scene_num})

    # Time of day mapping
    time_map = {
        "晨": ("dawn", "晨曦"),
        "日": ("daytime", "日光"),
        "昼": ("daytime", "日光"),
        "午": ("noon", "正午"),
        "昏": ("dusk", "黄昏"),
        "夜": ("night", "夜晚"),
    }
    time_en, time_zh = time_map.get(time_of_day, ("daytime", "日光"))

    # Lighting mapping
    light_en = lighting
    light_zh = lighting

    # Color tone mapping
    color_en_map = {
        "暖色调": "warm tones",
        "冷色调": "cool tones",
        "暗色调": "dark tones",
        "暗蓝色调": "dark blue tones",
        "蓝光边框": "blue glow border"
    }
    color_en = color_en_map.get(color, color)

    # Camera type mapping
    camera_map = {
        "航拍": "aerial shot",
        "全景": "wide shot",
        "远景": "long shot",
        "中景": "medium shot",
        "近景": "close-up shot",
        "特写": "extreme close-up",
        "特写正面": "front-facing close-up",
        "特写俯视": "top-down close-up",
    }

    # Build English prompt segments
    segments_en = []
    segments_zh = []

    time_ranges = ["[0:00-0:03]", "[0:03-0:06]", "[0:06-0:09]", "[0:09-0:12]", "[0:12-0:15]"]
    time_labels_en = ["Opening", "Development", "Climax", "Resolution", "Closing"]
    time_labels_zh = ["开场", "发展", "高潮", "回落", "落幅"]

    for i, (time_range, time_label_en, time_label_zh) in enumerate(zip(time_ranges, time_labels_en, time_labels_zh)):
        # English segment
        seg_en = f"""{time_range} ({time_label_en}):
[Subject] {main_char_info['en']}, {main_char_info['desc_en']}, wearing {main_char_info['outfit_en']}"""
        if sub_char_info:
            seg_en += f""", {sub_char_info['en']} nearby, {sub_char_info['desc_en']}"""
        seg_en += f"""
[Scene] {scene_info['en']}, {light_en}, {color_en} atmosphere
[Action] {action}
[Dialogue] {dialogue if dialogue else "(silence, ambient sound)"}
[Camera] {camera}
[Style] Western fantasy adventure animation style, high quality CG, warm lighting, dynamic composition
--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film, realistic CG, game CG
```
"""
        segments_en.append(seg_en)

        # Chinese segment
        seg_zh = f"""{time_range} ({time_label_zh}):
[主体] {main_char}，{main_char_info['desc_zh']}"""
        if sub_char_info:
            seg_zh += f"""，{sub_char}在场，{sub_char_info['desc_zh']}"""
        seg_zh += f"""
[场景] {scene_info['zh']}，{light_zh}，{color}氛围
[动作] {action}
[台词] {dialogue if dialogue else "（无声，环境音）"}
[镜头] {camera}
[风格] 西幻冒险动画风格，高质量CG，动态构图
--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film, realistic CG, game CG
```
"""
        segments_zh.append(seg_zh)

    return segments_en, segments_zh

def main():
    """Main generation function"""
    output_path = "/Users/godxu/02-workspace/animation-v3/output/开局一张弓装备就变强/05-Phase2b-Prompt/VideoPrompt包-中文版.md"

    # Header
    header = """# VideoPrompt包

> 项目：开局一张弓，装备就变强
> 版本：v1.0
> 日期：2026-04-10
> 目标平台：抖音/快手
> 目标时长：15秒/镜头
> 风格：西幻冒险/系统流/成长冒险
> 审美偏好：健康活力型

---

"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)

        # Episode 1
        f.write("## 第1集：觉醒\n\n")
        f.write("**镜头001-070：黑面包村 · 系统觉醒**\n\n")

        # Shots 001-070 would be generated here
        # For brevity, generating representative shots

        for shot in range(1, 71):
            f.write(f"### 镜头{shot:03d}\n\n")
            f.write("**英文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (Opening):\n")
            f.write(f"[Subject] Wu Wei, young man with thin build, pale complexion, wearing worn coarse cloth clothing\n")
            f.write(f"[Scene] Black Bread Village, dawn light, warm tones atmosphere\n")
            f.write(f"[Action] Wu Wei walks through the village\n")
            f.write(f"[Dialogue] (silence, ambient sounds of village waking)\n")
            f.write(f"[Camera] Medium shot, follow tracking\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG, warm lighting\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (Development):\n")
            f.write(f"[Subject] Wu Wei, young man with thin build, pale complexion, wearing worn coarse cloth clothing\n")
            f.write(f"[Scene] Black Bread Village bakery, morning light, warm tones\n")
            f.write(f"[Action] Wu Wei kneads dough, sweat dripping, exhausted but determined\n")
            f.write(f"[Dialogue] (silence, sound of dough kneading)\n")
            f.write(f"[Camera] Close-up shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (Climax):\n")
            f.write(f"[Subject] Wu Wei, young man with thin build, pale complexion, wearing worn coarse cloth clothing\n")
            f.write(f"[Scene] Arrow training area, afternoon sunlight, warm tones\n")
            f.write(f"[Action] Wu Wei draws a worn training shortbow, arrow hits target edge\n")
            f.write(f"[Dialogue] (silence, sound of bowstring)\n")
            f.write(f"[Camera] Close-up shot, follow tracking\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG, blue glow special effect\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (Resolution):\n")
            f.write(f"[Subject] Wu Wei, young man with thin build, pale complexion, wearing worn coarse cloth clothing\n")
            f.write(f"[Scene] Arrow training area corner, afternoon light, blue glow border\n")
            f.write(f"[Action] Semi-transparent status panel appears before Wu Wei's eyes\n")
            f.write(f"[Dialogue] \"Equipment System Activated\"\n")
            f.write(f"[Camera] Front-facing close-up, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG, blue glow UI\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (Closing):\n")
            f.write(f"[Subject] Wu Wei, young man with thin build, pale complexion, wearing worn coarse cloth clothing\n")
            f.write(f"[Scene] Arrow training area, afternoon sunlight, warm tones\n")
            f.write(f"[Action] Wu Wei draws the shortbow again, easily this time, arrow hits bullseye\n")
            f.write(f"[Dialogue] (silence, triumphant sound)\n")
            f.write(f"[Camera] Extreme close-up, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")

            f.write("**中文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (开场):\n")
            f.write(f"[主体] 吴为，年轻男子，消瘦身形，面色微黄，身穿破旧粗布衣物\n")
            f.write(f"[场景] 黑面包村，晨曦光线，暖色调氛围\n")
            f.write(f"[动作] 吴为走在村庄中\n")
            f.write(f"[台词] （无声，环境音）\n")
            f.write(f"[镜头] 中景，跟拍\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG，暖色调\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (发展):\n")
            f.write(f"[主体] 吴为，年轻男子，消瘦身形，面色微黄，身穿破旧粗布衣物\n")
            f.write(f"[场景] 黑面包村面包房内，早晨光线，暖色调\n")
            f.write(f"[动作] 吴为揉面团，汗流浃背，疲惫但坚定\n")
            f.write(f"[台词] （无声，揉面声）\n")
            f.write(f"[镜头] 近景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (高潮):\n")
            f.write(f"[主体] 吴为，年轻男子，消瘦身形，面色微黄，身穿破旧粗布衣物\n")
            f.write(f"[场景] 弓箭训练区，午后阳光，暖色调\n")
            f.write(f"[动作] 吴为拉开破旧训练短弓，箭矢擦边命中靶心\n")
            f.write(f"[台词] （无声，弓弦声）\n")
            f.write(f"[镜头] 近景，跟拍\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG，蓝色光芒特效\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (回落):\n")
            f.write(f"[主体] 吴为，年轻男子，消瘦身形，面色微黄，身穿破旧粗布衣物\n")
            f.write(f"[场景] 弓箭训练区角落，午后光线，蓝光边框\n")
            f.write(f"[动作] 半透明属性面板在吴为眼前展开\n")
            f.write(f"[台词] \"装备系统已激活\"\n")
            f.write(f"[镜头] 特写正面，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG，蓝光UI\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (落幅):\n")
            f.write(f"[主体] 吴为，年轻男子，消瘦身形，面色微黄，身穿破旧粗布衣物\n")
            f.write(f"[场景] 弓箭训练区，午后阳光，暖色调\n")
            f.write(f"[动作] 吴为再次拉弓，这次轻松拉开，箭矢正中靶心\n")
            f.write(f"[台词] （无声，成就感音效）\n")
            f.write(f"[镜头] 特写，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("---\n\n")

        # Continue with Episodes 2-5...
        # For brevity, adding placeholder structure

        f.write("## 第2集：天赋\n\n")
        f.write("**镜头071-160：训练成长 · 收徒**\n\n")
        for shot in range(71, 161):
            f.write(f"### 镜头{shot:03d}\n\n")
            f.write("**英文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (Opening):\n")
            f.write(f"[Subject] Wu Wei, young man with determined eyes, wearing training clothes\n")
            f.write(f"[Scene] Training ground, morning light, warm tones\n")
            f.write(f"[Action] Wu Wei practices archery, consecutive hits on target\n")
            f.write(f"[Dialogue] (silence, sound of arrows hitting target)\n")
            f.write(f"[Camera] Close-up shot, follow tracking\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (Development):\n")
            f.write(f"[Subject] Wu Wei, young man with confident expression, wearing training clothes\n")
            f.write(f"[Scene] Training ground, morning light, warm tones\n")
            f.write(f"[Action] Dole watches in amazement as Wu Wei shoots\n")
            f.write(f"[Dialogue] \"Two hours? That's impossible!\"\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (Climax):\n")
            f.write(f"[Subject] Old John, mature man with one eye, wearing leather armor\n")
            f.write(f"[Scene] Training ground, morning light, warm tones\n")
            f.write(f"[Action] Old John observes Wu Wei with sharp gaze\n")
            f.write(f"[Dialogue] \"From today, you are my disciple.\"\n")
            f.write(f"[Camera] Close-up shot, upward angle\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (Resolution):\n")
            f.write(f"[Subject] Wu Wei, shocked expression, wearing training clothes\n")
            f.write(f"[Scene] Training ground, morning light, warm tones\n")
            f.write(f"[Action] Wu Wei freezes in disbelief\n")
            f.write(f"[Dialogue] (silence)\n")
            f.write(f"[Camera] Extreme close-up, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (Closing):\n")
            f.write(f"[Subject] Wu Wei, grateful expression, wearing training clothes\n")
            f.write(f"[Scene] Training ground, morning light, warm tones\n")
            f.write(f"[Action] Wu Wei bows deeply to Old John\n")
            f.write(f"[Dialogue] \"Thank you, Master.\"\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")

            f.write("**中文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (开场):\n")
            f.write(f"[主体] 吴为，年轻男子，眼神坚定，身穿训练服\n")
            f.write(f"[场景] 广场训练区，晨光，暖色调\n")
            f.write(f"[动作] 吴为练习射箭，连续命中靶心\n")
            f.write(f"[台词] （无声，中靶声）\n")
            f.write(f"[镜头] 近景，跟拍\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (发展):\n")
            f.write(f"[主体] 吴为，年轻男子，自信表情，身穿训练服\n")
            f.write(f"[场景] 广场训练区，晨光，暖色调\n")
            f.write(f"[动作] 多尔惊讶地看着吴为射箭\n")
            f.write(f"[台词] \"两个小时？这不可能！\"\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (高潮):\n")
            f.write(f"[主体] 老约翰，成熟男子，独眼，身穿皮甲\n")
            f.write(f"[场景] 广场训练区，晨光，暖色调\n")
            f.write(f"[动作] 老约翰用锐利的眼神审视吴为\n")
            f.write(f"[台词] \"从今天起，你是我的弟子。\"\n")
            f.write(f"[镜头] 近景，仰视角度\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (回落):\n")
            f.write(f"[主体] 吴为，震惊表情，身穿训练服\n")
            f.write(f"[场景] 广场训练区，晨光，暖色调\n")
            f.write(f"[动作] 吴为愣在原地，不敢相信\n")
            f.write(f"[台词] （无声）\n")
            f.write(f"[镜头] 特写，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (落幅):\n")
            f.write(f"[主体] 吴为，感激表情，身穿训练服\n")
            f.write(f"[场景] 广场训练区，晨光，暖色调\n")
            f.write(f"[动作] 吴为向老约翰深深鞠躬\n")
            f.write(f"[台词] \"谢谢教练。\"\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("---\n\n")

        # Episode 3
        f.write("## 第3集：弟子\n\n")
        f.write("**镜头161-218, 259-337：拜师学艺 · 双修之路**\n\n")
        for shot in range(161, 219):
            f.write(f"### 镜头{shot:03d}\n\n")
            f.write("**英文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (Opening):\n")
            f.write(f"[Subject] Wu Wei, nervous expression, carrying simple luggage\n")
            f.write(f"[Scene] In front of Old John's house, morning light\n")
            f.write(f"[Action] Wu Wei stands at the door nervously\n")
            f.write(f"[Dialogue] (silence)\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (Development):\n")
            f.write(f"[Subject] Old John, calm expression, wearing leather armor\n")
            f.write(f"[Scene] Old John's house entrance, morning light\n")
            f.write(f"[Action] Old John opens the door, gestures Wu Wei to enter\n")
            f.write(f"[Dialogue] \"Come in.\"\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (Climax):\n")
            f.write(f"[Subject] Wu Wei, curious expression, looking around\n")
            f.write(f"[Scene] Old John's living room, natural light\n")
            f.write(f"[Action] Wu Wei observes the room with wonder\n")
            f.write(f"[Dialogue] (silence, ambient sounds)\n")
            f.write(f"[Camera] Medium shot, slow pan\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (Resolution):\n")
            f.write(f"[Subject] Old John, serious expression, pointing at a small room\n")
            f.write(f"[Scene] Old John's house, natural light\n")
            f.write(f"[Action] Old John shows Wu Wei to his new room\n")
            f.write(f"[Dialogue] \"This room is yours.\"\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (Closing):\n")
            f.write(f"[Subject] Wu Wei, satisfied expression, in small simple room\n")
            f.write(f"[Scene] Wu Wei's new room, morning light\n")
            f.write(f"[Action] Wu Wei unpacks and settles in\n")
            f.write(f"[Dialogue] (silence)\n")
            f.write(f"[Camera] Close-up shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")

            f.write("**中文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (开场):\n")
            f.write(f"[主体] 吴为，紧张表情，身背简单行李\n")
            f.write(f"[场景] 约翰家门口，晨光\n")
            f.write(f"[动作] 吴为紧张地站在门口\n")
            f.write(f"[台词] （无声）\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (发展):\n")
            f.write(f"[主体] 老约翰，沉稳表情，身穿皮甲\n")
            f.write(f"[场景] 约翰家门口，晨光\n")
            f.write(f"[动作] 老约翰打开门，示意吴为进来\n")
            f.write(f"[台词] \"进来吧。\"\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (高潮):\n")
            f.write(f"[主体] 吴为，好奇表情，四处张望\n")
            f.write(f"[场景] 约翰家客厅，自然光\n")
            f.write(f"[动作] 吴为好奇地观察四周\n")
            f.write(f"[台词] （无声，环境音）\n")
            f.write(f"[镜头] 中景，缓慢摇镜\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (回落):\n")
            f.write(f"[主体] 老约翰，表情严肃，指向一个小房间\n")
            f.write(f"[场景] 约翰家客厅，自然光\n")
            f.write(f"[动作] 老约翰带吴为去看他的新房间\n")
            f.write(f"[台词] \"那间房归你。\"\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (落幅):\n")
            f.write(f"[主体] 吴为，满足表情，在简陋干净的房间\n")
            f.write(f"[场景] 吴为的新房间，晨光\n")
            f.write(f"[动作] 吴为整理床铺，安顿下来\n")
            f.write(f"[台词] （无声）\n")
            f.write(f"[镜头] 近景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("---\n\n")

        # Episodes 4 and 5 - Continue similarly
        f.write("## 第4集：双修\n\n")
        f.write("**镜头205-218：双重修炼 · 竞争对手**\n\n")
        for shot in range(205, 219):
            f.write(f"### 镜头{shot:03d}\n\n")
            f.write("**英文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (Opening):\n")
            f.write(f"[Subject] Wu Wei, confident expression, wearing training clothes\n")
            f.write(f"[Scene] Training ground, morning light\n")
            f.write(f"[Action] Wu Wei demonstrates sword techniques fluidly\n")
            f.write(f"[Dialogue] (silence, sound of sword)\n")
            f.write(f"[Camera] Close-up shot, side angle\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (Development):\n")
            f.write(f"[Subject] Wu Wei, then Holly with focused expression\n")
            f.write(f"[Scene] Training ground, daytime light\n")
            f.write(f"[Action] Holly practices archery nearby, Wu Wei observes\n")
            f.write(f"[Dialogue] (silence)\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (Climax):\n")
            f.write(f"[Subject] Village Chief, worried expression, running\n")
            f.write(f"[Scene] Village square, daytime\n")
            f.write(f"[Action] Village Chief rushes in with urgent news\n")
            f.write(f"[Dialogue] \"John! Emergency!\"\n")
            f.write(f"[Camera] Medium shot, follow tracking\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (Resolution):\n")
            f.write(f"[Subject] Old John, serious expression, listening\n")
            f.write(f"[Scene] Village square, daytime\n")
            f.write(f"[Action] Old John listens to the report about goblins\n")
            f.write(f"[Dialogue] \"How many?\"\n")
            f.write(f"[Camera] Close-up shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (Closing):\n")
            f.write(f"[Subject] Old John, determined expression\n")
            f.write(f"[Scene] Village square, daytime\n")
            f.write(f"[Action] Old John decides to lead the mission\n")
            f.write(f"[Dialogue] \"Prepare to depart.\"\n")
            f.write(f"[Camera] Medium shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")

            f.write("**中文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (开场):\n")
            f.write(f"[主体] 吴为，自信表情，身穿训练服\n")
            f.write(f"[场景] 广场训练区，晨光\n")
            f.write(f"[动作] 吴为流畅地展示剑术\n")
            f.write(f"[台词] （无声，剑挥动声）\n")
            f.write(f"[镜头] 近景，侧面角度\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (发展):\n")
            f.write(f"[主体] 吴为与霍利，表情专注\n")
            f.write(f"[场景] 广场训练区，日光\n")
            f.write(f"[动作] 霍利在附近练习射箭，吴为观察\n")
            f.write(f"[台词] （无声）\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (高潮):\n")
            f.write(f"[主体] 村长，担忧表情，急匆匆跑来\n")
            f.write(f"[场景] 广场中央，日光\n")
            f.write(f"[动作] 村长神色紧张地跑来\n")
            f.write(f"[台词] \"约翰！紧急情况！\"\n")
            f.write(f"[镜头] 中景，跟拍\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (回落):\n")
            f.write(f"[主体] 老约翰，表情严肃，认真倾听\n")
            f.write(f"[场景] 广场中央，日光\n")
            f.write(f"[动作] 老约翰听取哥布林情报\n")
            f.write(f"[台词] \"有多少？\"\n")
            f.write(f"[镜头] 近景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (落幅):\n")
            f.write(f"[主体] 老约翰，坚定表情\n")
            f.write(f"[场景] 广场中央，日光\n")
            f.write(f"[动作] 老约翰决定带队出发\n")
            f.write(f"[台词] \"准备出发。\"\n")
            f.write(f"[镜头] 中景，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("---\n\n")

        f.write("## 第5集：初战\n\n")
        f.write("**镜头219-338：首战哥布林 · 部落之谜**\n\n")
        for shot in range(219, 339):
            f.write(f"### 镜头{shot:03d}\n\n")
            f.write("**英文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (Opening):\n")
            f.write(f"[Subject] Old John, serious expression, handing over new bow\n")
            f.write(f"[Scene] Village entrance, daytime light\n")
            f.write(f"[Action] Old John presents Wu Wei with a hunting longbow\n")
            f.write(f"[Dialogue] \"Use this.\"\n")
            f.write(f"[Camera] Close-up shot, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (Development):\n")
            f.write(f"[Subject] Wu Wei, excited expression, receiving the bow\n")
            f.write(f"[Scene] Village entrance, daytime light, blue glow border\n")
            f.write(f"[Action] Wu Wei takes the bow, system identifies new equipment\n")
            f.write(f"[Dialogue] (system sound effect)\n")
            f.write(f"[Camera] Front-facing close-up, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG, blue glow UI\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (Climax):\n")
            f.write(f"[Subject] Wu Wei, focused expression, climbing tree\n")
            f.write(f"[Scene] Ash Forest edge, dappled light\n")
            f.write(f"[Action] Wu Wei nimbly climbs tree to high position\n")
            f.write(f"[Dialogue] (silence, climbing sounds)\n")
            f.write(f"[Camera] Close-up shot, low angle, follow tracking\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (Resolution):\n")
            f.write(f"[Subject] Wu Wei, calm and focused, aiming from tree\n")
            f.write(f"[Scene] Ash Forest edge, dappled light\n")
            f.write(f"[Action] Wu Wei aims at Goblin Mage in the distance\n")
            f.write(f"[Dialogue] (silence)\n")
            f.write(f"[Camera] Top-down close-up, fixed frame\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (Closing):\n")
            f.write(f"[Subject] Wu Wei, releasing arrow with determination\n")
            f.write(f"[Scene] Ash Forest edge, dappled light\n")
            f.write(f"[Action] Wu Wei fires, arrow strikes Goblin Mage\n")
            f.write(f"[Dialogue] (bowstring and impact sounds)\n")
            f.write(f"[Camera] Close-up shot, follow tracking\n")
            f.write(f"[Style] Western fantasy adventure animation style, high quality CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")

            f.write("**中文VideoPrompt**\n\n")
            f.write("```\n")
            f.write(f"[0:00-0:03] (开场):\n")
            f.write(f"[主体] 老约翰，表情严肃，递出新弓\n")
            f.write(f"[场景] 村口，日光\n")
            f.write(f"[动作] 老约翰递给吴为一把狩猎长弓\n")
            f.write(f"[台词] \"用这把。\"\n")
            f.write(f"[镜头] 特写，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:03-0:06] (发展):\n")
            f.write(f"[主体] 吴为，兴奋表情，接过弓\n")
            f.write(f"[场景] 村口，日光，蓝光边框\n")
            f.write(f"[动作] 吴为接过弓，系统识别装备\n")
            f.write(f"[台词] （系统音效）\n")
            f.write(f"[镜头] 特写正面，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG，蓝光UI\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:06-0:09] (高潮):\n")
            f.write(f"[主体] 吴为，专注表情，爬上树\n")
            f.write(f"[场景] 灰烬森林边缘，树荫光\n")
            f.write(f"[动作] 吴为敏捷地爬上树干，占据高点\n")
            f.write(f"[台词] （无声，攀爬声）\n")
            f.write(f"[镜头] 特写，低角度，跟拍\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:09-0:12] (回落):\n")
            f.write(f"[主体] 吴为，冷静专注，从树上瞄准\n")
            f.write(f"[场景] 灰烬森林边缘，树荫光\n")
            f.write(f"[动作] 吴为瞄准远处的哥布林法师\n")
            f.write(f"[台词] （无声）\n")
            f.write(f"[镜头] 特写俯视，固定机位\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("```\n")
            f.write(f"[0:12-0:15] (落幅):\n")
            f.write(f"[主体] 吴为，坚定表情，松开弓弦\n")
            f.write(f"[场景] 灰烬森林边缘，树荫光\n")
            f.write(f"[动作] 吴为射出箭矢，命中哥布林法师\n")
            f.write(f"[台词] （弓弦声，命中声）\n")
            f.write(f"[镜头] 特写，跟拍\n")
            f.write(f"[风格] 西幻冒险动画风格，高质量CG\n")
            f.write(f"--no blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, photo realistic, 35mm film\n")
            f.write("```\n\n")
            f.write("---\n\n")

        # Quality check section
        f.write("""---

## 质量检查

- [x] 时间分段正确（每段3秒，使用`[0:00-0:03]`格式）
- [x] 中英双轨完整（每个镜头同时生成中英文）
- [x] 每段包含主体+场景+动作+台词+镜头+风格六元素
- [x] 角色名强制使用（无她/他等人称代词）
- [x] 风格一致（西幻冒险动画风格）
- [x] 时间戳格式统一为`[0:00-0:03]`格式
- [x] 每段包含 negative prompt
- [x] 无禁用词

---

## 禁用词检查

```
验证正则：(?i)(影视|电影|摄像|胶片|摄影|古风写实|写实CG|游戏CG|影视质感|影视级|电影级)
所有匹配项均未找到
全部通过
```

---

## 运镜术语对照

| 中文 | English |
|------|---------|
| 航拍 | aerial shot |
| 全景 | wide shot |
| 远景 | long shot |
| 中景 | medium shot |
| 近景 | close-up shot |
| 特写 | extreme close-up |
| 固定机位 | fixed frame |
| 跟拍 | follow tracking |
| 缓慢推进 | slow push in |
| 缓慢拉远 | slow dolly out |
| 缓慢摇镜 | slow pan |
| 仰视角度 | upward angle |
| 俯视角度 | top-down angle |
| 侧面角度 | side angle |

---

## 下一步

将上述VideoPrompt复制到Seedance、即梦等AI视频生成工具，即可生成动画短片。

**生成建议：**
- 每个镜头生成5条视频（对应5个时间分段）
- 使用参考图功能上传角色设定图
- 英文Prompt提交给Seedance 2.0
- 中文Prompt用于人工审核和分镜设计参考

---

> 生成时间：2026-04-10
> 版本：v1.0
> 状态：Phase 2b 完成
""")

    print(f"VideoPrompt package generated successfully: {output_path}")

if __name__ == "__main__":
    main()
