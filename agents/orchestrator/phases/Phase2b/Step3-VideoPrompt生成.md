# Step 3: 生成VideoPrompt

> 执行角色：AI美术技术总监
> 所属阶段：Phase 2b
> 版本：v3.0
> **v3.0更新**：先生成 Prompt Export IR，再导出中文/英文 VideoPrompt；核心交付覆盖率默认 100%

---

## 1. 生成流程

### 1.1 逐Shot生成（Simultaneous）

对 Shot IR 逐个生成 `PromptExportIR.md`，再从同一 IR 导出中文/英文版本：

```
For each Shot IR unit:
    1. 合并 Shot IR 的镜头字段
    2. 合并 Visual Anchor IR 的人物、场景、道具和风格锚点
    3. 生成 Prompt Export IR 行
    4. 从 Prompt Export IR 导出：
       - VideoPrompt包-中文版.md
       - VideoPrompt包-英文版.md
       - ToolExport/{工具名}.md（按需）
    5. 校验导出内容与 Prompt Export IR 一致
```

### 1.2 覆盖率要求（MANDATORY）

#### 覆盖率标准

| 指标 | 要求 | 说明 |
|-------|------|------|
| Prompt Export IR 覆盖率 | 100% | 覆盖 Shot IR 全部镜头 |
| 核心交付 VideoPrompt 覆盖率 | 100% | 覆盖 Prompt Export IR 全部核心镜头 |

精简交付模式必须由用户明确确认，并在 `project-manifest.md` 中记录范围与未覆盖原因。

#### 镜头优先级排序（仅用于精简交付模式）

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
actual_shots = len(ShotIR)
minimum_required = actual_shots

if len(generated_prompts) < minimum_required:
    raise "VideoPrompt覆盖率不足，当前{len(generated_prompts)}/{actual_shots}，核心交付模式要求100%"
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

`格式A` 是中文审阅版和通用导出版的呈现格式，不是 Phase 2b 的唯一事实源。所有字段必须先写入 `PromptExportIR.md`。

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

- [ ] PromptExportIR 行数 = ShotIR 行数
- [ ] 中文/英文 VideoPrompt 数量 = PromptExportIR 核心导出数量
- [ ] 中文版每个shot有5个时间段（0-3s/3-6s/6-9s/9-12s/12-15s）
- [ ] 英文版每个shot有5个时间段
- [ ] 中英文基本信息表字段一致
- [ ] 中英文内容对应（同一shot的中英文描述同一场景）
- [ ] 无禁用词（影视质感、电影级、古风写实等）
- [ ] 运镜术语专业且正确
- [ ] 起幅→落幅连续性在相邻shot间体现
- [ ] 内容与增强分镜执行表逐行对应（不得模板重复）
- [ ] 人物描述与人物资产卡一致
- [ ] 场景描述与场景资产卡一致

---

## 5. 输出文件

生成完成后，输出到：

```
output/{项目名}/05-Phase2b-Prompt/
├── PromptExportIR.md
├── VideoPrompt包-中文版.md    # 中文提示词（shot数量来自 project-manifest.md）
├── VideoPrompt包-英文版.md    # English prompts
└── ToolExport/
```

**注意**：
- 中英文分开，不混在同一文件
- 每个文件包含 project manifest 定义的全部核心交付 shot
- 文件头包含元数据（项目名、版本、日期、目标平台）
