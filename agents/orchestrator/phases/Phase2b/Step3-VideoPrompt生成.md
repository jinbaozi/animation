# Step 3: 生成VideoPrompt

> 执行角色：AI美术技术总监
> 所属阶段：Phase 2b
> 版本：v2.0
> **v2.0更新**：同时生成中英文、格式A（带基本信息表）、基于增强分镜执行表逐shot生成、覆盖率≥80%要求

---

## 1. 生成流程

### 1.1 逐Shot生成（Simultaneous）

对shot逐个生成，**中英文同时生成**：

```
For each shot (001-N):
    1. 从增强分镜执行表提取：
       - 镜头编号、场景编号、场景类型
       - 运镜方式、镜头语言
       - 主要人物、次要人物
       - 动作/台词、情绪
       - 光线、色调

    2. 生成基本信息表（中文版 + 英文版）

    3. 同时生成：
       - 中文VideoPrompt（5段式）
       - 英文VideoPrompt（5段式）

    4. 内容一致性检查
```

### 1.2 覆盖率要求（v2.0新增·MANDATORY）

#### 覆盖率标准

| 指标 | 要求 | 说明 |
|-------|------|------|
| 核心镜头覆盖率 | ≥80% | 增强分镜镜头数×80% |

#### 镜头优先级排序

生成VideoPrompt时，按以下优先级筛选：

| 优先级 | 镜头类型 | 理由 |
|-------|---------|------|
| P0 | 核心叙事镜头 | 推动剧情发展的关键镜头 |
| P0 | 情绪高潮镜头 | 情感爆发/转折点 |
| P1 | 奇幻视觉奇观镜头 | 特效展示，需要详细描述 |
| P1 | 动作戏关键帧 | 战斗高潮 |
| P2 | 过渡镜头 | 可用标准化模板 |
| P3 | 远景空镜 | 场景交代，可用标准化描述 |

#### 覆盖率计算

```
actual_shots = len(增强分镜执行表)
target_coverage = 0.8
minimum_required = ceil(actual_shots * target_coverage)

if len(generated_prompts) < minimum_required:
    # 必须补充缺失镜头
    raise "VideoPrompt覆盖率不足，当前{len(generated_prompts)}/{actual_shots}，需至少{minimum_required}个"
```

### 1.3 版本标注要求（v2.0新增）

所有输出文件**必须**在头部标注版本信息：

```markdown
> 版本：v1.x
> 覆盖率：{实际数}/{总数} ({百分比})
> 版本联动：v1.x新增{变更内容}
``` |

---

## 2. 输出格式（格式A）

### 2.1 中文版结构

```markdown
## 镜头{编号}：{场景描述}

### 基本信息
| 字段 | 内容 |
|------|------|
| 镜头编号 | {001} |
| 场景 | S{01} |
| 场景类型 | {日常氛围治愈系} |
| 时长 | 15秒 |
| 运镜方式 | {中景→近景} |

---

### 中文VideoPrompt

**0-3s (开场)**:
[场景引入，定场镜头]
{中文内容}

**3-6s (发展)**:
[人物动作，场景推进]
{中文内容}

**6-9s (高潮)**:
[关键情感/动作时刻]
{中文内容}

**9-12s (回落)**:
[情绪/动作延续]
{中文内容}

**12-15s (落幅)**:
[结尾镜头，情绪落点]
{中文内容}
```

### 2.2 英文版结构

```markdown
## Shot {编号}: {Scene Description}

### Basic Info
| Field | Content |
|-------|---------|
| Shot Number | {001} |
| Scene | S{01} |
| Scene Type | {Daily/Healing} |
| Duration | 15s |
| Camera | {Medium→Close-up} |

---

### English VideoPrompt

**0-3s (Opening)**:
[Scene introduction, establishing shot]
{English content}

**3-6s (Development)**:
[Character action, scene progression]
{English content}

**6-9s (Climax)**:
[Key emotional/action moment]
{English content}

**9-12s (Resolution)**:
[Emotional/action continuation]
{English content}

**12-15s (Closing)**:
[Closing shot, emotional landing]
{English content}
```

---

## 3. 内容生成规则

### 3.1 主体描述
- 从人物四视图Prompt包提取角色外貌描述
- 包含：身形、脸型、肤色、发型、服装
- 特殊标记（胡须/木杖/白发/独眼等）不得遗漏

### 3.2 场景描述
- 从场景资产卡提取环境细节
- 包含：建筑特征、光线、氛围
- 色调必须与增强分镜执行表一致

### 3.3 动作描述
- 基于增强分镜执行表的"动作/台词"字段
- 扩展为具体视觉表现
- 使用动作动词（拉、推、注视、转身等）

### 3.4 情绪描述
- 基于增强分镜执行表的"情绪"字段
- 通过面部表情、身体语言体现
- 与场景氛围协调

---

## 4. 质量检查

生成完成后，AI美术技术总监必须验证：

- [ ] Shot数量 = 338（与增强分镜执行表一致）
- [ ] 中文版每个shot有5个时间段（0-3s/3-6s/6-9s/9-12s/12-15s）
- [ ] 英文版每个shot有5个时间段
- [ ] 中英文基本信息表字段一致
- [ ] 中英文内容对应（同一shot的中英文描述同一场景）
- [ ] 无禁用词（影视质感、电影级、古风写实等）
- [ ] 运镜术语专业且正确
- [ ] 起幅→落幅连续性在相邻shot间体现
- [ ] 内容与增强分镜执行表逐行对应（不得模板重复）

---

## 5. 输出文件

生成完成后，输出到：

```
output/{项目名}/05-Phase2b-Prompt/
├── VideoPrompt包-中文版.md    # 中文提示词（338个shot）
└── VideoPrompt包-英文版.md    # English prompts（338个shot）
```

**注意**：
- 中英文分开，不混在同一文件
- 每个文件包含全部338个shot
- 文件头包含元数据（项目名、版本、日期、目标平台）
