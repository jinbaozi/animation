# VideoPrompt Industrial Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the documentation, rules, templates, and orchestration contracts so this project reliably converts novel text or user descriptions into high-quality, multi-tool VideoPrompt packages.

**Architecture:** Keep the existing Phase 0 → Phase 1 → Phase 1.5 → Phase 2a → Phase 2b flow, but redefine it around four intermediate representations: Story IR, Shot IR, Visual Anchor IR, and Prompt Export IR. Promote the audit system into a formal Audit Gate and move Seedance2, 即梦, and Chinese review output into explicit tool-export profiles.

**Tech Stack:** Markdown rule system, shell orchestration script, Claude Code prompt workflow, graphify/MCP references, git-based review.

---

## Reference Spec

Primary design document:

- `docs/superpowers/specs/2026-04-29-video-prompt-industrial-pipeline-design.md`

Implementation must preserve these approved decisions:

- Final workflow scope ends at VideoPrompt package delivery.
- Phase 2a remains required as the visual consistency anchor layer.
- Multi-tool export is supported through shared Prompt Export IR.
- Audit becomes a formal delivery gate.
- Default coverage standard is 100% for required intermediate assets and final core VideoPrompt export.
- Concrete project counts such as “12 characters” or “8 scenes” must not live in generic role/rule files.

---

## File Structure Map

### New Files

- `agents/orchestrator/roles/orchestrator-role.md`  
  Canonical role definition for the orchestrator. This fixes the broken reference in `agents/orchestrator/roles/README.md`.

- `rules/中间表示规范.md`  
  Shared Story IR, Shot IR, Visual Anchor IR, and Prompt Export IR schema rules.

- `templates/output/StoryIR模板.md`  
  Concrete output template for Phase 1 Story IR.

- `templates/output/ShotIR模板.md`  
  Concrete output template for Phase 1.5 Shot IR.

- `templates/output/VisualAnchorIR模板.md`  
  Concrete output template for Phase 2a Visual Anchor IR.

- `templates/output/PromptExportIR模板.md`  
  Concrete output template for Phase 2b Prompt Export IR.

- `templates/output/ToolExport-Seedance2.md`  
  Seedance2 export format and validation checklist.

- `templates/output/ToolExport-即梦.md`  
  即梦/豆包 export format and validation checklist.

- `templates/output/ToolExport-中文审阅版.md`  
  Human-readable simplified Chinese review format.

### Existing Files To Modify

- `agents/orchestrator/orchestrator.md`  
  Update the main pipeline, final delivery boundary, Phase map, and reference to `orchestrator-role.md`.

- `agents/orchestrator/00-index.md`  
  Update the orchestrator index to include IR and Audit Gate.

- `agents/orchestrator/roles/README.md`  
  Make role index match the new canonical role files and responsibilities.

- `agents/orchestrator/roles/compliance-role.md`  
  Reframe as full-pipeline rule gate owner, not only Phase 0 content reviewer.

- `agents/orchestrator/roles/director-role.md`  
  Reframe around Story IR ownership.

- `agents/orchestrator/roles/shot-designer-role.md`  
  Reframe around Shot IR ownership.

- `agents/orchestrator/roles/art-director-role.md`  
  Reframe around Visual Anchor IR and Prompt Export IR visual fields. Remove hardcoded sample project checks from generic role rules.

- `agents/orchestrator/phases/Phase0/Phase0-主索引.md`  
  Add G0/G1 relationship and project manifest dependency.

- `agents/orchestrator/phases/Phase1/Phase1-主索引.md`  
  Add Story IR as a first-class output.

- `agents/orchestrator/phases/Phase1/Step2-剧本改编.md`  
  Align script generation with Story IR, dialogue provenance, and non-outline requirements.

- `agents/orchestrator/phases/Phase1/Step3-分镜设计.md`  
  Keep basic storyboard, but clarify it is upstream intent for Shot IR.

- `agents/orchestrator/phases/Phase1.5/Phase1.5-主索引.md`  
  Add Shot IR as a first-class output.

- `agents/orchestrator/phases/Phase1.5/Step1-镜头序列设计.md`  
  Replace broad audit language with Shot IR continuity contracts.

- `agents/orchestrator/phases/Phase1.5/Step2-序列衔接表.md`  
  Align sequence continuity table with Shot IR fields.

- `agents/orchestrator/phases/Phase2a/Phase2a-主索引.md`  
  Add Visual Anchor IR output and 100% coverage gate.

- `agents/orchestrator/phases/Phase2a/Step2-四视图生成.md`  
  Remove fixed example counts and project-specific names from generic rules.

- `agents/orchestrator/phases/Phase2a/Step3-场景资产卡.md`  
  Remove fixed example counts and align with Visual Anchor IR.

- `agents/orchestrator/phases/Phase2b/Phase2b-主索引.md`  
  Add Prompt Export IR and Tool Export outputs.

- `agents/orchestrator/phases/Phase2b/Step2-时间分段.md`  
  Move time segmentation into tool profiles.

- `agents/orchestrator/phases/Phase2b/Step3-VideoPrompt生成.md`  
  Refactor from a single output format into Prompt Export IR plus tool exports.

- `agents/orchestrator/phases/Phase2b/Phase2b-质量标准.md`  
  Resolve 80% vs 100% coverage conflict.

- `agents/audit/audit-agent.md`  
  Promote to Audit Gate and align input list with new output directories.

- `agents/audit/Phase3/Phase3-主索引.md`  
  Rename conceptually from Phase 3 to Audit Gate in wording while preserving path compatibility.

- `rules/00-index.md`  
  Add `中间表示规范.md` and update load order.

- `rules/视频格式.md`  
  Change from one canonical timing format to shared Prompt Export IR plus tool profiles.

- `rules/双轨生成.md`  
  Keep language positioning, but make it a review/export alignment rule instead of a primary generation flow.

- `rules/运镜知识.md`  
  Remove or qualify conflicting generic recommendations such as `cinematic` and `photorealistic` when project style forbids them.

- `rules/质量门禁.md`  
  Replace 10-stage production gate with G0-G6 VideoPrompt delivery gates.

- `rules/输出验证.md`  
  Align final verification with IR, full delivery mode, and explicit simplified delivery mode.

- `templates/00-index.md`  
  Register new IR and tool export templates.

- `docs/编排师操作手册.md`  
  Update state machine, input package assembly, return routing, and version mapping.

- `docs/output目录结构规范.md`  
  Update output directories to include IR, tool exports, Audit Gate, and final package.

- `knowledge/00-知识库索引.md`  
  Update top-level conceptual map and remove stale claims about final stages.

- `scripts/orchestrate.sh`  
  Evaluate after documentation changes. Update only if the docs and script disagree in a way that blocks usage.

---

## Task 1: Orchestrator Boundary And Role Index

**Files:**
- Create: `agents/orchestrator/roles/orchestrator-role.md`
- Modify: `agents/orchestrator/orchestrator.md`
- Modify: `agents/orchestrator/00-index.md`
- Modify: `agents/orchestrator/roles/README.md`

- [ ] **Step 1: Create canonical orchestrator role file**

Create `agents/orchestrator/roles/orchestrator-role.md` with this structure:

```markdown
# 编排师 — 角色职责规范

> 状态：已确认 | 版本：v2.0 | 日期：2026-04-29
> 核心定位：VideoPrompt 工业化流水线的状态机、契约校验与版本链中枢

---

## 1. 核心定位

编排师是用户与所有执行角色之间的唯一通信中枢。编排师不生产具体创作内容，只负责把用户输入转化为可执行任务，维护阶段状态、输入输出契约、质量门禁、返工路由和最终交付索引。

---

## 2. 职责边界

### 编排师职责

| # | 职责 | 说明 |
|---|---|---|
| 1 | 项目配置 | 生成并维护 project manifest |
| 2 | 阶段调度 | 调度 Phase 0、Phase 1、Phase 1.5、Phase 2a、Phase 2b、Audit Gate |
| 3 | 输入包组装 | 为每个阶段组装完整输入包 |
| 4 | 契约校验 | 校验阶段输入输出是否符合 IR 与门禁要求 |
| 5 | 版本链管理 | 记录 Story IR、Shot IR、Visual Anchor IR、Prompt Export IR 与导出包版本映射 |
| 6 | 返工路由 | 按问题归属路由到对应责任角色 |
| 7 | 最终交付 | 汇总最终 VideoPrompt 包、审核报告、版本链和交付检查清单 |

### 编排师禁止行为

| # | 禁止行为 | 说明 |
|---|---|---|
| 1 | 不写剧本 | 剧本由内容总导演负责 |
| 2 | 不改分镜 | 镜头设计由镜头序列设计师负责 |
| 3 | 不写视觉资产 | 四视图和场景资产由美术技术总监负责 |
| 4 | 不写工具 Prompt | 工具导出由 Prompt 适配器或 Phase 2b 模块负责 |
| 5 | 不绕过门禁 | G0-G6 与 Audit Gate 必须按流程执行 |

---

## 3. 交付边界

本系统主流程只交付到 VideoPrompt 包。成片生成、配音合成、上线发布、版权证书和后期剪辑不属于当前主流程。

---

## 4. 主流程

```text
Input
→ G0 项目配置门禁
→ Phase 0 合规与风险预审
→ Phase 1 Story IR 与剧本
→ Phase 1.5 Shot IR 与镜头连续性
→ Phase 2a Visual Anchor IR
→ Phase 2b Prompt Export IR
→ Tool Export
→ Audit Gate
→ Final VideoPrompt Package
```
```

- [ ] **Step 2: Update orchestrator entrypoint**

In `agents/orchestrator/orchestrator.md`, update the role definition reference:

```markdown
> **角色定义**：详细角色定义见 `roles/orchestrator-role.md`
```

Replace the current Phase flow with:

```markdown
用户提交任务
    │
    ▼
G0（项目配置门禁）→ Phase 0（品控合规官）→ Phase 1（内容总导演）
    → Phase 1.5（镜头序列设计师）→ Phase 2a（美术技术总监）
    → Phase 2b（美术技术总监 + Prompt适配器）→ Audit Gate（审核智能体）
    → 最终 VideoPrompt 交付
```

Replace the Phase input-output mapping with:

```markdown
| 阶段 | 执行角色 | 输入 | 输出 |
|---|---|---|---|
| G0 | 编排师 | 用户任务 | project-manifest.md |
| Phase 0 | 品控合规官 | 小说文本、项目配置 | 合规预审报告.md |
| Phase 1 | 内容总导演 | 合规通过的输入包 | StoryIR.md、剧本.md、人物清单.md、场景清单.md |
| Phase 1.5 | 镜头序列设计师 | Story IR、剧本、基础分镜 | ShotIR.md、增强分镜执行表.md、序列衔接与继承表.md |
| Phase 2a | 美术技术总监 | Shot IR、人物清单、场景清单 | VisualAnchorIR.md、人物四视图Prompt包.md、场景资产卡.md |
| Phase 2b | 美术技术总监 + Prompt适配器 | Visual Anchor IR、Shot IR | PromptExportIR.md、多工具 VideoPrompt 导出 |
| Audit Gate | 审核智能体 | 全部 IR 与导出包 | 审核报告.md、返工问题清单或通过结论 |
```

- [ ] **Step 3: Update role README**

In `agents/orchestrator/roles/README.md`, update the role index to include `orchestrator-role.md` as an existing canonical file and add Prompt 适配器 as a Phase 2b module:

```markdown
| 文件 | 角色 | Phase | 判断类型 |
|---|---|---|---|
| `orchestrator-role.md` | 编排师 | G0/全流程 | 分析型 |
| `compliance-role.md` | 品控合规官 | Phase 0/G1-G6规则门禁 | 分析型 |
| `director-role.md` | 内容总导演 | Phase 1 | 体感型 |
| `shot-designer-role.md` | 镜头序列设计师 | Phase 1.5 | 感知型 + 体感型 |
| `art-director-role.md` | 美术技术总监 | Phase 2a/2b | 分析型 |
| `Prompt适配器` | Phase 2b内部模块 | Phase 2b导出 | 分析型 |
| `audit-agent.md` | 审核智能体 | Audit Gate | 分析型 + LLM细审 |
```

- [ ] **Step 4: Verify task 1**

Run:

```bash
rg "orchestrator-role.md|Audit Gate|Prompt适配器|G0" agents/orchestrator
```

Expected:

- `orchestrator-role.md` exists.
- `orchestrator.md` references the new role file.
- Role README mentions Audit Gate and Prompt 适配器.

- [ ] **Step 5: Commit task 1**

```bash
git add agents/orchestrator/orchestrator.md agents/orchestrator/00-index.md agents/orchestrator/roles/README.md agents/orchestrator/roles/orchestrator-role.md
git commit -m "docs: define industrial orchestrator boundary"
```

---

## Task 2: Add IR Rules And Output Templates

**Files:**
- Create: `rules/中间表示规范.md`
- Create: `templates/output/StoryIR模板.md`
- Create: `templates/output/ShotIR模板.md`
- Create: `templates/output/VisualAnchorIR模板.md`
- Create: `templates/output/PromptExportIR模板.md`
- Modify: `rules/00-index.md`
- Modify: `templates/00-index.md`

- [ ] **Step 1: Create IR rule file**

Create `rules/中间表示规范.md`:

```markdown
# 中间表示规范

> 状态：v1.0 | 日期：2026-04-29
> 作用：定义 Story IR、Shot IR、Visual Anchor IR、Prompt Export IR 的字段契约。

---

## 1. 总原则

所有最终 VideoPrompt 必须从 Prompt Export IR 导出。Prompt Export IR 必须可追溯到 Visual Anchor IR、Shot IR 和 Story IR。

禁止绕过 IR 直接从小说文本生成最终工具 Prompt。

---

## 2. Story IR

Story IR 是叙事事实源，由内容总导演负责。

必填字段：

| 字段 | 说明 |
|---|---|
| project_id | 项目唯一标识 |
| source_summary | 原始小说或描述摘要 |
| story_units | 章节、段落或剧情单元 |
| character_graph | 人物关系、目标、冲突 |
| scene_list | 场景编号、时间、地点、氛围 |
| dialogue_source | 可拍摄台词及来源 |
| emotional_beats | 情绪压强、前摇、释放、余震 |
| shot_volume_plan | 目标镜头数和序列数 |

---

## 3. Shot IR

Shot IR 是镜头事实源，由镜头序列设计师负责。

必填字段：

| 字段 | 说明 |
|---|---|
| shot_id | 全局唯一镜号 |
| scene_id | 对应场景编号 |
| scene_type | 8种场景类型之一 |
| narrative_function | 建立、推进、反应、转折、落幅 |
| subject | 具体角色名或场景主体 |
| action | 可见动作 |
| gaze | 视线方向和落点 |
| shot_size | 景别 |
| camera_movement | 运镜 |
| opening_frame | 起幅 |
| closing_frame | 落幅 |
| continuity | 服装、位置、道具、光线、运动方向 |

---

## 4. Visual Anchor IR

Visual Anchor IR 是视觉一致性事实源，由美术技术总监负责。

必填字段：

| 字段 | 说明 |
|---|---|
| character_anchors | 人物四视图、特殊标记、服装阶段 |
| scene_anchors | 场景资产卡、布局、光源、色调 |
| style_anchors | 风格关键词、禁用词、色彩、材质 |
| prop_anchors | 关键道具视觉特征 |
| reference_map | 参考图或 AD image 映射 |
| version_map | 上游依据版本 |

---

## 5. Prompt Export IR

Prompt Export IR 是多工具导出的唯一来源。

必填字段：

| 字段 | 说明 |
|---|---|
| shot_id | 对应 Shot IR |
| subject_anchor | 主体锚定 |
| action_unit | 可执行动作 |
| gaze_unit | 视线和眼神 |
| camera_unit | 景别、角度、运镜 |
| environment_unit | 场景细节 |
| lighting_unit | 光源、色温、方向 |
| style_anchor | 风格锚点 |
| continuity | 起幅落幅和相邻镜头连续性 |
| reference_map | 参考图映射 |
| negative_constraints | 负面约束 |
| tool_profiles | 目标工具导出配置 |

---

## 6. 覆盖率

默认完整交付模式：

- Story IR 覆盖核心剧情 100%。
- Shot IR 覆盖目标镜头规划 100%。
- Visual Anchor IR 人物和场景覆盖率 100%。
- Prompt Export IR 覆盖核心镜头 100%。

精简交付模式必须显式标注被合并或未导出的镜头，不得伪装为完整交付。
```

- [ ] **Step 2: Create Story IR template**

Create `templates/output/StoryIR模板.md`:

```markdown
# Story IR

> 项目：{项目名}
> 版本：v1.0
> 依据：{原始输入文件或用户描述}

## 1. 项目配置摘要

| 字段 | 内容 |
|---|---|
| 项目名 |  |
| 目标平台 |  |
| 目标工具 |  |
| 风格 |  |
| 交付模式 | 完整交付 |

## 2. 原文拆解

| 单元ID | 原文范围 | 核心事件 | 冲突 | 情绪 |
|---|---|---|---|---|

## 3. 人物关系

| 角色 | 关系 | 目标 | 冲突 | 变化 |
|---|---|---|---|---|

## 4. 场景清单

| 场景编号 | 场景名 | 时间 | 地点 | 氛围 | 关键道具 |
|---|---|---|---|---|---|

## 5. 台词来源

| 台词ID | 角色 | 台词 | 来源单元 | 用途 |
|---|---|---|---|---|

## 6. 情绪节拍

| 节拍ID | 场景 | 压强 | 前摇 | 释放 | 余震 |
|---|---|---|---|---|---|

## 7. 体量规划

| 指标 | 值 | 说明 |
|---|---|---|
| 原文字数 |  |  |
| 目标镜头数 |  | 按 `ceil(总字数 / 80)` 参考 |
| 目标序列数 |  | 按工具 profile 生成 |
```

- [ ] **Step 3: Create Shot IR template**

Create `templates/output/ShotIR模板.md`:

```markdown
# Shot IR

> 项目：{项目名}
> 版本：v1.0
> 依据：StoryIR.md v1.0

## 镜头表

| shot_id | scene_id | scene_type | narrative_function | subject | action | gaze | shot_size | camera_movement | opening_frame | closing_frame | continuity |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 连续性检查

| shot_id | 上一镜落幅 | 本镜起幅 | 服装 | 位置 | 道具 | 光线 | 运动方向 |
|---|---|---|---|---|---|---|---|

## 轴线与视线检查

| shot_id | 轴线状态 | 视线落点 | 承接物 | 问题 |
|---|---|---|---|---|

## 动作戏检查

| shot_id | 起幅 | 运动 | 落幅 | 回收 | 是否单拍单动作 |
|---|---|---|---|---|---|
```

- [ ] **Step 4: Create Visual Anchor IR template**

Create `templates/output/VisualAnchorIR模板.md`:

```markdown
# Visual Anchor IR

> 项目：{项目名}
> 版本：v1.0
> 依据：StoryIR.md v1.0 | ShotIR.md v1.0

## 1. 人物锚点

| 角色 | 四视图状态 | 特殊标记 | 服装阶段 | 参考图编号 | 覆盖 |
|---|---|---|---|---|---|

## 2. 场景锚点

| 场景编号 | 场景名 | 布局 | 光源 | 色调 | 关键道具 | 覆盖 |
|---|---|---|---|---|---|---|

## 3. 风格锚点

| 维度 | 规则 |
|---|---|
| 画风 |  |
| 色彩 |  |
| 光影 |  |
| 材质 |  |
| 禁用词 |  |

## 4. 道具锚点

| 道具 | 所属角色或场景 | 视觉特征 | 出现镜头 |
|---|---|---|---|

## 5. 版本映射

| Visual Anchor 输出 | 依据版本 |
|---|---|
```

- [ ] **Step 5: Create Prompt Export IR template**

Create `templates/output/PromptExportIR模板.md`:

```markdown
# Prompt Export IR

> 项目：{项目名}
> 版本：v1.0
> 依据：ShotIR.md v1.0 | VisualAnchorIR.md v1.0

## Prompt 单元

| shot_id | subject_anchor | action_unit | gaze_unit | camera_unit | environment_unit | lighting_unit | style_anchor | continuity | reference_map | negative_constraints | tool_profiles |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 工具导出配置

| 工具 | 语言 | 时间分段 | 参考图规则 | 输出目录 |
|---|---|---|---|---|
| Seedance2 | 英文 | 4-5秒分段 | AD Reference 必填 | `06-ToolExports/Seedance2/` |
| 即梦 | 简体中文或工具指定格式 | 按工具 profile | 参考图按需 | `06-ToolExports/Jimeng/` |
| 中文审阅版 | 简体中文 | 人类审阅友好 | 可选 | `06-ToolExports/中文审阅版/` |
```

- [ ] **Step 6: Register new rules and templates**

In `rules/00-index.md`, add `中间表示规范.md` after `剧本格式规范.md`:

```markdown
| `中间表示规范.md` | Phase 1-2b 生成前 | 0.8 | 剧本格式规范.md |
```

In `templates/00-index.md`, add the new output templates under `output/`:

```markdown
| `StoryIR模板.md` | Phase 1 |
| `ShotIR模板.md` | Phase 1.5 |
| `VisualAnchorIR模板.md` | Phase 2a |
| `PromptExportIR模板.md` | Phase 2b |
| `ToolExport-Seedance2.md` | Phase 2b 工具导出 |
| `ToolExport-即梦.md` | Phase 2b 工具导出 |
| `ToolExport-中文审阅版.md` | Phase 2b 人工审阅 |
```

- [ ] **Step 7: Verify task 2**

Run:

```bash
rg "Story IR|Shot IR|Visual Anchor IR|Prompt Export IR|中间表示规范" rules templates
```

Expected:

- New rule and templates are discoverable from indexes.
- All four IR names appear in both rules and templates.

- [ ] **Step 8: Commit task 2**

```bash
git add rules/00-index.md rules/中间表示规范.md templates/00-index.md templates/output/StoryIR模板.md templates/output/ShotIR模板.md templates/output/VisualAnchorIR模板.md templates/output/PromptExportIR模板.md
git commit -m "docs: add intermediate representation contracts"
```

---

## Task 3: Reframe Execution Roles Around Ownership Boundaries

**Files:**
- Modify: `agents/orchestrator/roles/compliance-role.md`
- Modify: `agents/orchestrator/roles/director-role.md`
- Modify: `agents/orchestrator/roles/shot-designer-role.md`
- Modify: `agents/orchestrator/roles/art-director-role.md`

- [ ] **Step 1: Update compliance role**

In `compliance-role.md`, replace the Phase-only positioning with:

```markdown
**身份**：全流程规则门禁官

**核心价值**：

| # | 价值 | 说明 |
|---|---|---|
| 1 | 合规前置 | 在 Phase 0 识别平台、版权和内容风险 |
| 2 | 规则门禁 | 在 G2-G6 检查格式、覆盖率、语言纯净度、禁用词和交叉引用 |
| 3 | 阻断判定 | 对 P0 级规则错误给出阻断结论 |
| 4 | 抽检策略 | 对 AI 自检结果设置人工抽检比例 |
```

Replace its “不作品控判断” wording with:

```markdown
| 1 | 不做艺术裁决 | 不判断某个镜头是否“更美”或“更高级”，只判断是否违反明确规则 |
```

- [ ] **Step 2: Update director role**

In `director-role.md`, update core responsibility:

```markdown
**核心职责**：负责 Story IR。内容总导演把小说文本或用户描述转化为剧本、人物关系、场景事实、台词来源、情绪节拍和基础分镜意图。
```

Add to prohibited behavior:

```markdown
| # | 禁止行为 | 说明 |
|---|---|---|
| 7 | 不写 Shot IR 最终镜头语言 | 镜头序列、轴线、起幅落幅由镜头序列设计师负责 |
| 8 | 不写工具导出 Prompt | Seedance2、即梦等格式由 Phase 2b 处理 |
```

- [ ] **Step 3: Update shot designer role**

In `shot-designer-role.md`, update core responsibility:

```markdown
**核心职责**：负责 Shot IR。镜头序列设计师把 Story IR 和基础分镜意图转化为可执行镜头单元，补齐景别、运镜、轴线、视线、起幅、落幅和连续性。
```

Constrain its upstream audit:

```markdown
Phase 1.5 对 Phase 1 的审核只检查“叙事是否能被镜头执行”。剧情主题、人物弧光和台词风格的最终改写权仍属于内容总导演。
```

- [ ] **Step 4: Update art director role**

In `art-director-role.md`, update core responsibility:

```markdown
**核心职责**：负责 Visual Anchor IR 和 Prompt Export IR 的视觉字段。美术技术总监把 Shot IR 中的镜头意图转化为角色、场景、风格、道具和参考图锚点，并为 Prompt Export IR 提供稳定视觉约束。
```

Remove generic hardcoded examples such as fixed role counts and specific names from mandatory checklists. Replace them with:

```markdown
人物数量、场景数量、角色名、场景名和特殊标记来自 project manifest、Story IR 和人物/场景清单。通用角色规范不得硬编码具体项目示例。
```

- [ ] **Step 5: Verify task 3**

Run:

```bash
rg "Story IR|Shot IR|Visual Anchor IR|Prompt Export IR|通用角色规范不得硬编码" agents/orchestrator/roles
```

Run:

```bash
rg "必须12个|必须8个|吴为|老约翰|村长|梅丽夫人|霍利" agents/orchestrator/roles/art-director-role.md
```

Expected:

- First command finds the new ownership language.
- Second command returns no project-specific hardcoded examples in the generic role file.

- [ ] **Step 6: Commit task 3**

```bash
git add agents/orchestrator/roles/compliance-role.md agents/orchestrator/roles/director-role.md agents/orchestrator/roles/shot-designer-role.md agents/orchestrator/roles/art-director-role.md
git commit -m "docs: clarify agent ownership boundaries"
```

---

## Task 4: Align Phase Contracts With IR Outputs

**Files:**
- Modify: `agents/orchestrator/phases/Phase0/Phase0-主索引.md`
- Modify: `agents/orchestrator/phases/Phase1/Phase1-主索引.md`
- Modify: `agents/orchestrator/phases/Phase1/Step2-剧本改编.md`
- Modify: `agents/orchestrator/phases/Phase1/Step3-分镜设计.md`
- Modify: `agents/orchestrator/phases/Phase1.5/Phase1.5-主索引.md`
- Modify: `agents/orchestrator/phases/Phase1.5/Step1-镜头序列设计.md`
- Modify: `agents/orchestrator/phases/Phase1.5/Step2-序列衔接表.md`
- Modify: `agents/orchestrator/phases/Phase2a/Phase2a-主索引.md`
- Modify: `agents/orchestrator/phases/Phase2a/Step2-四视图生成.md`
- Modify: `agents/orchestrator/phases/Phase2a/Step3-场景资产卡.md`
- Modify: `agents/orchestrator/phases/Phase2b/Phase2b-主索引.md`
- Modify: `agents/orchestrator/phases/Phase2b/Step2-时间分段.md`
- Modify: `agents/orchestrator/phases/Phase2b/Step3-VideoPrompt生成.md`
- Modify: `agents/orchestrator/phases/Phase2b/Phase2b-质量标准.md`

- [ ] **Step 1: Add G0/G1 relationship to Phase 0**

In `Phase0-主索引.md`, change input from:

```markdown
| 输入 | 小说文本、改编要求、目标平台、项目名 |
```

to:

```markdown
| 输入 | 小说文本或剧情描述、project-manifest.md、改编要求 |
```

Add:

```markdown
Phase 0 属于 G1 合规门禁。Phase 0 不生成叙事、分镜或 Prompt，只输出合规预审报告和风险清单。
```

- [ ] **Step 2: Add Story IR to Phase 1**

In `Phase1-主索引.md`, update output list:

```markdown
| StoryIR.md | Markdown表格与结构化小节 | 是 |
| 剧本.md | Markdown | 是 |
| 基础分镜执行表.md | Markdown表格 | 是 |
| 人物清单.md | Markdown表格 | 是 |
| 场景清单.md | Markdown表格 | 是 |
```

Add `templates/output/StoryIR模板.md` to the module/template index.

- [ ] **Step 3: Align script adaptation with Story IR**

In `Step2-剧本改编.md`, add:

```markdown
剧本.md 必须从 Story IR 的台词来源、人物关系、场景事实和情绪节拍派生。分镜表和 Prompt 不得在下游重新发明台词。
```

Keep the existing non-outline requirements.

- [ ] **Step 4: Clarify basic storyboard as upstream intent**

In `Step3-分镜设计.md`, add:

```markdown
基础分镜执行表是 Shot IR 的上游意图，不是最终镜头语言。最终景别、轴线、起幅、落幅和连续性由 Phase 1.5 的 Shot IR 冻结。
```

- [ ] **Step 5: Add Shot IR to Phase 1.5**

In `Phase1.5-主索引.md`, update output:

```markdown
| 输出 | ShotIR.md + 增强分镜执行表.md + 序列衔接与继承表.md |
```

Add `templates/output/ShotIR模板.md` to the module/template index.

- [ ] **Step 6: Refactor shot sequence step**

In `Step1-镜头序列设计.md`, add a section:

```markdown
## Shot IR 核心字段

每个镜头必须补齐：

| 字段 | 要求 |
|---|---|
| shot_id | 全局连续编号 |
| scene_type | 8种场景类型之一 |
| narrative_function | 建立、推进、反应、转折、落幅 |
| subject | 必须使用具体角色名或场景主体 |
| action | 可见、可执行动作 |
| gaze | 视线方向和落点 |
| shot_size | 景别 |
| camera_movement | 运镜 |
| opening_frame | 起幅 |
| closing_frame | 落幅 |
| continuity | 与前后镜头的服装、位置、道具、光线、运动方向连续性 |
```

- [ ] **Step 7: Add Visual Anchor IR to Phase 2a**

In `Phase2a-主索引.md`, update output:

```markdown
| 输出 | VisualAnchorIR.md + 人物四视图Prompt包.md + 场景资产卡.md |
```

Add `templates/output/VisualAnchorIR模板.md`.

- [ ] **Step 8: Remove hardcoded Phase 2a examples**

In `Step2-四视图生成.md` and `Step3-场景资产卡.md`, replace fixed example counts with:

```markdown
覆盖数量必须来自 project manifest、人物清单和场景清单。若人物清单包含 N 个角色，则人物四视图覆盖率必须为 N/N。若场景清单包含 M 个场景，则场景资产卡覆盖率必须为 M/M。
```

- [ ] **Step 9: Add Prompt Export IR to Phase 2b**

In `Phase2b-主索引.md`, update output:

```markdown
| 输出 | PromptExportIR.md + Seedance2导出包 + 即梦导出包 + 中文审阅版 + 双语对照版 |
```

Add `templates/output/PromptExportIR模板.md` and tool export templates to the module index.

- [ ] **Step 10: Move timing rules into tool profiles**

In `Step2-时间分段.md`, replace any single universal time segmentation rule with:

```markdown
时间分段由工具 profile 决定：

| 工具 | 默认分段 |
|---|---|
| Seedance2 | 4-5秒单段，独立生成 |
| 即梦/豆包 | 按工具 profile 配置 |
| 中文审阅版 | 可使用人类可读段落，不作为工具提交格式 |
```

- [ ] **Step 11: Refactor VideoPrompt generation step**

In `Step3-VideoPrompt生成.md`, replace “逐 Shot 直接生成中英文五段式” as the core flow with:

```markdown
For each Shot IR unit:
    1. 合并 Shot IR 的镜头字段
    2. 合并 Visual Anchor IR 的角色、场景、风格和道具锚点
    3. 生成 Prompt Export IR
    4. 通过工具 profile 导出 Seedance2、即梦、中文审阅版和双语对照版
    5. 执行 G5 Prompt Export 门禁
```

- [ ] **Step 12: Resolve coverage conflict**

In `Phase2b-质量标准.md`, replace default 80% requirement with:

```markdown
默认完整交付模式要求核心镜头 VideoPrompt 导出覆盖率 100%。精简交付模式可以低于 100%，但必须在文件头显式标注交付模式、覆盖率、被合并镜头和未导出镜头。
```

- [ ] **Step 13: Verify task 4**

Run:

```bash
rg "StoryIR.md|ShotIR.md|VisualAnchorIR.md|PromptExportIR.md|完整交付模式|精简交付模式" agents/orchestrator/phases
```

Run:

```bash
rg "必须12个|必须8个|338个shot|覆盖率 ≥80%|覆盖率≥80%" agents/orchestrator/phases
```

Expected:

- First command finds IR outputs in all relevant phases.
- Second command returns no generic hardcoded counts or default 80% coverage requirements.

- [ ] **Step 14: Commit task 4**

```bash
git add agents/orchestrator/phases/Phase0/Phase0-主索引.md agents/orchestrator/phases/Phase1/Phase1-主索引.md agents/orchestrator/phases/Phase1/Step2-剧本改编.md agents/orchestrator/phases/Phase1/Step3-分镜设计.md agents/orchestrator/phases/Phase1.5/Phase1.5-主索引.md agents/orchestrator/phases/Phase1.5/Step1-镜头序列设计.md agents/orchestrator/phases/Phase1.5/Step2-序列衔接表.md agents/orchestrator/phases/Phase2a/Phase2a-主索引.md agents/orchestrator/phases/Phase2a/Step2-四视图生成.md agents/orchestrator/phases/Phase2a/Step3-场景资产卡.md agents/orchestrator/phases/Phase2b/Phase2b-主索引.md agents/orchestrator/phases/Phase2b/Step2-时间分段.md agents/orchestrator/phases/Phase2b/Step3-VideoPrompt生成.md agents/orchestrator/phases/Phase2b/Phase2b-质量标准.md
git commit -m "docs: align phase contracts with IR pipeline"
```

---

## Task 5: Unify Rules Around G0-G6 VideoPrompt Gates

**Files:**
- Modify: `rules/视频格式.md`
- Modify: `rules/双轨生成.md`
- Modify: `rules/运镜知识.md`
- Modify: `rules/质量门禁.md`
- Modify: `rules/输出验证.md`

- [ ] **Step 1: Refactor video format rule**

In `rules/视频格式.md`, add this top-level principle near the beginning:

```markdown
VideoPrompt 格式分为两层：

1. Prompt Export IR：所有工具导出的统一来源。
2. Tool Export：Seedance2、即梦、中文审阅版等具体工具格式。

任何工具格式不得直接覆盖 Prompt Export IR 的字段契约。
```

Move `0-3s` or `4-5秒` language into tool-specific sections.

- [ ] **Step 2: Refactor dual-track rule**

In `rules/双轨生成.md`, update positioning:

```markdown
双轨生成不再定义主流程。主流程先生成 Prompt Export IR，再导出中文审阅版、英文提交版和双语对照版。
```

Keep:

```markdown
中文 = 人类叙事/分镜审阅参考
英文 = Seedance2 实际提交 Prompt
双语对照版 = 一致性校验
```

- [ ] **Step 3: Qualify forbidden style conflicts in camera knowledge**

In `rules/运镜知识.md`, replace generic recommended style keywords that conflict with `rules/风格一致性.md`:

```markdown
风格关键词必须从当前项目风格 profile 中读取。下列表述只作为工具能力示例，不得绕过项目风格禁用词：

- cinematic
- photorealistic
- film grain
- 影视质感
- 电影级
```

Add:

```markdown
若项目风格为国风动漫，所有导出必须遵守 `rules/风格一致性.md` 和 `rules/风格/国风动漫.md` 的禁用词。
```

- [ ] **Step 4: Replace quality gate system**

In `rules/质量门禁.md`, replace the current 10-stage table with:

```markdown
## G0-G6 VideoPrompt 交付门禁

| Gate | 阶段 | 责任角色 | 核心检查 |
|---|---|---|---|
| G0 | 项目配置 | 编排师 | project manifest 完整 |
| G1 | 合规预审 | 品控合规官 | 平台、版权、敏感内容 |
| G2 | Story IR | 内容总导演 + 品控合规官 | 剧本、人物、场景、台词、体量规划 |
| G3 | Shot IR | 镜头序列设计师 | 镜号、景别、运镜、视线、起幅落幅、连续性 |
| G4 | Visual Anchor IR | 美术技术总监 | 人物四视图、场景资产、风格锚点、版本映射 |
| G5 | Prompt Export IR | 美术技术总监 + Prompt适配器 | Prompt字段完整、多工具导出一致 |
| G6 | Audit Gate | 审核智能体 | 8维度审核、P0/P1/P2问题分级 |
```

Move Phase 3-5 production content into a clearly marked appendix:

```markdown
## 附录：后续成片阶段预留

以下内容不属于当前 VideoPrompt 主流程，仅作未来扩展参考。
```

- [ ] **Step 5: Refactor output validation**

In `rules/输出验证.md`, add final delivery checks:

```markdown
## VideoPrompt 工业化交付检查

- [ ] project-manifest.md 存在
- [ ] StoryIR.md 存在
- [ ] ShotIR.md 存在
- [ ] VisualAnchorIR.md 存在
- [ ] PromptExportIR.md 存在
- [ ] Seedance2 导出包存在或在 manifest 中标注未启用
- [ ] 即梦导出包存在或在 manifest 中标注未启用
- [ ] 中文审阅版存在
- [ ] 双语对照版存在
- [ ] Audit Gate 通过或存在返工清单
- [ ] 完整交付模式覆盖率为 100%
- [ ] 精简交付模式显式列出合并和未导出镜头
```

- [ ] **Step 6: Verify task 5**

Run:

```bash
rg "G0|G1|G2|G3|G4|G5|G6|Prompt Export IR|Tool Export|精简交付模式" rules
```

Run:

```bash
rg "影视质感|电影级|photorealistic|cinematic|film grain" rules/运镜知识.md rules/视频格式.md
```

Expected:

- First command shows the new gate and IR vocabulary.
- Second command only finds those terms in warnings, examples, or style-profile-qualified contexts.

- [ ] **Step 7: Commit task 5**

```bash
git add rules/视频格式.md rules/双轨生成.md rules/运镜知识.md rules/质量门禁.md rules/输出验证.md
git commit -m "docs: unify prompt delivery quality gates"
```

---

## Task 6: Add Tool Export Templates

**Files:**
- Create: `templates/output/ToolExport-Seedance2.md`
- Create: `templates/output/ToolExport-即梦.md`
- Create: `templates/output/ToolExport-中文审阅版.md`
- Modify: `templates/00-index.md`

- [ ] **Step 1: Create Seedance2 export template**

Create `templates/output/ToolExport-Seedance2.md`:

```markdown
# Tool Export: Seedance2

> 用途：从 Prompt Export IR 导出 Seedance2 实际提交 Prompt
> 语言：英文为主，角色名可保留中文

## 导出规则

- 运镜和景别放在开头。
- 每段建议 4-5 秒。
- AD Reference 必填。
- 每个动作必须可执行。
- 每段必须包含视线或眼神。
- 负面 Prompt 只列举名词，不使用 no/not/do not/don't。

## 格式

```markdown
================================================================
[Shot ID] {shot_id} — Segment {segment_id}
================================================================

AD image 1 = {character_or_scene_reference}

{camera_unit}. {subject_anchor}, {action_unit}. {gaze_unit}. {environment_unit}. {lighting_unit}. {style_anchor}.

Negative constraints:
{negative_constraints}
```

## 检查清单

- [ ] 引用了 Prompt Export IR 的 shot_id
- [ ] AD image 编号连续
- [ ] 正文引用对应 AD image
- [ ] 无人称代词替代角色名
- [ ] 动作不是抽象情绪词
- [ ] 风格词不违反项目风格 profile
```

- [ ] **Step 2: Create 即梦 export template**

Create `templates/output/ToolExport-即梦.md`:

```markdown
# Tool Export: 即梦/豆包

> 用途：从 Prompt Export IR 导出即梦/豆包可用视频提示词
> 语言：按项目配置，可使用简体中文审阅友好格式

## 导出规则

- 保留主体、动作、视线、环境、灯光、风格字段。
- 时间分段按 project manifest 的工具 profile 执行。
- 不允许与 Visual Anchor IR 冲突。
- 不允许混用项目风格禁用词。

## 格式

```markdown
## 镜头 {shot_id}

| 字段 | 内容 |
|---|---|
| 主体 | {subject_anchor} |
| 动作 | {action_unit} |
| 视线 | {gaze_unit} |
| 镜头 | {camera_unit} |
| 环境 | {environment_unit} |
| 灯光 | {lighting_unit} |
| 风格 | {style_anchor} |
| 连续性 | {continuity} |
| 负面约束 | {negative_constraints} |
```

## 检查清单

- [ ] 每个字段来自 Prompt Export IR
- [ ] 时间分段符合工具 profile
- [ ] 中文表达清晰
- [ ] 角色名完整
- [ ] 风格词合规
```

- [ ] **Step 3: Create Chinese review template**

Create `templates/output/ToolExport-中文审阅版.md`:

```markdown
# Tool Export: 中文审阅版

> 用途：供用户、编排师和审核智能体审阅，不直接提交给 Seedance2。

## 格式

```markdown
## 镜头 {shot_id}：{narrative_function}

**主体**：{subject_anchor}
**动作**：{action_unit}
**视线**：{gaze_unit}
**镜头**：{camera_unit}
**环境**：{environment_unit}
**灯光**：{lighting_unit}
**风格**：{style_anchor}
**起幅**：{opening_frame}
**落幅**：{closing_frame}
**连续性**：{continuity}
**负面约束**：{negative_constraints}
```

## 检查清单

- [ ] 除专业术语外均使用简体中文
- [ ] 角色名不用代词替代
- [ ] 动作可见且可执行
- [ ] 起幅落幅明确
- [ ] 与 Shot IR 和 Visual Anchor IR 一致
```

- [ ] **Step 4: Verify task 6**

Run:

```bash
rg "Tool Export: Seedance2|Tool Export: 即梦|Tool Export: 中文审阅版|AD Reference|Prompt Export IR" templates/output templates/00-index.md
```

Expected:

- Three tool export templates exist.
- Template index references them.

- [ ] **Step 5: Commit task 6**

```bash
git add templates/00-index.md templates/output/ToolExport-Seedance2.md templates/output/ToolExport-即梦.md templates/output/ToolExport-中文审阅版.md
git commit -m "docs: add multi-tool prompt export templates"
```

---

## Task 7: Promote Audit System Into Formal Gate

**Files:**
- Modify: `agents/audit/audit-agent.md`
- Modify: `agents/audit/Phase3/Phase3-主索引.md`
- Modify: `agents/audit/Phase3/Step1-产物收集.md`
- Modify: `agents/audit/Phase3/Step2-规则预检.md`
- Modify: `agents/audit/Phase3/Step3-LLM细审.md`
- Modify: `agents/audit/Phase3/Phase3-报告生成.md`

- [ ] **Step 1: Update audit positioning**

In `agents/audit/audit-agent.md`, change trigger wording from Phase 2b completion to:

```markdown
> **触发时机**：Tool Export 完成后，最终交付前自动触发
> **流程定位**：Audit Gate，属于 VideoPrompt 交付门禁 G6
```

Update input products:

```markdown
| 产物 | 位置 | 审核维度 |
|---|---|---|
| project-manifest.md | `00-项目配置/` | 全局 |
| StoryIR.md | `02-Phase1-StoryIR/` | D4/D8 |
| ShotIR.md | `03-Phase1.5-ShotIR/` | D3/D5/D6/D7 |
| VisualAnchorIR.md | `04-Phase2a-VisualAnchorIR/` | D1/D2/D8 |
| PromptExportIR.md | `05-Phase2b-PromptExportIR/` | D1-D8 |
| Tool Exports | `06-ToolExports/` | D1-D8 |
```

- [ ] **Step 2: Update Phase3 wording**

In `agents/audit/Phase3/Phase3-主索引.md`, keep the directory path but update title:

```markdown
# Audit Gate: VideoPrompt 交付审核

> 路径兼容：当前仍位于 `agents/audit/Phase3/`，但流程定位是 G6 Audit Gate，不属于成片 Phase 3。
```

- [ ] **Step 3: Update collection step**

In `Step1-产物收集.md`, make required artifacts match the new output structure from the design spec:

```markdown
必需产物：

- `00-项目配置/project-manifest.md`
- `02-Phase1-StoryIR/StoryIR.md`
- `03-Phase1.5-ShotIR/ShotIR.md`
- `04-Phase2a-VisualAnchorIR/VisualAnchorIR.md`
- `05-Phase2b-PromptExportIR/PromptExportIR.md`
- `06-ToolExports/`
```

- [ ] **Step 4: Update report output**

In `Phase3-报告生成.md`, ensure the report includes:

```markdown
## 门禁结论

| 结论 | 处理 |
|---|---|
| PASS | 可生成最终交付包 |
| PASS_WITH_P1 | 可交付，但建议修复 P1 |
| FAIL_P0 | 阻断交付，必须返工 |

## 返工路由

| 问题ID | 级别 | 责任角色 | 目标文件 | 修复要求 |
|---|---|---|---|---|
```

- [ ] **Step 5: Verify task 7**

Run:

```bash
rg "Audit Gate|G6|project-manifest.md|StoryIR.md|ShotIR.md|VisualAnchorIR.md|PromptExportIR.md|返工路由" agents/audit
```

Expected:

- Audit system refers to G6 Audit Gate.
- Required inputs align with the new output structure.

- [ ] **Step 6: Commit task 7**

```bash
git add agents/audit/audit-agent.md agents/audit/Phase3/Phase3-主索引.md agents/audit/Phase3/Step1-产物收集.md agents/audit/Phase3/Step2-规则预检.md agents/audit/Phase3/Step3-LLM细审.md agents/audit/Phase3/Phase3-报告生成.md
git commit -m "docs: promote audit system to delivery gate"
```

---

## Task 8: Update Operations Docs And Evaluate Script Drift

**Files:**
- Modify: `docs/编排师操作手册.md`
- Modify: `docs/output目录结构规范.md`
- Modify: `knowledge/00-知识库索引.md`
- Evaluate: `scripts/orchestrate.sh`

- [ ] **Step 1: Update orchestrator manual state machine**

In `docs/编排师操作手册.md`, update state list to include:

```markdown
| G0_CONFIG_PENDING | 项目配置中 | config_complete() |
| PHASE0_PENDING | 合规预审中 | phase0_complete() / rework() |
| PHASE1_STORYIR_PENDING | Story IR 生成中 | phase1_complete() / rework() |
| PHASE1_5_SHOTIR_PENDING | Shot IR 生成中 | phase1_5_complete() / rework() |
| PHASE2A_VISUAL_ANCHOR_PENDING | Visual Anchor IR 生成中 | phase2a_complete() / rework() |
| PHASE2B_PROMPT_EXPORT_PENDING | Prompt Export IR 与工具导出中 | phase2b_complete() / rework() |
| AUDIT_GATE_PENDING | 交付审核中 | audit_complete() / rework() |
| FINAL_READY | 最终 VideoPrompt 包可交付 | deliver() |
```

- [ ] **Step 2: Update input package assembly**

In the same file, add input packages for:

```markdown
#### G0 项目配置输入包

| 项目 | 内容 | 验证 |
|---|---|---|
| 用户输入 | 小说文本或剧情描述 | 非空 |
| 目标平台 | 抖音/快手/B站/其他 | 非空 |
| 目标工具 | Seedance2/即梦/多工具 | 非空 |
| 风格 | 国风动漫/中国奇幻/3D等 | 非空 |

#### Audit Gate 输入包

| 项目 | 内容 | 验证 |
|---|---|---|
| project manifest | project-manifest.md | 存在 |
| Story IR | StoryIR.md | 存在 |
| Shot IR | ShotIR.md | 存在 |
| Visual Anchor IR | VisualAnchorIR.md | 存在 |
| Prompt Export IR | PromptExportIR.md | 存在 |
| Tool Exports | 06-ToolExports/ | 存在 |
```

- [ ] **Step 3: Update output directory spec**

In `docs/output目录结构规范.md`, replace the standard structure with:

```text
output/{项目名}_{日期}/
├── 00-项目配置/
├── 01-Phase0-合规预审/
├── 02-Phase1-StoryIR/
├── 03-Phase1.5-ShotIR/
├── 04-Phase2a-VisualAnchorIR/
├── 05-Phase2b-PromptExportIR/
├── 06-ToolExports/
├── 07-AuditGate/
└── 99-最终交付物/
```

- [ ] **Step 4: Update knowledge index**

In `knowledge/00-知识库索引.md`, update execution flow to:

```markdown
G0 项目配置 → Phase 0 合规预审 → Phase 1 Story IR → Phase 1.5 Shot IR
→ Phase 2a Visual Anchor IR → Phase 2b Prompt Export IR
→ Tool Export → Audit Gate → 最终 VideoPrompt 交付
```

Add `rules/中间表示规范.md` and new output templates to the quick navigation sections.

- [ ] **Step 5: Evaluate script drift**

Run:

```bash
rg "04-Phase2a-风格四视图|05-Phase2b-Prompt生成|0:00-0:03|338|覆盖率" scripts/orchestrate.sh
```

If the command finds stale hardcoded paths or time formats, update `scripts/orchestrate.sh` only enough to match the new docs:

- `04-Phase2a-风格四视图` → `04-Phase2a-VisualAnchorIR`
- `05-Phase2b-Prompt生成` → `05-Phase2b-PromptExportIR`
- Add `06-ToolExports` output instructions.
- Remove script-level universal `[0:00-0:03]` requirement.

Do not rewrite the shell script architecture in this task.

- [ ] **Step 6: Verify docs and script consistency**

Run:

```bash
rg "04-Phase2a-风格四视图|05-Phase2b-Prompt生成|0:00-0:03|338个shot|Phase 3：成片" docs knowledge scripts agents rules templates
```

Expected:

- No stale generic references remain, except in explicitly marked historical notes or examples.

Run:

```bash
bash -n scripts/orchestrate.sh
```

Expected:

- No shell syntax errors.

- [ ] **Step 7: Commit task 8**

```bash
git add docs/编排师操作手册.md docs/output目录结构规范.md knowledge/00-知识库索引.md scripts/orchestrate.sh
git commit -m "docs: sync operations with prompt pipeline"
```

---

## Final Verification

- [ ] **Step 1: Run global conflict scan**

```bash
rg "必须12个|必须8个|338个shot|覆盖率≥80%|覆盖率 ≥80%|0:00-0:03|0-3s|3-6s|Phase 3：成片|Phase 4：音效|Phase 5：版权" agents rules templates docs knowledge scripts
```

Expected:

- No stale generic requirements remain.
- Any remaining mentions are in historical notes, examples, or explicitly marked future appendices.

- [ ] **Step 2: Run IR discoverability scan**

```bash
rg "Story IR|Shot IR|Visual Anchor IR|Prompt Export IR|Audit Gate|Tool Export|project-manifest" agents rules templates docs knowledge
```

Expected:

- All major areas reference the new architecture.

- [ ] **Step 3: Run path consistency scan**

```bash
rg "02-Phase1-StoryIR|03-Phase1.5-ShotIR|04-Phase2a-VisualAnchorIR|05-Phase2b-PromptExportIR|06-ToolExports|07-AuditGate" docs agents rules templates knowledge scripts
```

Expected:

- Output directory references are consistent across operational docs, phase docs, and script prompts.

- [ ] **Step 4: Review git diff**

```bash
git diff --stat
git diff --check
```

Expected:

- Diff contains only documentation, rules, templates, and minimal script prompt/path updates.
- `git diff --check` reports no whitespace errors.

- [ ] **Step 5: Create final commit if any verification-only edits were made**

Only run this if final verification required follow-up edits after Task 8:

```bash
git add agents rules templates docs knowledge scripts
git commit -m "docs: finalize prompt pipeline consistency"
```

---

## Execution Notes

- Keep each task independently reviewable.
- Do not mix script refactoring with documentation rewrites unless a stale script prompt directly contradicts the new pipeline.
- Preserve existing Chinese terminology unless it conflicts with the new IR architecture.
- Use simplified Chinese for documentation prose except established technical terms such as `Story IR`, `Shot IR`, `Prompt Export IR`, `Audit Gate`, `Tool Export`, `Seedance2`, and `AD Reference`.
- Do not remove archived `bak/` files.
- Do not alter generated output examples unless they are used as active rules.

