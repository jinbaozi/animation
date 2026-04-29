---
title: "feat: Integrate graphify knowledge graph into /orchestrate workflow"
type: feat
status: completed
date: 2026-04-17
origin: docs/brainstorms/ (inline design doc: godxu-main-design-knowledge-graph-orchestrate-20260417-144028.md)
---

# feat: 知识图谱驱动编排工作流

## Overview

将 `/orchestrate` 命令从"空骨架 + agents 逐文件读规则"改造为"知识图谱驱动"架构：每个执行 Agent 在关键节点通过 graphify MCP 查询图谱获取规则，替代逐文件读取，实现单一真相源和可溯源交付物。

## Problem Frame

当前 `/orchestrate` 工作流的问题：
- agents 执行时靠逐文件读取获取规则上下文，效率低且无溯源
- `knowledge/` 已有图谱（92节点），但 agents 无法自动查询
- `rules/`、`agents/`、`templates/`、`docs/` 均未纳入图谱
- 图谱与源文件之间无强制同步机制

目标：agents 在关键节点强制查询图谱，生成可溯源（source_location）的工业级交付物。

## Requirements Trace

- R1. 各 Phase Agent 在执行前通过 graphify MCP 查询图谱获取必要规则
- R2. 图谱覆盖 `knowledge/`、`rules/`、`agents/`、`templates/scene/`、`templates/output/`、`docs/`
- R3. 文档变更通过 `/graphify` Skill 手动同步；代码变更通过 git hook 自动处理
- R4. 每个 Phase 的交付物附带图谱查询溯源记录（source_location）
- R5. orchestrate.sh 不启动 MCP server（编排师仅调度，不执行图谱查询）

## Scope Boundaries

- **不包含**：templates/scene/ 以外的内容解析（templates/output/ 仅索引）
- **不包含**：Phase 执行文档的具体 prompt 改写（Step 4 的具体内容）
- **不包含**：mcp_config.json 的具体格式（Step 3 的实现细节）

### Deferred to Separate Tasks

- Phase Agent 执行文档的具体改写（Step 4）：各 Phase 文档的图谱查询步骤需逐个编写
- templates/scene/ 完整解析（阶段 3）：需单独调用 `/graphify` Skill

## Context & Research

### Relevant Code and Patterns

- `graphify-out/graph.json`：现有 92 节点图谱（knowledge/）
- `agents/orchestrator/orchestrator.md`：编排师角色定义
- `agents/orchestrator/phases/Phase*/`：各 Phase 执行文档
- `rules/*.md`：规则文件（审美偏好、风格一致性、视频格式、运镜知识等）
- `.claude/commands/orchestrate.md`：`/orchestrate` 命令入口
- `scripts/orchestrate.sh`：编排脚本

### graphify 能力边界（已验证）

| 功能 | 实现方式 |
|------|---------|
| extraction（语义提取） | `/graphify` Skill 工具，不支持 CLI |
| query（图谱查询） | `graphify query "..."` CLI 命令 |
| MCP server | `python3 -m graphify.serve`（需 `pip install mcp`） |
| git hook | `graphify hook install`（仅处理代码文件 AST，不处理 .md） |

## Key Technical Decisions

- **编排师不查图谱**：星型拓扑中编排师仅调度，职责单一
- **graphify MCP（C1）**：顺序调用并发安全，graphify 原生支持
- **图谱优先（B）**：单一真相源，强制同步是质量门禁
- **两层同步模型**：代码文件 → git hook 自动 AST；.md 文档 → 手动 `/graphify` Skill

## Open Questions

### Resolved During Planning

- mcp_config.json 消费者 → 各 Phase Agent 在执行前连接 MCP 查询
- templates/scene/ 解析粒度 → 完整结构化解析（场景模板是交付物格式基准）
- git hook 同步范围 → 仅代码文件（.md 不在 hook 处理范围内）

### Deferred to Implementation

- 图谱版本管理：同步状态追踪方式待定
- 审计追踪：图谱查询记录格式和持久化方式待定

## Implementation Units

- [x] **Unit 1: 安装 MCP 包** ✅

**Goal:** 解除 graphify MCP server 的依赖阻塞

**Requirements:** R1

**Dependencies:** 无

**Files:**
- Modify: `graphify-out/`（验证用）

**Approach:**
执行 `pip install mcp`，然后验证 `python3 -m graphify.serve graphify-out/graph.json` 可正常启动。

**Verification:**
`python3 -m graphify.serve graphify-out/graph.json --help` 无报 `ModuleNotFoundError: mcp`

- [x] **Unit 2: 图谱扩展 — rules/ 目录** ✅ (309→344 nodes, 318→367 edges)

**Goal:** 将 `rules/` 目录纳入图谱，覆盖所有规则文件

**Requirements:** R2, R3

**Dependencies:** Unit 1

**Files:**
- Modify: `graphify-out/graph.json`（增量更新）

**Approach:**
调用 `/graphify` Skill，path=`rules/`，mode=`--update`（增量）。

**Verification:**
图谱节点数从 ~92 增长到 ~200-300，新增 edges 连接 rules/ 与现有 knowledge/ 节点

- [x] **Unit 3: 图谱扩展 — agents/ 目录** ✅

**Goal:** 将 `agents/orchestrator/roles/` 纳入图谱

**Requirements:** R2, R3

**Dependencies:** Unit 1

**Files:**
- Modify: `graphify-out/graph.json`（增量更新）

**Approach:**
调用 `/graphify` Skill，path=`agents/orchestrator/roles/`，mode=`--update`（增量）。

**Verification:**
图谱覆盖编排师角色定义和各 Phase Agent 角色定义 (35 nodes, 63 edges added)

- [x] **Unit 4: 创建 mcp_config.json** ✅ (mcp_config.json created)

**Goal:** 配置文件供各 Phase Agent 连接 graphify MCP server

**Requirements:** R1

**Dependencies:** Unit 1

**Files:**
- Create: `mcp_config.json`

**Approach:**
创建标准 MCP 配置文件，command=`python3`，args=`["-m", "graphify.serve", "graphify-out/graph.json"]`。

**Verification:**
配置文件格式符合 Claude Code MCP 连接规范

- [x] **Unit 5: Phase Agent 改造（Phase 0）** ✅ (Step0-图谱查询.md created + 主索引 updated)

**Goal:** 改造 Phase 0 执行文档，增加图谱查询步骤

**Requirements:** R1, R5

**Dependencies:** Unit 4

**Files:**
- Modify: `agents/orchestrator/phases/Phase0/Step2-合规审核.md`（或其他 Phase 0 执行文档）

**Approach:**
在 Phase 0 执行流程的最前面插入图谱查询步骤：通过 mcp_config.json 连接 MCP server → 查询合规规则 → 获取禁用词正则和检查清单 → 继续原有执行流程。

**Pattern to follow:**
设计文档 Step 4 示例格式。

**Verification:**
Phase 0 执行文档包含 MCP 连接和图谱查询步骤

- [x] **Unit 6: Phase Agent 改造（Phase 1 / 1.5 / 2a / 2b）** ✅ (Step0-图谱查询.md + 主索引 created for all 4 phases)

**Goal:** 改造其余 Phase 执行文档

**Requirements:** R1, R5

**Dependencies:** Unit 4

**Files:**
- Modify: `agents/orchestrator/phases/Phase1/`
- Modify: `agents/orchestrator/phases/Phase1.5/`
- Modify: `agents/orchestrator/phases/Phase2a/`
- Modify: `agents/orchestrator/phases/Phase2b/`

**Approach:**
每个 Phase 按关键节点强制查询表执行图谱查询步骤改造。

**Pattern to follow:**
Phase 0 改写模式（Unit 5）

**Verification:**
5 个 Phase 的执行文档均包含图谱查询步骤

- [x] **Unit 7: Git Hook 安装** ✅ (post-commit + post-checkout installed)

**Goal:** 代码文件变更自动触发 AST 增量提取

**Requirements:** R3

**Dependencies:** 无

**Files:**
- Create: `.git/hooks/post-commit`（通过 hook 命令安装）
- Create: `.git/hooks/post-checkout`（通过 hook 命令安装）

**Approach:**
执行 `graphify hook install`。注意：此 hook 仅处理代码文件（.py .ts 等）的 AST 增量提取，不处理 .md 文档。

**Verification:**
`graphify hook status` 显示 post-commit 和 post-checkout 已安装

## System-Wide Impact

- **orchestrate.sh**：不直接启动 MCP server（各 Agent 各自连接）
- **Phase Agent 执行文档**：新增图谱查询前置步骤，Agent 执行流程变化
- **graphify-out/graph.json**：持续增长（rules/ agents/ templates/ 逐步纳入）
- **mcp_config.json**：各 Agent 的 MCP 连接配置

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| mcp 包安装失败 | 检查 Python 环境，确认 pip 可用 |
| 图谱扩展后节点冲突 | 增量模式 + dedup 自动处理 |
| Agent 不使用 MCP 查询 | 强制规则：图谱同步后才能执行 Phase |
| git hook 污染 commit | hook 有 `|| true`，失败不阻断 commit |

## Documentation / Operational Notes

- graphify hook 需在每个 clone 后的机器上重新安装
- .md 文档变更不在 hook 范围内，需手动同步
- 图谱准确性定期核查：通过 `graphify query "X 场景的运镜规则是什么？"` 对比源文件

## Sources & References

- **Origin design doc:** `/Users/godxu/.gstack/projects/animation-v3/godxu-main-design-knowledge-graph-orchestrate-20260417-144028.md`
- graphify skill: `~/.claude/skills/graphify/SKILL.md`
- Existing graph: `graphify-out/graph.json`（92 nodes）
- orchestrate.sh: `scripts/orchestrate.sh`
- orchestrator role: `agents/orchestrator/orchestrator.md`
