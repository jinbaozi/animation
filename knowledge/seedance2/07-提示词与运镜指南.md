# Seedance 2.0 提示词与运镜完全指南

> 来源：全网深度调研（2026年3月29日）
> 原文：飞书文档 - Seedance 2.0 提示词与运镜完全指南
> 重要更正：`Seedance` 是 MiniMax 视频模型的早期内部代号，已停用。当前正确名称为 **MiniMax Hailuo 2.3**（底层模型）/ **即梦AI**（C端产品）

---

## 一、核心提示词公式

### 基础公式（5要素结构）

```
[主体] + [动作/变化] + [场景/环境] + [运镜/镜头语言] + [风格/质感]
```

### 要素详解

| 要素 | 定义 | 写法要点 | 示例 |
|------|------|----------|------|
| **主体** | 视频核心对象 | 具体名词 + 外观描述 | `A young woman in a red dress` |
| **动作** | 动态行为/状态变化 | 动词-ing形式 | `walking slowly through the forest` |
| **场景** | 空间背景 | 时间 + 地点 + 天气/光线 | `in a misty bamboo forest at dawn` |
| **运镜** | 镜头语言 | 英文电影术语 | `slow dolly in, handheld` |
| **风格** | 视觉质感 | 风格关键词 | `cinematic lighting, volumetric light, 8K resolution` |

---

## 二、程度副词系统

### 速度类副词

| 程度 | 英文 | 速度感 | 适用场景 |
|------|------|--------|----------|
| 微速 | slowly, gently, subtly | 最慢 | 抒情、冥想、慢动作特写 |
| 中速 | steadily, moderately | 舒适 | 日常叙事、自然流动 |
| 快速 | quickly, briskly, nimbly | 快 | 轻快节奏、运动场景 |
| 极速 | rapidly, swiftly, fast | 很快 | 追逐、动作、打斗 |
| 猛然 | suddenly, abruptly, sharply | 瞬时 | 突发、惊讶、转折 |
| 暴力加速 | violently, frantically, explosively | 最快 | 爆炸、冲击、混乱 |

### 力度类副词

| 程度 | 英文 | 力度感 |
|------|------|--------|
| 轻柔 | gently, softly, delicately | 轻柔 |
| 中等 | firmly, resolutely | 中等 |
| 强劲 | powerfully, forcefully, intensely | 强劲 |
| 狂暴 | violently, savagely, brutally | 狂暴 |

---

## 三、@Tag 多模态引用系统

| 引用类型 | 上限 | 用途 |
|----------|------|------|
| @Image | 最多9张 | 参考图片中的主体外观/背景环境/色彩风格 |
| @Video | 最多3个 | 参考动作/运镜/节奏 |
| @Audio | 最多3个 | 参考音效/环境音/BGM |

### @Video 用法示例

```markdown
@Video1: Reference video of a dancer performing contemporary dance
Prompt: A martial artist replicating the fluid movements from @Video1

@Video1: A drone shot sweeping over mountains
Prompt: Apply the same aerial tracking movement from @Video1 to this cityscape
```

---

## 四、运镜类型完整列表

### 基础运镜

| 运镜类型 | 中文名称 | Prompt写法 |
|----------|----------|------------|
| Push in / Dolly in | 推进/前移 | `camera pushes in, dolly in, push forward, zoom in` |
| Pull out / Dolly out | 拉远/后移 | `camera pulls back, dolly out, pull back, zoom out` |
| Pan (horizontal) | 水平摇镜 | `camera pans left/right, pan shot, sweeping pan` |
| Tilt (vertical) | 垂直摇镜 | `camera tilts up/down, tilt shot, tilt upward` |
| Tracking / Follow | 跟踪拍摄 | `tracking shot, camera follows, follow shot` |
| Orbit / Circling | 环绕拍摄 | `orbiting camera, circling shot, 360-degree orbit` |
| Aerial / Drone | 航拍 | `aerial shot, drone footage, overhead shot` |
| Handheld | 手持跟拍 | `handheld shot, shaky cam` |
| Whip pan | 快速摇镜 | `whip pan, fast pan` |
| Crane up/down | 升降拍摄 | `crane shot, crane up, crane down` |
| Zoom | 光学变焦 | `zoom in, zoom out` |
| Dutch angle | 荷兰角/倾斜 | `Dutch angle, tilted camera` |
| POV / First-person | 主观视角 | `first-person perspective, POV shot` |
| Bird's eye / Top-down | 鸟瞰视角 | `bird's eye view, top-down shot` |
| Low angle | 低角度仰拍 | `low angle shot` |
| High angle | 高角度俯拍 | `high angle shot` |

### 进阶/特殊运镜

| 运镜类型 | 中文名称 | Prompt写法 |
|----------|----------|------------|
| Hitchcock zoom | 希区柯克变焦 | `Hitchcock zoom, dolly zoom` |
| Spiral / Helix | 螺旋运镜 | `spiral camera movement, helix shot` |
| Racking focus | 焦点转移 | `rack focus, shift focus` |
| Breathing camera | 呼吸感镜头 | `camera breathing` |
| Rapid cuts | 快切 | `rapid cuts, fast cuts, quick cuts` |
| Slow motion | 升格/慢动作 | `slow motion, slow-mo` |
| One-shot | 一镜到底 | `one continuous shot, no scene cuts` |
| Match cut | 匹配剪辑 | `match cut` |
| Over-the-shoulder | 过肩镜头 | `over-the-shoulder shot, OTS` |
| 360 orbit | 360环绕 | `360 orbit, full rotation` |
| Snap zoom | 快速变焦 | `snap zoom, rapid zoom` |
| Parallax pan | 视差摇镜 | `parallax pan` |

---

## 五、景别系统

| 景别 | 英文 | 用途 |
|------|------|------|
| 大远景/极远景 | Extreme Wide Shot / Establishing | 建立场景 |
| 远景 | Wide Shot | 交代环境 |
| 全景 | Full Shot | 完整人物 |
| 中景 | Medium Shot / Mid Shot | 对话/叙事 |
| 中近景 | Medium Close-up | 情绪 |
| 近景/特写 | Close-up / CU | 聚焦 |
| 大特写 | Extreme Close-up / ECU | 细节 |
| 面部特写 | Face Close-up | 表情 |
| 两人镜头 | Two Shot | 关系 |
| 过肩镜头 | OTS | 对话 |

---

## 六、镜头角度

| 角度类型 | 英文/写法 | 效果 |
|----------|----------|------|
| 平视 | Eye-level | 自然 |
| 仰拍/低角度 | Low-angle / Upward | 威严/压抑 |
| 俯拍/高角度 | High-angle / Downward | 渺小/无助 |
| 鸟瞰/正交俯视 | Bird's eye / Top-down | 上帝视角 |
| 荷兰角/倾斜 | Dutch angle / Tilted | 不安/紧张 |
| 主观视角 | POV / First-person | 沉浸 |
| 鱼眼视角 | Fisheye | 扭曲/压迫 |
| 长焦压缩 | Telephoto compression | 空间压缩 |
| 浅景深 | Shallow DOF | 虚化背景 |
| 深景深 | Deep focus | 全清晰 |

---

## 七、速度控制

| 速度描述 | Prompt写法 |
|----------|------------|
| 极快推进 | `rapidly pushes in, snaps forward, explosive push-in` |
| 快速推进 | `quick push in, fast dolly, rapid dolly in` |
| 匀速推进 | `slowly pushes in, gradual push forward` |
| 缓慢推进 | `glacially slow push, creeping dolly, 缓推` |
| 缓慢拉远 | `slowly pulls back, gradually revealing` |
| 变速推进 | `accelerating dolly, speed accelerates like a roller coaster` |

---

## 八、分段时间戳组合（9秒以上推荐）

```markdown
0-3秒：[画面描述 + 镜头语言]
4-8秒：[画面描述 + 镜头语言]
9-15秒：[画面描述 + 镜头语言]

示例（15秒仙侠镜头）：
0-3秒：低角度特写主角蓝袍衣摆被热浪吹得猎猎飘动
4-8秒：环绕摇镜快切，主角旋身挥剑
9-15秒：镜头缓推特写剑修侧脸，音效渐弱
```

---

## 九、与竞品对比

| 平台 | 运镜精准度 | 运镜多样性 | 运镜描述自由度 | 核心优势 |
|------|------------|------------|----------------|----------|
| **Seedance 2.0** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | @引用语法最强、动作与运镜解耦 |
| Kling 3.0 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Motion Control领先 |
| Sora 2 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 品牌背书、Characters功能 |
| Runway Gen-4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | VBench评测世界第一 |
| Veo 3 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 物理真实感最强、原生音频 |
| Pika 2.0 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 操作最简单 |

### Seedance 2.0 独特优势

1. **@引用语法**：可同时传入9张图+3个视频+3个音频
2. **动作与运镜解耦**：`reference @video1 for movement, reference @video2 for camera`
3. **分段时间戳**：0-3s / 4-8s / 9-15s 分段控制运镜变化

---

## 十、实战提示词库

### 风景类

```
A lone wolf howling at the full moon on a snowy mountain peak,
aerial drone shot slowly circling,
fog rolling through the valley,
blue moonlight casting long shadows,
cinematic, nature documentary style
```

### 人物特写

```
Close-up portrait of a tear rolling down a woman's cheek,
slow-motion,
soft diffused lighting,
shallow depth of field,
cinematic color grading,
anamorphic lens flare,
emotional film still
```

### 动作场景

```
A martial artist performing a spinning kick in mid-air,
briskly and with power,
dust particles swirling around,
dynamic low angle shot,
cinematic lighting, volumetric light beams,
action movie style
```

### 动漫风格

```
A chibi anime girl catching a falling cherry blossom petal,
gentle breeze,
sakura petals floating around,
Studio Ghibli inspired,
soft watercolor background,
cel-shaded character,
golden hour lighting
```

---

## 十一、已知问题与限制

| 问题 | 严重程度 | 说明 |
|------|----------|------|
| 时长上限12秒 | ⭐⭐⭐ | 需多段拼接 |
| 无4K输出 | ⭐⭐ | 目前最高1080p |
| 手部生成不稳定 | ⭐⭐⭐⭐ | 手指数量/形态异常是常见问题 |
| 文字渲染不支持 | ⭐⭐⭐ | 视频中无法生成可读文字 |
| 多人场景 | ⭐⭐⭐⭐ | 超过3人时角色一致性急剧下降 |
| 无原生音频生成 | ⭐⭐⭐ | 对比Veo 3/Sora 2的明显差距 |

---

## 十二、Do vs Don't 详细对照

| 场景 | ✅ Do | ❌ Don't |
|------|-------|----------|
| 人物特写 | `close-up, soft lighting` | `close-up of hands typing` |
| 动作场景 | `slow motion, dramatic` | `fast cut, multiple angles simultaneously` |
| 风景 | `aerial, golden hour` | `crowded scene with many people` |
| 产品 | `360° orbit, studio lighting` | `product rotating while floating in space` |

---

## 十三、生成前8项自检

1. 是否选择了"非固定镜头"模式？
2. 提示词是否≤150词？
3. 是否≤2个主要人物？
4. 是否避免了"手"的精细动作描写？
5. 运镜描述是否单一（不冲突）？
6. 光线描述是否具体？
7. 风格标签是否≤2个？
8. 是否用英文撰写提示词？

---

## 十四、实战案例（24个精选）

详见 `Seedance2_cases.md`，覆盖：
- 水下纪录片（追踪镜头）
- 动漫樱花武士武士场景×4变体
- 漫画风格×4变体
- 女性特写×4变体
- 品牌广告×4变体

---

## 十五、参考资源

| 资源 | 链接 |
|------|------|
| Seedance官方技能包 | github.com/zhanghaonan777/Seedance2-skill |
| awesome-seedance-2-guide | github.com/EvoLinkAI/awesome-seedance-2-guide |
| awesome-seedance | github.com/ZeroLu/awesome-seedance |
| awesome-seedance-2-prompts | github.com/YouMind-OpenLab/awesome-seedance-2-prompts |
| seedance2prompt.org | seedance2prompt.org |
