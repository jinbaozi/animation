# 影视摄影机镜头提示词知识库 - NotebookLM 知识库补充

> Supplementary Knowledge from NotebookLM Knowledge Base
> NotebookLM 来源: https://notebooklm.google.com/notebook/f56bd450-598b-4a97-938c-ae8b9c77ab2e
> 更新时间: 2026-04-06

---

## 1. 电影级摄影/镜头 AI 生成提示词 (Cinematic Camera & Lens Prompting)

### 画幅与传感器

| 描述词 | 作用 |
|--------|------|
| `shot on 35mm cinema camera` | 确立电影画幅基调 |
| `full-frame sensor depth` | 全画幅传感器景深 |
| `ARRI Alexa 65` | 顶级电影机，宽宽容度 |
| `RED V-Raptor` | 高分辨率电影机 |

### 镜头与光学特性

| 描述词 | 效果 |
|--------|------|
| `anamorphic lens compression and oval bokeh` | 模拟变形镜头特有畸变和椭圆形光斑 |
| `cinematic shallow depth of field` | 电影级浅景深 |
| `macro close-up with razor-thin focus plane` | 极薄焦平面的微距特写 |
| `deep depth of field` | 全景清晰 |

### 移焦效果 (Rack Focus)

```
Rack focus / Shift focus（移焦）
示例：将焦点从前景中人物的表情转移到身后墙上的照片
```

### 特定焦段描述

| 焦段 | 描述词 | 效果 |
|------|--------|------|
| 50mm | `50mm lens` | 标准视角，自然透视 |
| 超广角 | `Ultra-wide angle lens` | 夸张透视感 |
| 长焦 | `Telephoto lens` | 压缩空间感 |

---

## 2. 胶片级高光与影视质感 (Film-like Highlight Roll-off & Aesthetics)

### 高光与色彩控制

| 描述词 | 效果 |
|--------|------|
| `soft bloom on highlights` | 高光处柔和泛光，模拟胶片渐变 |
| `high dynamic range with deep shadows and controlled highlights` | 高动态范围，深邃阴影与受控高光 |
| `film-like highlight roll-off` | 胶片级高光滚落 |

### 胶片颗粒与质感

| 描述词 | 效果 |
|--------|------|
| `subtle film grain and analog texture` | 微妙胶片颗粒感和模拟纹理 |
| `35mm film` | 35毫米胶片质感 |
| `film-grade color grading in the style of modern cinema` | 现代电影风格胶片级调色 |
| `Kodak Portra 400` | 人像/婚礼摄影胶片，柔和暖调 |
| `Cinestill 800T` | Tungsten 灯下电影质感，Halation 效果 |
| `Fuji Provia` | 鲜艳色彩，高对比度 |
| `Kodak Vision3 500T` | 电影级，宽色域 |

### 光学"不完美"瑕疵

| 描述词 | 效果 |
|--------|------|
| `real-world imperfections: motion blur, rolling shutter, lens flare` | 真实世界瑕疵 |
| `cinematic anamorphic lens flares` | 电影级变形镜头光晕 |
| `lens dust` | 镜头灰尘 |
| `micro-scratches` | 微小划痕 |

---

## 3. 影视风格 AI 生成专业技巧 (Professional Techniques)

### 电影级布光体系 (Lighting)

| 布光类型 | 描述词 | 效果 |
|----------|--------|------|
| 三点布光 | `Cinematic three-point lighting` | 人物从背景中突出 |
| 伦勃朗光 | `Rembrandt lighting` | 脸颊倒三角高光，增强立体感 |
| 体积光 | `Volumetric lighting` / `Tyndall effect` | 空气中的灰尘感和光束 |
| 黄金时段 | `golden hour directional sunlight with long shadows` | 自然电影氛围 |
| 窗户光 | `Soft window light` | 柔和漫反射光 |
| 冷调光 | `Cool cinematic lighting` | 现代科技感 |

### 真人级生物质感 (Human Realism)

**皮肤质感：**
| 描述词 | 效果 |
|--------|------|
| `Subsurface scattering` | 次表面散射/皮肤半透明感 |
| `visible micro-texture, uneven pore density` | 微细纹理、毛孔密度不均 |
| `faint peach fuzz` | 细小绒毛 |

**五官细节：**
| 描述词 | 效果 |
|--------|------|
| `Natural sclera tone (not pure white)` | 非纯白的自然巩膜色 |
| `asymmetrical catchlight` | 不对称的眼神光 |
| `authentic facial micro-expressions` | 真实的细微表情 |
| `natural eye movement and blinking patterns` | 自然的眼球运动与眨眼 |

---

## 4. 视频运镜指令 (Camera Movement)

### 手持与纪实感

| 描述词 | 效果 |
|--------|------|
| `Dynamic handheld movement with natural micro-jitters` | 动态手持移动伴随自然微小抖动 |
| `Handheld camera` | 手持摄影 |

### 动态跟踪与推进

| 描述词 | 效果 |
|--------|------|
| `Smooth Steadicam tracking shot` | 平滑斯坦尼康跟随镜头 |
| `Tracking shot` | 跟拍 |
| `Slow cinematic push-in` | 缓慢电影级推轨 |
| `Zoom in` | 放大 |
| `Pull out` | 拉镜头，展现全景 |

### 戏剧化与紧张感

| 描述词 | 效果 |
|--------|------|
| `Dutch angle` / `Tilt` | 荷兰角/倾斜镜头，传达不安 |
| `Whip pan` | 快速摇摄，产生运动模糊残影 |
| `Vertigo effect` / `Dolly zoom` | 眩晕效果，主体不变背景透视扭曲 |

### 空间与环境调度

| 描述词 | 效果 |
|--------|------|
| `Arc shot` / `360° Panning` | 弧形拍摄/动态环绕 |
| `Crane shot` | 摇臂/升降镜头 |
| `Aerial shot` / `Drone shot` | 航拍/无人机拍摄 |
| `Rack focus` / `Shift focus` | 移焦，引导视线 |

---

## 5. 综合提示词示例模板 (Example Templates)

### 黄金公式

```
[镜头语言/景别 + 光影] + [主体及微观特征] + [主体动作] + [场景环境] + [氛围/电影质感/光学瑕疵]
```

### 示例 1：人物情绪特写

```
Extreme close-up shot of a humanoid robot face, shot on 35mm cinema camera. Pale gray metallic skin texture with subsurface scattering, uneven pore density. Eyes are two ice-blue glowing points, asymmetrical catchlight. The robot's expression is neutral but with subtle micro-movements. Cinematic three-point lighting, neon lights from the background cast red and purple reflections. Anamorphic lens compression, cinematic shallow depth of field. Soft bloom on highlights, subtle film grain, lens dust. Cyberpunk aesthetic, 8K, photorealistic.
```

### 示例 2：动态大场景

```
Wide-angle establishing shot with realistic lens distortion. A chaotic cyberpunk market alleyway. The camera pushes in slowly (Steadicam tracking shot). Dense ambient soundscape implied, cinematic environmental fog and light scattering (Volumetric lighting). Golden hour directional sunlight with deep shadows and controlled highlights. High-budget film aesthetic, real-world imperfections: motion blur, rolling shutter, cinematic anamorphic lens flares.
```

### 示例 3：终极肌肤细节特写

```
Macro close-up with razor-thin focus plane, cinematic three-point lighting. A 25-year-old woman, visible micro-texture, uneven pore density, faint peach fuzz, natural sclera tone with asymmetrical catchlight. She tilts her head slightly, natural eye movement and blinking patterns. Standing in a dimly lit cyberpunk alleyway, neon lights cast red and purple reflections on her wet skin. Shot on 35mm cinema camera, anamorphic lens compression and oval bokeh. Subtle film grain, lens dust, soft bloom on highlights, teal-and-orange cinematic color palette, 8K, photorealistic.
```

---

## 6. AI 视频生成平台提示词技巧

### Sora / Runway Gen-3 / Kling (可灵) / Veo 3

| 技巧 | 描述 |
|------|------|
| 运镜优先 | 在提示词开头指定 camera movement |
| 动作拆解 | 将动作拆解为单一微动态 (Micro-Dynamics) |
| 光影变化 | 描述光线随时间的变化 |
| 避免重复 | 不在视频提示词中重复首帧已有的静态信息 |

### Camera Movement 关键词库

| 分类 | 关键词 |
|------|--------|
| 稳定移动 | `Steadicam`, `tracking shot`, `push-in`, `pull out` |
| 手持感 | `handheld`, `dynamic movement`, `micro-jitters` |
| 戏剧化 | `Dutch angle`, `whip pan`, `dolly zoom` |
| 空间感 | `arc shot`, `crane shot`, `aerial`, `drone shot` |
| 对焦 | `rack focus`, `shift focus` |

---

## 7. 色彩调色提示词 (Color Grading)

| 调色风格 | 描述词 |
|----------|--------|
| 青橙色调 | `teal-and-orange cinematic color palette` |
| 柔和大地色 | `muted earth tones` |
| 现代电影 | `film-grade color grading in the style of modern cinema` |
| 专业级调色 | `professional-grade color grading` |
| 漂白旁路 | `bleach bypass` - 高对比度低饱和 |
| 单色电影 | `monochromatic film look` |

---

## 8. 注意事项 (Precautions)

### 视频生成注意事项

| 错误做法 | 正确做法 |
|----------|----------|
| 在 I2V 视频提示词中重复静态描述 | 100% 聚焦动作、运镜、情绪和光影变化 |
| 使用"没有XX"的否定句式 | 直接在 Negative Prompt 中填写客观名词 |
| 一次性描述复杂连招动作 | 拆解为单一微动态 |
| 使用"no simplified shading" | 使用 `realistic shading` |

### Negative Prompt 常用词

```
blurry, deformed hands, artificial structures, plastic skin, mannequin,
oversaturated, cartoonish, excessive smoothing, dead eyes, wrong anatomy
```

### 镜头平替策略

当无法直接使用品牌名时，用特性描述替代：

| 品牌 | 平替描述词 |
|------|-----------|
| ARRI Alexa | `35mm cinema camera, high dynamic range, film-like highlight roll-off` |
| Cooke S4 | `warm color palette, natural soft diffused lighting, organic tone` |
| Zeiss Master Prime | `razor-thin focus plane, hyper-realistic textures, zero distortion` |
| Anamorphic | `oval bokeh, lens compression, anamorphic flares` |

---

## 9. 完整结构化提示词模板

### 图像生成模板

```
[Shot Type] + [Camera/Lens] + [Subject Description] + [Lighting] + [Environment] + [Color/Texture/Mood] + [Technical Specs]

示例：
Cinematic extreme close-up, shot on ARRI Alexa 65 with Zeiss Master Prime lens.
[Subject] A woman with visible micro-texture skin, asymmetrical catchlight in her eyes...
[Lighting] Rembrandt lighting from the left, volumetric fog...
[Environment] Cyberpunk alleyway, neon reflections...
[Style] Teal-and-orange palette, subtle film grain, anamorphic flares...
[Specs] 8K, photorealistic, professional color grading
```

### 视频生成模板

```
[Camera Movement] + [Subject Action] + [Lighting Changes] + [Environment] + [Mood] + [Technical Quality]

示例：
Steadicam tracking shot, the woman slowly tilts her head. Natural eye movement and blinking.
Volumetric lighting shifts from warm to cool as the sun sets. Dense atmospheric fog.
Tense, melancholic mood. Shot on 35mm cinema camera, anamorphic lens compression.
Soft bloom on highlights, subtle film grain, 4K cinematic quality.
```

---

## 10. 来源与参考

- NotebookLM 知识库: https://notebooklm.google.com/notebook/f56bd450-598b-4a97-938c-ae8b9c77ab2e
- 全网搜索资源: `/Users/godxu/02-workspace/animation-v3/docs/knowledge/影视摄影机镜头提示词知识库.md`
