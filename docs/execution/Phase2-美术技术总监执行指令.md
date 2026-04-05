# Phase 2 - 美术技术总监执行指令

> 版本：v1.0.0
> 创建日期：2026-04-04
> 执行角色：AI美术技术总监
> 细分：Phase 2a（人物+场景）→ Phase 2b（VideoPrompt）

---

## 1. 执行概述

| Phase | 执行角色 | 输入 | 输出 | 时长 |
|-------|---------|------|------|------|
| Phase 2a | AI美术技术总监 | 增强分镜执行表 + 序列衔接表 | 人物四视图Prompt包 + 场景资产卡 | 约60分钟 |
| Phase 2b | AI美术技术总监 | Phase 2a输出 | VideoPrompt包 + 试生成素材 | 约60分钟 |

---

## 2. Phase 2a - 人物四视图 + 场景资产

### 2.1 执行步骤

#### Step 1: 人物分析

1. 接收 `人物清单.md`
2. 识别需要生成四视图的角色
3. 为每个角色建立视觉档案

#### Step 2: 生成人物四视图Prompt

**四视图格式（MANDATORY）**：

| 视图 | 角度 | 描述 |
|------|------|------|
| 正面全身 | 0度 | 正面站立，双手自然下垂 |
| 侧面全身 | 90度 | 侧面站立，展示轮廓 |
| 背面全身 | 180度 | 背面站立，展示背部设计 |
| 面部特写 | 面部 | 高清面部细节，眼睛、嘴唇特写 |

**Prompt生成规则**：

```markdown
# 人物四视图Prompt包

## 角色：白浅

### 正面全身
Prompt: 动画风格，8K高清，白浅，正面全身照，纯白背景，
鹅蛋脸，病态苍白肤色，杏核眼，眼神忧郁，长发及腰，
黑色长发自然垂落，身穿素雅白色长裙，纤细单薄身形，
服装细节：腰间淡蓝色丝带，简单发簪，站姿优雅，
无阴影，纯白背景，高质量动画

### 侧面全身
Prompt: 动画风格，8K高清，白浅，侧面全身照，纯白背景，
鹅蛋脸侧面轮廓，病态苍白肤色，长发及腰侧面效果，
素雅白色长裙侧身效果，腰间淡蓝色丝带，
纤细身形侧面，站姿优雅，纯白背景，高质量动画

### 背面全身
Prompt: 动画风格，8K高清，白浅，背面全身照，纯白背景，
黑色长发垂落背影，素雅白色长裙背面，腰间淡蓝色丝带背面效果，
纤细身形背影，无阴影，纯白背景，高质量动画

### 面部特写
Prompt: 动画风格，8K高清，白浅，面部特写，纯白背景，
鹅蛋脸，病态苍白肤色，杏核眼，眼神忧郁，
高清面部细节，精致五官，透明感皮肤，长发垂落两侧，
无阴影，纯白背景，高质量动画
```

#### Step 3: 生成场景资产卡

```markdown
# 场景资产卡

## 场景：天宫大殿

### 场景描述
室内场景，天宫大殿，金碧辉煌，雕梁画栋，龙柱耸立，
仙气缭绕，广阔空间，庄重氛围

### 视觉Prompt
Prompt: 动画风格，8K高清，天宫大殿内景，金碧辉煌，
雕梁画栋细节，龙柱耸立两旁，仙气缭绕，广阔空间，
日光从穹顶洒落，庄重氛围，中国古风仙侠风格，
高品质动画背景，详细建筑细节
```

### 2.2 质量标准

**人物四视图检查**：
- [ ] 每个角色有4个视角
- [ ] 全部纯白背景
- [ ] 无水印、无文字
- [ ] 风格一致（符合项目风格）
- [ ] 无禁用词

**场景资产卡检查**：
- [ ] 场景描述具体
- [ ] 包含环境、光线、氛围
- [ ] 可转化为视觉表达

---

## 3. Phase 2b - VideoPrompt生成

### 3.1 执行步骤

#### Step 1: 接收与准备

1. 接收 Phase 2a 输出
2. 接收 `增强分镜执行表.md`
3. 阅读 `rules/审美偏好.md`
4. 阅读 `rules/风格一致性.md`
5. 阅读 `rules/双轨生成.md`
6. 阅读 `rules/视频格式.md`

#### Step 2: 时间分段

VideoPrompt 按5秒一段：

| 时间段 | 内容 |
|--------|------|
| 0-3s | 开场/引入 |
| 3-6s | 发展/动作 |
| 6-9s | 高潮/关键 |
| 9-12s | 回落/过渡 |
| 12-15s | 结尾/收束 |

#### Step 3: 生成VideoPrompt

**格式规范**：

```markdown
# VideoPrompt包

> 项目：{项目名称}
> 版本：v1.0
> 生成日期：{YYYY-MM-DD}
> 目标平台：{平台}
> 目标时长：{秒数}秒

---

## 序列 001：天宫大殿 - 夜华表白

### 基本信息

| 字段 | 内容 |
|------|------|
| 镜头编号 | 001 |
| 场景 | S01 |
| 场景类型 | 对话场景 |
| 时长 | 15秒 |
| 运镜方式 | 中景→特写 |

### 英文VideoPrompt

**0-3s (开场)**:
[Scene introduction, establishing shot]
Medium shot, elegant palace interior, golden pillars, soft natural lighting,
Jade and gold architecture details, celestial atmosphere,
Chinese xianxia style, anime aesthetic, 8K, high quality

**3-6s (夜华走近)**:
[Character approach, romantic tension]
Camera dollies in slowly, Ye Hua walking forward,
Black and gold robes flowing, elegant movement,
Romantic atmosphere, soft lighting, Chinese xianxia style

**6-9s (特写表白)**:
[Key emotional moment, close-up]
Extreme close-up on Ye Hua's face, deep emotional eyes,
Romantic tension, soft focus background,
Chinese xianxia style, anime aesthetic

**9-12s (白浅反应)**:
[Bai Qian's reaction, emotional response]
Over the shoulder shot, Bai Qian's subtle smile,
Romantic atmosphere, petal falling slowly,
Chinese xianxia style, anime aesthetic

**12-15s (落幅)**:
[Closing shot, romantic mood]
Wide shot, couple together, soft lighting,
Romantic atmosphere, petals falling, Chinese xianxia style

### 中文VideoPrompt

**0-3s (开场)**:
[场景引入，定场镜头]
中景，典雅宫殿内景，金色立柱，柔和自然光，
玉雕与金色建筑细节，仙气氤氲，
中国古风仙侠风格，动画美学，8K，高质量

**3-6s (夜华走近)**:
[人物走近，浪漫氛围]
镜头缓慢推进，夜华向前行走，
黑金长袍飘逸，动作优雅，
浪漫氛围，柔和光线，中国古风仙侠风格

**6-9s (特写表白)**:
[关键情感时刻，特写]
夜华面部极近特写，深情眼神，
浪漫氛围，背景虚化，
中国古风仙侠风格，动画美学

**9-12s (白浅反应)**:
[白浅反应，情绪回应]
过肩镜头，白浅微微一笑，
浪漫氛围，花瓣缓缓飘落，
中国古风仙侠风格，动画美学

**12-15s (落幅)**:
[结尾镜头，浪漫氛围]
全景，二人并肩，柔和光线，
浪漫氛围，花瓣飘落，中国古风仙侠风格
```

### 3.2 双轨生成规则

```markdown
## 双轨Prompt生成规范

### 原则
1. 中文和英文Prompt同时生成
2. 内容必须一致（同一镜头）
3. 英文Prompt面向国际化模型优化
4. 中文Prompt面向国内模型优化

### 格式
- 英文Prompt：[描述性内容]
- 中文Prompt：[描述性内容]
- 时间标签：0-3s | 3-6s | 6-9s | 9-12s | 12-15s
```

### 3.3 质量标准

**VideoPrompt检查**：
- [ ] 时间分段正确（每段3秒）
- [ ] 中英双轨完整
- [ ] 无禁用词
- [ ] 运镜术语专业
- [ ] 场景类型匹配

---

## 4. 输出文件清单

| Phase | 文件 | 格式 | 必填 |
|-------|------|------|------|
| 2a | 人物四视图Prompt包.md | Markdown | 是 |
| 2a | 场景资产卡.md | Markdown表格 | 是 |
| 2b | VideoPrompt包.md | Markdown | 是 |

---

## 5. 工具适配参考

**Seedance 2.0**：
- `templates/knowledge/Seedance2导演级运镜库.md`
- `templates/knowledge/Seedance2提示词与运镜完全指南.md`

---

## 6. 返工机制

- **返工触发**：Prompt质量不达标、风格不一致
- **常见返工原因**：
  - 人物四视图风格不统一
  - VideoPrompt描述不够具体
  - 违反禁用词规则
- **返工上限**：3次

---

## 7. 禁用词检查

生成Prompt前，必须检查：
- [ ] `rules/风格一致性.md` 中的禁用词
- [ ] 无"影视质感"、"电影级"等描述
- [ ] 无"古风写实"等不匹配描述

---

## 版本历史

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0.0 | 2026-04-04 | 初始版本 |
