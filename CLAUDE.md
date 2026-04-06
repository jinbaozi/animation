# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **AI Animation Drama (AI漫剧) Production Rules System** - a modular rules and templates library for AI-driven animated drama creation.

## Directory Structure

```
animation-v3/
│
├── bak/                          # Backup of original role files (before agents/ migration)
│   ├── 00-角色编排总规范.md
│   ├── 01-AI内容总导演-角色职责规范.md
│   ├── 02-AI美术技术总监-角色职责规范.md
│   ├── 03-AI镜头序列设计师-角色职责规范.md
│   └── 04-AI品控合规官-角色职责规范.md
│   # Note: 05-编排师-角色职责规范.md → agents/orchestrator/orchestrator.md
│
├── rules/                        # Modular rules (load before tasks)
│   ├── 00-index.md               # Rules index
│   ├── 审美偏好.md               # User aesthetic preference
│   ├── 风格一致性.md             # Style consistency + forbidden words
│   ├── 视频格式.md               # VideoPrompt format spec
│   ├── 运镜知识.md               # Cinematography knowledge
│   ├── 质量门禁.md               # Quality gate system
│   ├── 双轨生成.md               # Chinese/English dual-track rules
│   ├── 输出验证.md               # Output verification checklist
│   ├── 抖音合规.md               # Douyin compliance rules
│   ├── 影视质感生成规范.md        # Film quality generation spec
│   ├── 审核智能体设计规范.md      # Audit agent design spec
│   ├── AI审核智能体设计规范.md    # AI audit agent design spec
│   └── 风格/                     # Style-specific reference
│       ├── 国风动漫.md
│       ├── 西方神话.md
│       ├── 拟真人.md
│       ├── 中国奇幻.md
│       └── 3D.md
│
├── templates/                    # Templates organized by category
│   ├── 00-index.md               # Template index
│   ├── scene/                    # 8 scene type templates
│   │   ├── 对话场景序列.md
│   │   ├── 动作戏序列.md
│   │   ├── 情感戏序列.md
│   │   ├── 悬疑惊悚序列.md
│   │   ├── 蒙太奇转场.md
│   │   ├── 独白内心戏序列.md
│   │   ├── 奇幻视觉奇观序列.md
│   │   └── 日常氛围治愈系序列.md
│   ├── knowledge/                # Hollywood reference knowledge
│   │   ├── 09-好莱坞运镜库.md
│   │   ├── 12-好莱坞剪辑语言.md
│   │   ├── 13-好莱坞导演技法.md
│   │   ├── 13-好莱坞光影体系.md
│   │   ├── 13-好莱坞配音体系.md
│   │   ├── Seedance2导演级运镜库.md
│   │   └── Seedance2提示词与运镜完全指南.md
│   ├── output/                   # Output templates
│   │   ├── 合规预审报告.md
│   │   ├── 场景资产卡.md
│   │   ├── 人物四视图Prompt包.md
│   │   └── VideoPrompt包.md
│   └── reference/                # Reference materials
│       ├── 场景基准模版.md
│       ├── 人物基准模版.md
│       ├── 古风国漫Prompt锚点与负面附录.md
│       ├── 国漫风格关键词库.md
│       └── 古风服饰配色指南.md
│
├── docs/                         # Execution documentation
│   ├── 路径规范.md               # Path conventions (this file)
│   ├── 快速入门指南.md           # Quick start guide
│   ├── 编排师操作手册.md          # Orchestrator manual
│   ├── 术语表.md                 # Glossary
│   ├── output目录结构规范.md      # Output structure spec
│   ├── 阻塞问题清单模板.md        # Block issue template
│   └── knowledge/                # Project knowledge base
│       ├── 影视摄影机镜头提示词知识库.md
│       └── AI动作戏视频提示词设计指南.md
│
├── examples/                     # Example projects
│   └── 01-完整示例/              # Complete end-to-end example
│
├── agents/                       # AI Agent definitions
│   ├── orchestrator/             # Orchestrator (星型拓扑中枢)
│   │   ├── orchestrator.md      # Main orchestrator role definition
│   │   ├── compliance/          # Phase 0 execution docs
│   │   │   └── Phase0/
│   │   ├── director/             # Phase 1 execution docs
│   │   │   └── Phase1/
│   │   ├── shot-designer/       # Phase 1.5 execution docs
│   │   │   └── Phase1.5/
│   │   ├── art-director/        # Phase 2 execution docs
│   │   │   └── Phase2/
│   │   │       ├── Phase2a/     # Character 4-view prompts
│   │   │       └── Phase2b/     # VideoPrompt generation
│   │   ├── Seedance2/          # Seedance 2.0 techniques
│   │   │   ├── Seedance2-基础理论.md
│   │   │   ├── Seedance2-禁止清单.md
│   │   │   ├── Seedance2-模板示例.md
│   │   │   ├── Seedance2-NotebookLM补充.md
│   │   │   └── Seedance2提示词技巧大全.md
│   │   └── execution/           # Shared execution docs
│   │       └── *.md
│   │
│   └── audit/                   # Audit agent (独立审核系统)
│       ├── audit-agent.md       # Audit agent orchestrator
│       ├── dimensions/          # 8 audit dimension modules
│       │   ├── 01-character-consistency.md
│       │   ├── 02-scene-consistency.md
│       │   ├── 03-action-coherence.md
│       │   ├── 04-narrative-logic.md
│       │   ├── 05-expression-precision.md
│       │   ├── 06-dialogue-interaction.md
│       │   ├── 07-cinematography.md
│       │   └── 08-world-building.md
│       ├── templates/           # Audit report templates
│       │   ├── audit-report.md
│       │   └── score-sheet.md
│       ├── rules/               # Audit rules engine
│       │   └── audit-rules.md
│       └── Phase3/              # Phase 3 execution docs
│           ├── Phase3-主索引.md
│           ├── Step1-产物收集.md
│           ├── Step2-规则预检.md
│           ├── Step3-LLM细审.md
│           └── Phase3-报告生成.md
│
└── scripts/                     # Automation scripts
    ├── orchestrate.sh            # Orchestrator trigger script
    └── audit-agent.sh            # Audit trigger script
```

## Architecture

### 5 Roles (星型拓扑)

| Role | Entry Point | Phase | Core Responsibility |
|------|-------------|-------|---------------------|
| 编排师 | `agents/orchestrator/orchestrator.md` | - | Coordinator (用户 ↔ 执行角色) |
| AI品控合规官 | `bak/04-AI品控合规官-角色职责规范.md` | Phase 0 | Compliance review |
| AI内容总导演 | `bak/01-AI内容总导演-角色职责规范.md` | Phase 1 | Script + storyboard |
| AI镜头序列设计师 | `bak/03-AI镜头序列设计师-角色职责规范.md` | Phase 1.5 | Scene sequence design |
| AI美术技术总监 | `bak/02-AI美术技术总监-角色职责规范.md` | Phase 2a/2b | Visual assets + prompts |

> Note: Role definition files are backed up in `bak/`. Active role definitions are in `agents/orchestrator/{submodule}/`.

### Phase Execution Flow

```
用户提交任务
    │
    ▼
Phase 0（品控合规官）→ Phase 1（内容总导演）→ Phase 1.5（镜头序列设计师）
                                                              │
                                                              ▼
                                              Phase 2a（美术技术总监）
                                                              │
                                                              ▼
                                              Phase 2b（美术技术总监）→ 完成
```

## Rules System

**Load rules before specific tasks:**

| Rule | When to Load |
|------|-------------|
| `审美偏好.md` | Before generating character 4-view prompts |
| `风格一致性.md` | Before generating any prompt (check forbidden word regex) |
| `视频格式.md` | Before generating VideoPrompts |
| `运镜知识.md` | Before designing shot sequences |
| `双轨生成.md` | Before generating VideoPrompts (Chinese + English) |
| `输出验证.md` | Before delivery/verification |

### Critical Rules

1. **Style Consistency (MANDATORY)**
   - If project is "国风动漫" → NEVER use "古风写实", "影视质感", etc.
   - Forbidden regex: `(?i)(影视|电影|摄像|胶片|摄影|古风写实|写实CG|游戏CG|影视质感|影视级|电影级)`

2. **User Aesthetic: 病弱古典美人**
   - Preferred: 鹅蛋脸, 病态苍白, 杏核眼, 纤细单薄
   - Forbidden: 瓜子脸, 健康红润, 大眼睛, 丰满

3. **Character 4-View Format (MANDATORY)**
   - Must have exactly 4 views: 正面全身, 侧面全身, 背面全身, 面部特写
   - All must be full body shots on pure white background
   - Every character including 龙套 must have 4-view prompts

4. **VideoPrompt Format**
   - Time segments: 0-3s | 3-6s | 6-9s | 9-12s | 12-15s
   - Each segment: 动作/内心活动/台词 (pick one based on scene type) + 镜头

5. **Dual-Track Generation**
   - Chinese + English prompts must be generated simultaneously
   - Stored in parallel directories

## 8 Scene Types

| Scene | Template | Characteristics |
|-------|----------|-----------------|
| 对话场景 | `templates/scene/对话场景序列.md` | Shot-reverse-shot, axis management |
| 动作戏 | `templates/scene/动作戏序列.md` | Fighting, chase sequences |
| 情感戏 | `templates/scene/情感戏序列.md` | Love, sadness, conflict |
| 悬疑惊悚 | `templates/scene/悬疑惊悚序列.md` | Tension, jump scares |
| 蒙太奇转场 | `templates/scene/蒙太奇转场.md` | Time compression |
| 独白内心戏 | `templates/scene/独白内心戏序列.md` | Internal thoughts |
| 奇幻视觉奇观 | `templates/scene/奇幻视觉奇观序列.md` | Magic, transformation |
| 日常氛围治愈系 | `templates/scene/日常氛围治愈系序列.md` | Everyday life, sensory |

## Key Constraints

- **No pronouns**: Must use actual character names (她/他 forbidden)
- **Shot count formula**: `target_shots ≈ ceil(total_word_count / 80)`
- **No content omission**: Thousands of words cannot result in only 2-3 sequences
- **Sequences must document 落幅→起幅 continuity**

## User Guidance

### For New Users

1. Read `docs/快速入门指南.md` first
2. Prepare your novel in .txt or .md format
3. Submit to the Orchestrator (编排师)
4. Follow Phase 0 → 1 → 1.5 → 2a → 2b
5. Receive final VideoPrompt

### Path Conventions

- Role files (backup): `bak/` (original role definitions before migration)
- Orchestrator entry: `agents/orchestrator/orchestrator.md`
- Audit agent entry: `agents/audit/audit-agent.md`
- Rules: `rules/` directory
- Templates: `templates/` directory
- Execution docs: `agents/orchestrator/{submodule}/PhaseX/`
- Examples: `examples/` directory

**Do NOT use**:
- `01-角色/` (doesn't exist)
- `02-基准模版/` (doesn't exist)
- `docs/execution/` (migrated to `agents/orchestrator/`)
- `rules/Seedance2/` (migrated to `agents/orchestrator/Seedance2/`)

See `docs/路径规范.md` for full path conventions.
