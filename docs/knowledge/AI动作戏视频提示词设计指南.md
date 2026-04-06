# AI动作戏视频提示词设计指南

> AI Action Scene Video Prompt Design Guide
> 更新时间: 2026-04-06
> 来源: 多平台搜索调研 (Midjourney, Stable Diffusion, Seedance 2.0, Kling, Sora, Veo 3, Runway Gen-3 等)

---

## 目录

1. [AI动作戏视频提示词设计与一致性](#1-ai动作戏视频提示词设计与一致性)
2. [Lighting和Texture消除AI塑料感](#2-lighting和texture消除ai塑料感)
3. [打斗戏的专业镜头语言指令](#3-打斗戏的专业镜头语言指令)
4. [手持拍摄进阶技巧](#4-手持拍摄进阶技巧)
5. [AI视频质量审核体系](#5-ai视频质量审核体系)

---

## 1. AI动作戏视频提示词设计与一致性

### 1.1 人物一致性保证的核心策略

AI生成动作戏时，人物一致性是最大挑战。当前主流AI视频模型（Seedance 2.0、Kling 2.5、Veo 3、Sora 2 Pro）在多镜头连续生成中均存在人物漂移（Character Drift）问题。以下是经过验证的应对策略：

#### 角色描述词固定化（Character Bible）

在生成任何镜头前，建立标准化的角色描述词库，包括：

| 描述维度 | 必须包含内容 | 示例 |
|---------|-------------|------|
| 面部特征 | 脸型、眼型、鼻型、唇形 | 鹅蛋脸, 杏核眼, 薄唇 |
| 肤色质感 | 肤色、冷暖调、质感描述 | 病态苍白, 亚光质感 |
| 发型发色 | 发型、颜色、长度 | 黑色长发, 及腰 |
| 服装铠甲 | 颜色、材质、关键配饰 | 深红色丝绸长袍, 银色腰带 |
| 体型特征 | 身高、体型特征 | 纤细单薄, 约170cm |
| 独特标记 | 胎记、伤疤、刺青等 | 左眼角有泪痣 |

**关键原则：每个角色使用同一套固定描述词组合，绝不在不同镜头中改变描述。**

#### 参考图像策略（Reference Chaining）

多镜头动作戏推荐流程：
1. **角色定妆照**：先单独生成角色的4-view（正面/侧面/背面/面部特写）全身图
2. **参考图复用**：在后续所有动作镜头提示词中引用该参考图
3. **Seedance 2.0实测**：3张参考图+简单提示词即可完成多镜头打斗序列

```
Seedance 2.0 动作戏示例提示词：
Multi-shot fight scene generated with 3 reference images.
Reference: [角色4-view定妆照]
Action: martial arts combat between two women, modern urban environment
Camera: dynamic tracking, Dutch angle during impact moments
Style: cinematic, 4K quality
```

#### Subject → Action → Camera → Style → Constraints 框架

Seedance 2.0社区基准测试表明，该结构化框架可将运动漂移（Motion Drift）减少最高70%：

| 位置 | 内容 | 示例 |
|------|------|------|
| 主体 | 角色名称+核心特征 | 李青云，身着深红丝绸长袍 |
| 动作 | 具体动作分解 | 右腿侧踢，左手格挡 |
| 相机 | 镜头运动方式 | handheld tracking, Dutch angle |
| 风格 | 电影质感/光线 | golden hour, volumetric fog |
| 约束 | 负面约束/禁止项 | no excessive motion blur |

### 1.2 场景一致性保持方法

| 方法 | 说明 | 适用场景 |
|------|------|---------|
| 场景描述词固定化 | 锁定场景核心元素（建筑风格、光线、色调） | 室内外交替 |
| 空间坐标锚定 | 明确角色相对位置（东西南北方位） | 多人打斗 |
| 色调锁定 | 使用同一色彩描述词组合 | 全片统一 |
| 天气/时间锁定 | 一旦设定不轻易改变 | 跨越多天的剧情 |

### 1.3 动作戏常见不合理内容及解决方法

#### 常见AI生成错误

| 错误类型 | 具体表现 | 发生原因 |
|---------|---------|---------|
| 物理逻辑错误 | 一个人被石头砸中变成流星砸来 | 力量传递不符合物理常识 |
| 关节扭曲 | 手脚弯折角度超过生理极限 | 动作幅度超出AI理解范围 |
| 武器消失/穿越 | 刀剑穿过身体无接触 | 碰撞检测失效 |
| 重量感缺失 | 打击感轻飘无力 | 缺少力反馈描写 |
| 服装/头发不随动 | 打斗中服饰静止不动 | 缺少物理模拟 |

#### 解决方法：动作逻辑约束提示词

**原则：描述符合物理定律的动作，而非超现实的"魔法"效果**

| 问题 | 错误提示词 | 正确提示词 |
|------|-----------|-----------|
| 物理不合理 | `character flies backward 10 meters after hit` | `character staggers back two steps, loses balance` |
| 关节扭曲 | `impossible martial arts pose` | `right leg sweep, left arm blocks` |
| 力量传递 | `one punch sends enemy flying` | `fist connects with opponent's jaw, head snaps sideways` |
| 武器交互 | `sword passes through body` | `blade slashes across shoulder, blood splatters` |
| 重量感 | `lightweight combat` | `heavy sword swings with momentum, dust rises on impact` |

#### 复合动作拆解策略

不要在一个提示词中描述一整套连招。将复杂动作拆解为**单一微动态（Micro-Dynamics）**：

```
错误示例（复杂连招）：
A martial artist performs a spinning kick, followed by a punch,
then a sweep, then a throw - all in one 5-second clip.

正确示例（微动态拆解）：
Take 1: Spinning hook kick - camera tracks the arc of the leg
Take 2: Opponent staggers from impact - camera push-in on reaction
Take 3: Immediate follow-up punch - handheld for impact shake
Take 4: Sweep attempt - camera low angle
Take 5: Throw executed - camera crane up to show technique
```

### 1.4 动作戏分镜提示词设计技巧

#### 六层框架结构

```
[Camera Style] + [Scene Description] + [Character Details] + [Action/Motion] + [Lighting/Mood] + [Technical Specs]
```

#### 动作戏专用提示词模板

**模板1：单打独斗**
```
[Shot Type], [Camera Movement], [Character] in [Setting].
[Character] performs [specific action 1], then [reaction].
[Character] counters with [action 2], [physical impact description].
[Lighting] with [atmosphere]. [Color grade]. [Tech specs].
```

**模板2：多人打斗**
```
[Shot Type], [Camera Movement], [Number] combatants in [Setting].
[Key action 1]: [Character A] executes [move] against [Character B].
[Physical result]: [describe impact, reaction, positioning change].
[Key action 2]: [Character C] intervenes with [move].
[Camera movement follows the action thread]. [Lighting]. [Mood].
```

#### 动作戏Shot List规划

| 镜头类型 | 时长 | 用途 | 提示词要点 |
|---------|------|------|-----------|
| Establishing Shot | 3-5s | 建立空间关系 | wide angle, drone/crest shot |
| Wide Shot | 3-5s | 全景动作 | 展示全部角色位置 |
| Medium Shot | 2-4s | 动作主体 | 聚焦1-2个角色 |
| Close-up | 1-3s | 细节/表情 | 表情变化, 手部动作 |
| Insert Shot | 1-2s | 关键物品 | 武器、特效触发物 |
| POV Shot | 2-3s | 主观视角 | 角色第一人称 |
| Reaction Shot | 1-2s | 旁观反应 | 旁观者表情/动作 |

---

## 2. Lighting和Texture消除AI塑料感

### 2.1 AI塑料感的根本原因

AI生成的图像/视频容易出现"塑料感"（Plastic Look），主要原因：
1. **皮肤过于完美**：无毛孔、无纹理、无血色
2. **光线过于均匀**：缺乏体积感和散射
3. **高光过于锐利**：缺乏胶片级滚落（Roll-off）
4. **阴影过于硬朗**：缺乏软阴影过渡
5. **过度平滑**：消除了所有"不完美"细节

### 2.2 专业光线描述词详解

#### 体积光与散射类

| 描述词 | 中文含义 | 效果 |
|--------|---------|------|
| `Volumetric lighting` | 体积光 | 可见空气中的光束，产生尘埃感和空间感 |
| `Tyndall effect` | 丁达尔效应 | 空气中微粒使光线可见，光束分明 |
| `Atmospheric haze` | 大气雾霾 | 远景虚化，空气透视感 |
| `God rays` | 神光/耶稣光 | 从云层/树冠洒下的光束 |
| `Light scattering` | 光线散射 | 柔化边缘，增加体积感 |
| `Crepuscular rays` | 黄昏光束 | 低角度太阳穿透云层 |
| `Subsurface scattering` | 次表面散射 | 光线穿透半透明材质（皮肤、蜡烛） |
| `Caustic light patterns` | 焦散光纹 | 水面/玻璃折射的光纹 |

#### 软光与漫射类

| 描述词 | 中文含义 | 效果 |
|--------|---------|------|
| `Soft diffused lighting` | 软散射光 | 柔和过渡，无硬边缘阴影 |
| `Overcast sky diffusion` | 阴天散射光 | 极软均匀的光线 |
| `Bounced light` | 反弹光 | 墙面/地面反射的二次光源 |
| `Ambient occlusion` | 环境光遮蔽 | 角落/缝隙的细微阴影 |
| `Indirection fill light` | 间接补光 | 主光外的柔和填充 |
| `Multiple light bounce` | 多重光线弹射 | 复杂室内环境的自然光线 |

#### 胶片级高光类

| 描述词 | 中文含义 | 效果 |
|--------|---------|------|
| `Film-like highlight roll-off` | 胶片级高光滚落 | 高光逐渐柔和衰减，非数字化硬截断 |
| `Soft bloom on highlights` | 高光柔和泛光 | 亮部向外扩散的渐变光晕 |
| `Highlight bloom` | 高光溢出 | 亮部向周围扩散 |
| `Natural highlight detail` | 自然高光细节 | 高光区域保留纹理细节 |
| `Highlight compression` | 高光压缩 | 避免过曝，保留细节 |

### 2.3 材质纹理描述词详解

#### 皮肤质感类

| 描述词 | 中文含义 | 效果 |
|--------|---------|------|
| `Subsurface scattering` | 次表面散射 | 皮肤半透明感，光线穿透皮下 |
| `Visible micro-texture` | 可见微纹理 | 毛孔、细纹、凹凸感 |
| `Uneven pore density` | 不均匀毛孔密度 | T区毛孔粗，两颊细腻 |
| `Faint peach fuzz` | 细小绒毛 | 面部细微绒毛 |
| `Natural skin imperfections` | 自然皮肤瑕疵 | 轻微泛红、痣、雀斑 |
| `Asymmetrical features` | 不对称特征 | 左右脸略有差异 |
| `Capillary visibility` | 毛细血管可见 | 皮肤下隐约可见血管 |
| `Keratin shine distribution` | 角质光泽分布 | T区油光，U区干燥 |

#### 五官真实感类

| 描述词 | 中文含义 | 效果 |
|--------|---------|------|
| `Natural sclera tone` | 自然巩膜色（非纯白） | 眼白略带血丝或淡蓝 |
| `Asymmetrical catchlight` | 不对称眼神光 | 双眼眼神光位置/形状略有不同 |
| `Iris detail variation` | 虹膜细节变化 | 虹膜纹理、颜色层次 |
| `Nasal tip redness` | 鼻尖微红 | 皮肤血色的自然表现 |
| `Lip texture with micro-cracks` | 唇部微裂纹理 | 唇部干燥纹理 |
| `Ear helix detail` | 耳廓细节 | 耳朵软骨结构 |

#### 材质类

| 描述词 | 中文含义 | 效果 |
|--------|---------|------|
| `Micro-texture` | 微纹理 | 任何表面都应有细微凹凸 |
| `Material heterogeneity` | 材质不均匀性 | 同一材质不同区域有差异 |
| `Surface wear patterns` | 表面磨损痕迹 | 使用痕迹增加真实感 |
| `Imperfections` | 瑕疵 | 划痕、污渍、变色 |
| `Surface patina` | 表面包浆 | 岁月积累的质感 |

### 2.4 电影级布光体系在AI中的应用

#### 三点布光（Three-Point Lighting）

| 灯光 | 位置 | 提示词 | 效果 |
|------|------|--------|------|
| 主光（Key Light） | 45度角 | `45-degree key light, hard/soft depending on mood` | 主要阴影/高光 |
| 补光（Fill Light） | 对侧 | `soft fill light, bounced off ceiling` | 填充阴影 |
| 轮廓光（Rim Light） | 背后 | `edge rim light, hair light, separation light` | 主体分离背景 |

#### 经典光型在AI中的描述

| 光型 | 提示词 | 适用场景 |
|------|--------|---------|
| 伦勃朗光 | `Rembrandt lighting, triangle highlight under eye on shadowed side` | 单人特写，情绪戏 |
| 蝴蝶光 | `butterfly lighting, Paramount glamour light, nose shadow below nose` | 女性特写 |
| 环形光 | `loop lighting, soft shadow loop under nose` | 通用人像 |
| 书式光 | `book lighting, flat even illumination both sides` | 访谈/对称感 |
| 窗口光 | `soft window light, north-facing diffused, cinematic quality` | 自然光场景 |
| 黄金时刻 | `golden hour directional sunlight, long shadows, warm amber tones` | 夕阳光 |

### 2.5 消除塑料感完整提示词公式

```
[Camera/Lens] + [Skin Texture Keywords] + [Lighting Setup] + [Imperfection Keywords] + [Film/Color Grade]

示例（消除塑料感人像）：
shot on ARRI Alexa 65, Zeiss Master Prime lens
[皮肤] visible micro-texture, uneven pore density, subsurface scattering,
natural skin imperfections, faint peach fuzz, capillary visibility
[光线] Rembrandt lighting from left, volumetric fog ambient,
soft bounced fill from right, edge rim light
[瑕疵] subtle surface patina, nasolabial fold detail
[调色] film-like highlight roll-off, teal-and-orange palette,
35mm cinema look, subtle film grain
```

---

## 3. 打斗戏的专业镜头语言指令

### 3.1 打斗戏常用镜头术语

#### 镜头运动类

| 术语 | 中文 | 说明 | 动作戏提示词 |
|------|------|------|-------------|
| `Dutch angle` | 荷兰角/倾斜角 | 镜头倾斜，传达不安/紧张 | `Dutch angle during combat, ground appears tilted` |
| `Whip pan` | 快速摇摄 | 极快横向移动，甩镜头 | `whip pan from fighter to opponent, motion blur trail` |
| `Swish pan` | 快速甩镜 | 同whip pan，切换用 | `swish pan transition, fast cut` |
| `Crash zoom` | 急推 | 快速推进镜头 | `crash zoom into face during revelation` |
| `Pull focus / Rack focus` | 移焦 | 焦点在不同主体间切换 | `rack focus from foreground fist to background scream` |
| `Dolly zoom` | 推拉变焦 | 主体不变，背景透视变化 | `dolly zoom during fight climax` |
| `Crane up/down` | 摇臂升降 | 大范围空间展示 | `crane up from ground-level fight to rooftop reveal` |
| `Arc shot` | 弧形拍摄 | 环绕主体移动 | `arc shot around two fighters exchanging blows` |
| `Tracking shot` | 跟踪拍摄 | 跟随主体移动 | `Steadicam tracking shot following the lead fighter` |
| `Pedestal shot` | 升降台 shot | 上下移动 | `pedestal up from feet to face during defeat` |

#### 镜头角度类

| 术语 | 中文 | 说明 | 动作戏提示词 |
|------|------|------|-------------|
| `Low angle` | 低角度仰拍 | 使被拍物显得强大 | `low angle on victorious fighter, looking up` |
| `High angle` | 高角度俯拍 | 使被拍物显得弱势 | `high angle on fallen opponent, vulnerability` |
| `Bird's eye view` | 鸟瞰角 | 顶视，全局观 | `bird's eye during group fight, tactical overview` |
| `Cowl's eye view` | 牛眼角 | 略微俯视 | `medium angle, slight downward for grounded feel` |
| `Over-the-shoulder (OTS)` | 过肩镜头 | 主观镜头 | `over-the-shoulder during sword clash` |
| `Point-of-view (POV)` | 主观视角 | 第一人称 | `POV of punch connecting with jaw` |
| `Insert shot` | 插入镜头 | 细节特写 | `insert shot of blade embedding in shield` |
| `Cutaway` | 切离镜头 | 切换注意力 | `cutaway to screaming bystander` |

#### 快节奏剪辑术语

| 术语 | 中文 | 说明 | 动作戏提示词 |
|------|------|------|-------------|
| `Cross-cutting` | 交叉剪辑 | 多线并行叙事 | `cross-cut between two fighters in different locations` |
| `Jump cut` | 跳切 | 打破连续性 | `jump cut during combo to show speed` |
| `Match cut` | 匹配剪辑 | 形状/动作呼应 | `match cut from fist to incoming vehicle` |
| `Smash cut` | 冲击剪辑 | 突然场景切换 | `smash cut from impact to black` |
| `Montage` | 蒙太奇 | 快速连续镜头 | `training montage, series of strikes` |
| `Slow motion` | 慢动作 | 延展关键时刻 | `slow motion on killing blow, blood droplet detail` |

### 3.2 动作捕捉与镜头语言结合

#### 动作戏镜头序列模板

```
[起幅 - Establishing]
Wide establishing shot, all combatants in position.
Camera: aerial drone shot slowly descending.

[第一波攻击 - Wave 1]
Lead fighter charges from left, camera tracks.
Shot: medium tracking shot, handheld for impact shake.
Action: spinning staff strike, opponent guards.

[特写插入 - Impact Insert]
Insert: fist connects with jaw, sweat flies.
Shot: close-up, crash zoom on reaction.

[第二波攻击 - Wave 2]
Opponent retaliates, camera whip pans to follow.
Shot: OTS over shoulder during sword clash.
Action: blade grinds against blade, sparks.

[高潮 - Climax]
Both fighters leap, mid-air exchange.
Shot: bird's eye view, slow motion.
Action: simultaneous strikes, dust explosion on landing.

[收尾 - Resolution]
Loser falls, camera pedestals up from ground.
Shot: low angle on winner, high angle on fallen.
```

### 3.3 快节奏剪辑的镜头语言

#### 节奏控制公式

| 段落 | 镜头数 | 平均时长 | 镜头类型 |
|------|--------|---------|---------|
| 开场建立 | 2-3 | 4-6s | 宽广稳定 |
| 试探交锋 | 4-6 | 2-3s | 中景交替 |
| 激烈交火 | 8-12 | 0.5-2s | 短切特写 |
| 高潮 | 2-4 | 2-4s | 慢动作特写 |
| 结局 | 2-3 | 3-5s | 拉远稳定 |

```
快节奏剪辑提示词（在提示词中加入节奏指令）：
"Rapid cross-cutting between close-up impacts and wide tracking shots,
1-2 second cuts, heartbeat rhythm, handheld during exchanges,
slow motion on climactic blow, final cut to wide establishing."
```

### 3.4 动作戏运镜技巧详解

#### 手持（Handheld）

| 应用 | 提示词 | 效果 |
|------|--------|------|
| 贴身搏斗 | `handheld close combat, camera shakes on every impact` | 临场感、紧迫感 |
| 追逐戏 | `running handheld, breathing rhythm visible, stride bounce` | 速度感、疲惫感 |
| 主观打斗 | `POV handheld, attacker swings at camera` | 沉浸感 |

#### 斯坦尼康（Steadicam）

| 应用 | 提示词 | 效果 |
|------|--------|------|
| 跟踪追击 | `Steadicam tracking shot, smooth glide following fighter` | 流畅、优雅 |
| 穿越人群 | `Steadicam push through crowd, seamless transition` | 空间穿越感 |
| 情绪收尾 | `Steadicam slow pull-back during emotional beat` | 情绪释放 |

#### 摇臂（Crane/Jib）

| 应用 | 提示词 | 效果 |
|------|--------|------|
| 场景建立 | `crane up from fighting figures to burning building` | 宏观视野 |
| 动作过渡 | `crane down from sky to street-level combat` | 戏剧化入场 |
| 史诗结尾 | `slow crane out to reveal full battlefield` | 史诗感 |

#### 特殊效果

| 效果 | 提示词 | 适用场景 |
|------|--------|---------|
| 眩晕效果 | `dolly zoom during face-off, perspective distortion` | 对峙时刻 |
| 时间膨胀 | `slow motion 120fps during killing blow` | 高潮瞬间 |
| 空间扭曲 | `Dutch angle rotation during character knockback` | 打击感强化 |
| 速度线 | `motion blur speed lines during dash attack` | 速度感 |

---

## 4. 手持拍摄进阶技巧

### 4.1 手持拍摄在动作戏中的应用

手持摄影（Handheld Camera）在动作戏中能增强临场感、真实感和紧迫感。

#### 手持vs稳定器选择指南

| 场景 | 推荐 | 手持提示词 | 稳定器提示词 |
|------|------|-----------|-------------|
| 贴身搏斗 | 手持 | `handheld close combat, natural shake, breath rhythm` | `Steadicam smooth glide` |
| 追逐跑酷 | 手持 | `running handheld, stride bounce, breathing visible` | `Steadicam tracking runner` |
| 严肃决斗 | 稳定器 | `shot on tripod` | `Steadicam locked shot` |
| 主观视角 | 手持 | `POV handheld, attacker swings` | `gimbal smooth` |
| 情绪对话 | 稳定器 | N/A | `Steadicam emotional scene` |
| 混乱战场 | 手持 | `handheld chaos, multiple combatants, shake` | N/A |
| 跟踪监视 | 稳定器 | N/A | `Steadicam surveillance mode` |

### 4.2 "动态手持移动"等描述词的具体用法

#### 手持描述词层级

| 层级 | 描述词 | 强度 | 适用场景 |
|------|--------|------|---------|
| 轻微手持 | `slight handheld shake` | 微弱 | 日常场景，增加生气 |
| 标准手持 | `handheld camera, natural movement` | 中等 | 纪录片风格 |
| 动态手持 | `dynamic handheld movement with natural micro-jitters` | 中强 | 动作场景 |
| 激烈手持 | `aggressive handheld, heavy shake during impacts` | 强 | 搏斗、爆炸 |
| 极限手持 | `extreme handheld, disorienting shake, breathlessness` | 极强 | 追逐、坠落 |

#### 具体手持描述词示例

```
标准动作戏手持：
"Dynamic handheld camera, natural micro-jitters, breathing rhythm visible,
stride bounce during running, camera shake on every physical impact,
organic unsteadiness, documentary realism."

激烈搏斗手持：
"Aggressive handheld, heavy camera shake with each punch landed,
breathing急促，body impact transmitted through camera,
jump cuts to emphasize violence, shake intensity matches action."

追踪场景手持：
"Running handheld, vertical bounce with each footfall,
horizontal sway during turns, wind blur at edges,
sudden stop - camera overshoots then settles."
```

### 4.3 如何通过手持感增强真实感

#### 呼吸感（Breath Feel）

```
提示词加入：
"visible breath condensation in cold air"
"chest heaving with exertion, camera tremor matches"
"breathing rhythm visible in frame movement"
```

#### 物理反馈感（Physical Feedback）

```
提示词加入：
"camera shake on fist impact, energy transmitted through frame"
"recoil bounce after explosion, camera momentarily disoriented"
"contact shake when weapons clash, metallic vibration in frame"
```

#### 重量感（Weight Feel）

```
提示词加入：
"camera struggles against imaginary wind resistance during fast movement"
"heavy settling bounce when character lands after jump"
"momentum drag when character suddenly changes direction"
```

### 4.4 手持vs稳定器的混合使用

#### 动作戏中的混合策略

| 段落 | 设备 | 提示词 | 目的 |
|------|------|--------|------|
| 开场全景 | 稳定器 | `Steadicam smooth wide establishing shot` | 冷静建立 |
| 遭遇战 | 手持 | `suddenly handheld when fight breaks out, shake` | 打破平静 |
| 激烈交火 | 手持 | `aggressive handheld, close rapid cuts` | 紧张感 |
| 短暂停 | 稳定器 | `Steadicam brief lull, camera floats` | 喘息时刻 |
| 再次爆发 | 手持 | `return to handheld, even more aggressive` | 情绪升级 |
| 结局 | 稳定器 | `Steadicam slow pullback, finality` | 情绪收尾 |

### 4.5 手持摄影AI生成技巧

#### 手持与景别组合

| 景别 | 手持效果 | 提示词 |
|------|---------|--------|
| 特写 | 轻微抖动明显 | `close-up handheld, slight shake, every micro-movement visible` |
| 中景 | 标准抖动 | `medium shot handheld, balanced movement` |
| 全景 | 抖动不易察觉 | `wide shot handheld, environmental, subtle shake` |
| POV | 极强抖动 | `first-person POV handheld, disorienting shake, full immersion` |

---

## 5. AI视频质量审核体系

### 5.1 人物一致性保持方法

#### 角色描述词固定化检查表

每个角色生成前必须确认以下信息已完成：

| 检查项 | 标准 | 未通过 |
|--------|------|--------|
| 面部特征描述 | 至少5项具体描述（脸型、眼型、鼻型、唇形、肤色） | 重新定义 |
| 体型特征描述 | 身高、体型、独特标记 | 重新定义 |
| 服装描述 | 颜色、材质、关键配饰 | 重新定义 |
| 参考图生成 | 4-view定妆照完成 | 先生成参考图 |
| 负面约束词 | 已设定禁止出现的特征 | 补充Negative Prompt |

#### 多镜头一致性审核

| 镜头序列 | 面部一致性 | 服装一致性 | 体型一致性 | 通过/不通过 |
|---------|-----------|-----------|-----------|------------|
| Shot 1 | 0.9 | 0.95 | 1.0 | Pass |
| Shot 2 | 0.85 | 0.9 | 1.0 | Conditional |
| Shot 3 | 0.7 | 0.85 | 1.0 | Fail - 重新生成 |

评分标准：>0.85为Pass，0.7-0.85为Conditional需修复，<0.7为Fail

### 5.2 场景一致性审核标准

| 维度 | 必须锁定项 | 允许变动项 |
|------|-----------|-----------|
| 空间 | 室内/室外、场景类型 | 具体摆设 |
| 光线 | 主色调（暖/冷/自然）、时间段 | 天气细节 |
| 色调 | 整体色系 | 局部色彩 |
| 时间 | 白天/夜晚/黎明/黄昏 | 具体时间点 |
| 天气 | 晴/阴/雨/雪 | 湿度细节 |

#### 场景一致性评分

| 评分 | 定义 | 行动 |
|------|------|------|
| A级 | 完全一致，无可察觉差异 | 直接使用 |
| B级 | 细微差异，专业人士可察觉 | 微调后使用 |
| C级 | 明显差异，需要修复 | 重新生成 |
| D级 | 完全不一致 | 废弃不用 |

### 5.3 动作连贯性检查要点

#### 物理逻辑检查

| 检查项 | 问题描述 | 修复方法 |
|--------|---------|---------|
| 关节角度 | 手脚弯折超过生理极限 | 调整动作描述词 |
| 碰撞反馈 | 打击无物理响应 | 加入反应描述词 |
| 重量感 | 物体漂浮/穿透 | 加入物理约束词 |
| 连续动作 | 招式之间无过渡 | 加入动作连接词 |
| 武器交互 | 武器穿过身体 | 明确接触点描述 |

#### 动作戏连贯性评分

```
连贯性评分 = 物理合理性(30%) + 动作连续性(25%) + 视线轴线(20%) + 时序合理性(15%) + 空间位置(10%)

评分标准：
A (90-100): 完美连贯
B (75-89): 基本连贯，轻微问题
C (60-74): 明显问题，需要修复
D (<60): 严重问题，重新生成
```

### 5.4 剧情符合度评估

| 检查项 | 说明 | 权重 |
|--------|------|------|
| 角色行为 | 角色行为是否符合人设/性格 | 20% |
| 情绪表达 | 情绪戏是否传达正确情感 | 20% |
| 剧情推进 | 镜头是否有效推进剧情 | 20% |
| 对白/动作 | 对白或动作是否符合剧本 | 20% |
| 节律感 | 节奏是否符合预期情绪 | 20% |

### 5.5 表情/动作/运镜审核标准

#### 表情审核

| 检查项 | 合格标准 | 常见问题 |
|--------|---------|---------|
| 眼睛 | 虹膜细节、瞳孔反应、自然眨眼 | 死鱼眼、白眼 |
| 嘴型 | 嘴唇纹理、自然开合 | 塑料微笑、嘴型僵硬 |
| 眉毛 | 自然运动、表情协调 | 眉毛不动、过度夸张 |
| 微表情 | 细微情绪变化 | 表情跳变 |

#### 动作审核

| 检查项 | 合格标准 | 常见问题 |
|--------|---------|---------|
| 姿势 | 符合人体工学 | 关节扭曲、身体折叠 |
| 速度 | 符合物理预期 | 动作过快/过慢 |
| 力度 | 力度传递可见 | 打击感缺失 |
| 随动 | 头发/衣服/配件随动 | 静止不动 |

#### 运镜审核

| 检查项 | 合格标准 | 常见问题 |
|--------|---------|---------|
| 焦距 | 符合景别预期 | 焦距跳变 |
| 运动 | 运动平滑自然 | 抖动异常/运动不连贯 |
| 稳定性 | 符合手持/稳定器描述 | 稳定器漂移 |
| 角度 | 角度符合轴线规则 | 越轴 |

### 5.6 AI视频常见失败模式及修复

| 失败类型 | 表现 | 修复策略 |
|---------|------|---------|
| 面部崩溃（Face Collapse） | 面部模糊/扭曲/多张脸叠加 | 使用参考图，增加面部描述词 |
| 人物漂移（Character Drift） | 多镜头中角色外貌变化 | 固定描述词，使用参考图 |
| 运动模糊过度（Excessive Motion Blur） | 动作细节丢失 | 减少动态模糊描述词 |
| 关节失效（Joint Failure） | 手指/脚趾消失或多余 | 明确手部描述，Negative Prompt |
| 物理穿模（Physics Penetration） | 物体/武器穿过身体 | 明确接触点，加入物理约束 |
| 光线不一致（Lighting Inconsistency） | 同一场景光线突变 | 锁定光线描述词 |
| 材质异常（Material Anomaly） | 皮肤/物体出现塑料/金属质感 | 增加纹理描述词 |

#### Negative Prompt 常用词（动作戏专用）

```
deformed hands, extra fingers, missing fingers,
blurry anatomy, incorrect anatomy, disfigured,
mutation, mutated, ugly, disgusting,
artificial structures, plastic skin, mannequin skin,
excessive smoothing, over-processed,
dead eyes, wrong eye shape, asymmetric eyes,
cartoonish, anime style, oversaturated,
motion blur too heavy, distortion,
weapon clipping through body, physics violation
```

---

## 附录：动作戏提示词模板库

### 模板A：武侠动作戏

```
[Wide establishing shot] Ancient Chinese courtyard at dusk.
Bamboo shadows cast by paper lanterns, golden hour fading.
[Camera movement] Steadicam push-in as [Character A] enters.
[Combat] [Character A] draws sword with fluid motion,
blade catches lantern light. [Character B] attacks from right,
camera whip pans to follow strike. [Action detail]
Steel clashes, sparks shower, camera shake on impact.
[Close-up] Sweat droplets fly in slow motion from foreheads.
[Rim lighting] Fighters silhouetted against burning sunset.
[Cut] Simultaneous thrust, [Reaction] both stagger back.
[Camera] Dutch angle tilts as loser falls to knees.
[Final] Steadicam slow pull-back, winner sheathes sword.
Shot on ARRI Alexa 65, anamorphic lens, Kodak Vision3 500T,
volumetric fog, cinematic color grading, 4K quality.
```

### 模板B：现代搏击

```
[Medium shot] Underground fight club, neon pink and blue lights.
[Character A] circles right, shadows dancing on concrete walls.
[Camera] Handheld tracking, breathing rhythm visible.
[Combat] Right hook connects - camera shake, sweat flies.
[Crowd reaction] Cutaway to screaming faces in slow motion.
[POV] Insert shot from fighter's perspective as opponent falls.
[High angle] on loser, vulnerability, camera pedestals down.
[Close-up] Winner raises bloodied fist, camera low angle upward.
[Lighting] Practical neon flickering, volumetric smoke,
volumetric lighting cutting through haze.
[Style] Teal and orange, bleach bypass, film grain.
Shot on RED Komodo, 35mm lens, 24fps cinematic.
```

### 模板C：科幻战斗

```
[Aerial establishing] Futuristic cityscape at night, rain.
[Camera] Drone shot descending toward rooftop battle.
[Combatants] [Character A] in powered armor, [Character B] in tactical gear.
[Combat] Energy sword ignites, camera rack focus to blade.
[Action] Swinging arc, camera arc shot around fighters.
[Impact] Explosion bloom, camera aggressive handheld shake.
[Insert] Bullet-time slow motion, droplets frozen in air.
[POV] [Character A]'s helmet visor reflection of battle.
[Cut] Jump cut between multiple simultaneous strikes.
[Environment] Volumetric fog, neon city glow, atmospheric haze.
[Detail] Rain droplets on armor, micro-texture visible.
[Style] Cyberpunk, blue and orange rim lighting,
anamorphic lens flares, cinematic color palette.
Shot on ARRI Alexa, anamorphic, 8K, photorealistic.
```

---

## 参考来源

- Midjourney Cinematography Guide: https://dangergirlx.com/cinematography-and-film-cameras-in-midjourney/
- VO3 AI Character Consistency Guide: https://www.vo3ai.com/blog/how-to-create-consistent-ai-video-characters
- Seedance 2.0 Prompt Guide: https://seedance2.so/blog/ai-video-camera-movement-prompt-guide
- Venice.ai AI Video Prompt Engineering: https://cdn.venice.ai/blog/the-complete-guide-to-ai-video-prompt-engineering
- Genra AI Why AI Videos Look Fake: https://genra.ai/blog/why-ai-videos-look-fake-how-to-fix
- StudioBinder Action Scene Storyboarding: https://www.studiobinder.com/blog/how-to-shoot-dynamic-fight-scenes/
- Inception Rotating Hallway Fight Breakdown: https://streamintel.io/inception-rotating-hallway-fight-scene-breakdown/
- Adorama Handheld Camera Techniques: https://www.adorama.com/alc/5-handheld-moves-for-cinematic-storytelling/
- VidHex Plastic Skin Fix: https://www.vidhex.ai/blog/make-ai-skin-look-real/
- Claid.ai AI Skin Texture: https://claid.ai/blog/article/fix-ai-skin-texture
- Wolfcrow Steadicam vs Handheld: https://wolfcrow.com/steadicam-gimbal-handheld-the-mistakes-you-want-to-avoid-now/
- NotebookLM Knowledge Base: https://notebooklm.google.com/notebook/f56bd450-598b-4a97-938c-ae8b9c77ab2e

---

*本指南持续更新，结合实际AI生成平台特性（Seedance 2.0、Kling 2.5、Veo 3、Sora 2等）调整提示词策略。*
