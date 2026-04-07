# Seedance 2.0 NotebookLM补充

> 版本：v2.0 | 日期：2026-04-05
> 来源：NotebookLM知识库实时查询（2026-04-05）

---

## 十一、NotebookLM深度技巧（2026-04-05实时查询补充）

> 本节内容来源于NotebookLM知识库实时查询（URL: `https://notebooklm.google.com/notebook/f56bd450-598b-4a97-938c-ae8b9c77ab2e`），为本指南最权威的来源之一。

### 11.1 对话场景的导演级技巧

**过肩镜头（Over-the-Shoulder）—— Seedance 2.0对话场景首选运镜**

在对话场景中，使用"肩部视角/过肩镜头"，即从一个人的身后取景，透过其肩部看向另一个人。这能体现角色间的空间关系和视线交互。

```
Prompt写法：
  镜头：Over-the-shoulder shot, from [说话者A] behind shoulder looking at [说话者B]
```

**移焦（Rack Focus）—— 单镜头内展示注意力转移**

为了在单镜头内展现对话焦点的变化：
```
Prompt写法：
  镜头：Rack focus from [前景人物] thoughtful expression to [背景中的某物体/人物]
  示例："将焦点从前景中人物若有所思的表情，转移到其身后墙上的一张照片"
```

**中景用于对话（Medium Shot，腰部以上）**

对话时通常使用中景，显示腰部以上，在细节和环境之间取得平衡。
```
Prompt写法：
  镜头：Medium shot, both characters visible from waist up, engaged in conversation
```

### 11.2 微动作系统（Micro-movements）

**核心原则：提示词不能只写模糊的形容词（如"悲伤"），必须将其拆解为具体、可执行的细微动作。**

| 情绪 | 错误写法（太模糊） | 正确写法（微动作） |
|------|-------------------|--------------------|
| 沉思 | `thinking deeply` | `neutral expression but with subtle micro-movements suggesting inner contemplation, eye-lights flicker gently twice` |
| 温柔 | `gently touching` | `fingertips barely graze the cheek, pause for a beat, then slowly slide down` |
| 紧张 | `nervous` | `hands fidget with the hem of the sleeve, eyes dart briefly to the side then return` |
| 感动 | `touched` | `lips part slightly, a single tear forms but does not fall, eyes shimmer` |

**Seedance 2.0运动幅度设置：**

- **推荐设置为Medium（中等）**
- 太高：画面容易崩坏变形
- 太低：缺乏动感，画面静止
- 如果生成的动作过于夸张，**优先修改提示词**（如将"轻轻闪烁两次"改为"微微闪烁一次"），而不是盲目重新生成

**景别配合情绪的硬性规则：**

- 情感爆发的戏份**务必**使用**特写（Close-up）或极近特写（ECU）**来聚焦瞳孔、泪水等面部细节
- 大场面则用远景（Wide shot）
- **切忌全程使用中景**，否则情绪会很平淡

### 11.3 动作戏避坑指南

**AI视频模型目前的局限性：**

1. **必须拆解为单一动作**：不要在一段提示词中写入一套连招，必须将角色动作拆解到可执行的单一动作
2. **主攻"微动态"**：动作幅度不要太大。AI生成"微动态"（头发飘动、衣服随风摆动、眨眼、光影变化）最有质感且最不容易崩坏
3. **借助特效掩盖**：在玄幻或武打短剧中，可以利用AI生成的光影特效、魔法渲染来增强视觉张力，从而弥补肢体动作的不足

**动作幅度对比：**
```
过于复杂（AI难以处理）：
  "夜华连续三刺剑法，第一刺被挡，第二刺破防，第三刺击中对方"

拆解为单一动作（推荐）：
  0-3s：夜华握剑后撤，重心下沉，准备出击
  3-6s：夜华猛然向前突刺一剑
  6-9s：剑尖击中敌人，剑身剧烈震动
```

### 11.4 一致性保障：图生视频垫图法

**这是Seedance 2.0保持角色一致性的最重要技术。**

1. **首帧参考图垫图**：先用图像模型（如Midjourney通过`--cref`参数或NanoBanana 2）生成极其稳定的人物三视图和场景图
2. **在Seedance中必须上传这张图作为首帧图片**，否则角色一定会发生形变
3. **忽略静态，专写动态**：由于模型已经能"看到"你上传的首帧参考图，视频提示词中**不需要重复描述角色的长相或场景静态布局**。提示词应100%专注于动态变化（动作、运镜、光影流转）
4. **统一光效关键词**：为了防止场景切换时风格割裂，在同一个场景的所有分镜提示词中，**必须加上相同的光效关键词**，如`cinematic lighting`、`volumetric lighting`等

```
一致性保障三步法：

步骤1：生成角色首帧参考图
  Midjourney: --cref [角色图] --v 5 --v2

步骤2：在Seedance中上传首帧图
  → 提示词不再需要写角色外观描述
  → 提示词只写：动作 + 运镜 + 光影流转

步骤3：统一光效关键词（全场景）
  → 每个镜头的Prompt末尾都加上：cinematic lighting, volumetric light
```

### 11.5 "AI魔改"政策红线

**坚决不能踩内容合规红线：**

1. **严禁对以下题材进行颠覆性篡改、"魔性"解构、恶搞或低俗化改编：**
   - 四大名著
   - 经典影视IP
   - 历史题材
   - 革命题材
   - 英模人物

2. **视频内容禁止：**
   - 渲染血腥暴力
   - 猎奇低俗
   - 违背公序良俗

3. **必须在显著位置标注"AI生成"字样**

### 11.6 Negative Prompt正确写法

**不要用带有指令性语法的词汇（如"不要显示墙"、"没有多余的手指"），而应直接输入你不想看到的客观名词。**

```
错误写法（指令性）：
  --no dont show walls, no extra fingers, remove blurred background

正确写法（客观名词）：
  --no walls, deformed hands, extra fingers, blurred background, text, watermark
```

### 11.7 关键建议合集

| 建议项目 | 具体操作 | 原因 |
|---------|---------|------|
| **使用英文提示词** | Seedance 2.0及大多数主流视频模型对英文的理解远好于中文 | 生成结果质量更高 |
| **单镜头时长控制在4-5秒** | 极限不超过10-15秒。视频太长极易导致画面变形、动作崩坏、出现幻觉 | AI模型注意力有限 |
| **优先修改提示词而不是重新生成** | 如果生成的动作过于夸张，修改提示词降低幅度描述 | 重新生成浪费token且不保证改善 |
| **动作幅度用Medium** | Seedance 2.0专用设置 | 防止画面崩坏 |
| **提示词≤150词** | 不要堆砌冗长描述 | 模型注意力有限 |

---

## 十二、NotebookLM进阶查询补充（第二轮深度查询）

### 12.1 口型同步规则（Lip-Sync）

当角色在对话中不说话时，嘴巴必须保持自然状态，避免出现不自然的抖动：

- **LivePortrait 工具**：启用 `lip_zero` 参数（阈值建议 0.03），抑制角色未说话时的非自然嘴部抖动
- **Seedance 2.0 提示词**：明确描述非说话角色的嘴部状态
  ```
  对话中不说话的角色：mouth closed naturally, lips gently pressed together, no mouth movement
  ```

### 12.2 皮肤质感与真实感检查清单

为了消除"AI塑料感"，让面部表情更有机真实，Prompt 中应包含以下生理细节：

| 质感维度 | 英文Prompt写法 | 效果 |
|---------|---------------|------|
| 光线穿透皮肤 | `subsurface scattering on skin` | 真实皮肤透光感 |
| 微妙纹理 | `visible micro-texture on face` | 非光滑塑料皮肤 |
| 毛孔密度不均 | `uneven pore density across skin surface` | 增加真实度 |
| 绒毛 | `faint peach fuzz on cheekbone` | 皮肤细节 |
| 眼白自然色调 | `natural sclera tone with subtle blood vessels` | 不完美但真实的眼睛 |
| 光学缺陷 | `film grain, slight lens flare` | 模拟真实相机 |
| 色差/色散 | `chromatic aberration on edges` | 电影感镜头效果 |

**效果对比：**
```
错误（塑料感）：
  "She looked at him with beautiful clear blue eyes, smooth flawless skin"

正确（有机真实感）：
  "Her expression is neutral with subtle micro-movements. Visible micro-texture on her pale skin, faint peach fuzz on her cheekbones, natural sclera tone in her eyes, subsurface scattering from the warm backlight, subtle film grain throughout"
```

### 12.3 音频情感标签系统

对于配音和口型同步音频（ElevenLabs），需要在剧本中加入情感标签：

**音频情感标签格式：**
```
剧本格式：
  "你要走了？" [whispers, voice trembling] 她问道。

常用标签：
  [laughs]        — 笑声
  [whispers]      — 耳语
  [sighs]         — 叹息
  [crying]        — 哭泣
  [gasps]         — 倒吸一口气
  [chuckles]      — 轻笑
```

**配音工具设置（ElevenLabs / 类似工具）：**

| 参数 | 推荐值 | 效果 |
|------|--------|------|
| Stability（稳定性） | 0.3-0.5（高情感） | 值越低声音越不稳定但更富变化，适合情感戏 |
| Style Exaggeration（风格强化） | 10-15% | 值越高越戏剧化 |

### 12.4 人物锁定技术进阶

**Midjourney 角色一致性锁定：**

| 场景 | 参数 | 说明 |
|------|------|------|
| 完全锁定（脸+发型+服装） | `--cref [角色URL] --cw 100` | 保持角色在所有镜头中外观一致 |
| 仅锁定脸型（换衣服/换发型） | `--cref [角色URL] --cw 0` | 保持面部相似但允许改变服装或发型 |
| 风格锁定 | `--sref [风格图URL]` | 统一全场景的色调和纹理 |

**Seedance 2.0 + Midjourney 工作流推荐：**
```
1. Midjourney生成角色图: MJ -> --cref URL -> 生成角色标准图
2. 上传种子帧图到Seedance: 使用角色标准图作为首帧输入
3. 视频提示词专注于动态: 不再描述角色外观，只写动作+运镜+光影
4. 统一光效: 所有镜头加入相同光影关键词
```

### 12.5 多角度空间一致性保障

当涉及复杂相机运动时，为防止背景扭曲变形：

**方法：预生成同一环境的四个角度**
```
环境角度生成清单：
  □ 正面视角图 — 建立空间主体
  □ 侧面视角图 — 确认侧方空间
  □ 背面视角图 — 确认后方空间
  □ 俯视视角图 — 确认平面关系

使用这四张图喂给视频模型，能提供丰富的3D空间数据，
保持环境在复杂镜头运动中的稳定性。
```

### 12.6 法律红线与版权保护

**作品完整权保护（法律）：**
对经典 IP 进行颠覆性篡改、"魔性"解构、恶搞或低俗化改编，违反了法律中的**"保护作品完整权"**（Right to Protect the Integrity of a Work）。

**肖像权保护（法律）：**
对历史人物、英模人物进行篡改，还侵犯了**肖像权**（Portrait Rights）。

**版权保护建议：**
```
1. 所有最终 AI 内容必须在显眼位置标注"AI生成"水印
2. 通过区块链时间戳提供提示词和参数日志作为版权证据
3. 保留所有生成记录和版本迭代历史
```

### 12.7 音频长度限制

对于使用 ElevenLabs 或其他 TTS 平台：
- **超过4分钟**的音频：音量会逐渐衰减到接近无声
- **解决法案**：将文本拆分为 **60秒或更短** 的片段（约 860 个单词），然后拼接起来

### 12.8 Seedance 2.0 运动幅度参数总结

| 设置 | 说明 | 推荐值 |
|------|------|--------|
| Motion Amplitude（运动幅度） | 控制画面动态变化程度 | **Medium** |
| 太高会怎样 | 人物变形、画面崩坏、动作诡异 | 避免 |
| 太低会怎样 | 静态如死水、缺乏动感和吸引力 | 避免 |
| 运动不完美时 | **修改提示词降低幅度描述**，而非盲目重新生成 | 优先 |
