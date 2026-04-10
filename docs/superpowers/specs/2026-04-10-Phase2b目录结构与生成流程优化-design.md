# Phase 2b 目录结构与生成流程优化

> 版本：v1.0
> 日期：2026-04-10
> 状态：已批准

---

## 1. 背景

当前 Phase 2b 目录结构存在混乱：
- `05-Phase2b-视频提示词/` 和 `05-Phase2b-Prompt生成/` 两个目录并存
- 主输出（VideoPrompt包.md）内容为模板重复填充，338个shot内容相同，质量不合格
- 生成脚本混在output目录中

需要优化 Phase 2b 的目录结构和生成流程。

---

## 2. 目标

- 一个 Phase 2b 目录，中文/英文分开存放
- 生成时综合：增强分镜执行表、规则、技巧、示例、默会知识
- 同时生成中/英文版本（格式A，带基本信息表）
- 每个shot内容必须基于增强分镜执行表，不得模板重复

---

## 3. 目录结构

```
05-Phase2b-Prompt/
├── VideoPrompt包-中文版.md      # 中文提示词（338个shot）
├── VideoPrompt包-英文版.md      # English prompts (338 shots)
└── 生成日志.md                  # 生成过程记录（可选）
```

**说明：**
- 目录名 `05-Phase2b-Prompt` 与 `docs/output目录结构规范.md` 一致
- 中文/英文分开，不混在同一文件
- 生成脚本移至 `scripts/` 目录，不属于产出物

---

## 4. 输入材料

| 材料 | 用途 |
|------|------|
| `03-Phase1.5/增强分镜执行表.md` | 338个shot，逐行提取action/dialogue/scene/情绪/运镜 |
| `rules/风格一致性.md` | 风格锚点、禁用词清单 |
| `rules/双轨生成.md` | 中英双轨生成规范 |
| `rules/视频格式.md` | 时间分段规则（0-3s/3-6s/6-9s/9-12s/12-15s） |
| `rules/运镜知识.md` | 运镜术语规范 |
| `agents/orchestrator/Seedance2/Seedance2提示词技巧大全.md` | Seedance2专有技巧 |
| `templates/knowledge/13-好莱坞运镜库.md` | 运镜参考 |
| `.claude/skills/polanyi-tacit-knowledge/knowledge/` | 默会知识库（镜头语言、情绪节奏等） |
| `agents/orchestrator/phases/Phase2b/VideoPrompt模板.md` | 优秀示例 |

---

## 5. 生成流程

### 5.1 阅读输入（执行前）

AI美术技术总监必须阅读并理解以下材料：
- 增强分镜执行表（338个shot）
- 风格一致性规则（禁用词、风格锚点）
- 双轨生成规则
- 视频格式规范
- Seedance2技巧
- 默会知识（镜头语言、情绪节奏把控）
- VideoPrompt模板示例

### 5.2 逐Shot生成（Simultaneous）

对338个shot逐个生成，**中英文同时生成**：

```
For each shot (001-338):
    1. 从增强分镜执行表提取：
       - 镜头编号、场景编号、场景类型
       - 运镜方式、镜头语言、落幅/起幅
       - 主要人物、次要人物
       - 动作/台词、情绪、光线、色调

    2. 生成基本信息表（中文版 + 英文版）

    3. 同时生成中文VideoPrompt（5段式）
       同时生成英文VideoPrompt（5段式）

    4. 内容一致性检查：
       - 中英文基本信息表字段一致
       - 中文VideoPrompt内容 ≠ 英文VideoPrompt内容（中英描述方式不同）
       - 中英文动作/场景描述对应
```

### 5.3 时间分段

每个shot = 15秒，固定5段：

| 段 | 时间 | 标签（中文） | 标签（英文） |
|----|------|-------------|--------------|
| 1 | 0-3s | 开场 | Opening |
| 2 | 3-6s | 发展 | Development |
| 3 | 6-9s | 高潮 | Climax |
| 4 | 9-12s | 回落 | Resolution |
| 5 | 12-15s | 落幅 | Closing |

---

## 6. VideoPrompt格式（格式A）

### 6.1 中文版

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

### 6.2 英文版

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

## 7. 质量检查清单

生成完成后，AI美术技术总监必须验证：

- [ ] Shot数量 = 338（与增强分镜执行表一致）
- [ ] 中文版每个shot有5个时间段（0-3s/3-6s/6-9s/9-12s/12-15s）
- [ ] 英文版每个shot有5个时间段
- [ ] 中英文基本信息表字段一致
- [ ] 无禁用词（影视质感、电影级、古风写实等）
- [ ] 运镜术语专业且正确
- [ ] 起幅→落幅连续性在相邻shot间已体现
- [ ] 内容与增强分镜执行表逐行对应（不得模板重复）

---

## 8. 版本联动

Phase 2b 生成后，如果：
- 增强分镜执行表.md 更新 → Phase 2b 必须重新生成
- 人物四视图Prompt包.md 更新 → Phase 2b 必须重新生成（人物描述可能变化）
- 场景资产卡.md 更新 → Phase 2b 必须重新生成（场景描述可能变化）

---

## 9. 实施步骤

1. 创建正确目录结构 `05-Phase2b-Prompt/`
2. 更新 `agents/orchestrator/phases/Phase2b/` 下的执行文档（Step1/Step2/Step3）
3. 更新 `docs/output目录结构规范.md` 中的 Phase 2b 目录说明
4. 删除冗余目录 `05-Phase2b-视频提示词/` 和 `05-Phase2b-Prompt生成/`
5. 将生成脚本移至 `scripts/` 目录
6. 重新生成 Phase 2b 输出（基于正确的生成逻辑）

---

## 10. 成功标准

- 一个 Phase 2b 目录，中文/英文分开
- 338个shot，每个内容独特（不模板重复）
- 中英文同时生成，内容一致
- 每个shot格式为格式A（带基本信息表）
- 质量评分 ≥ 9.0/10
