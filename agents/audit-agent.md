# AI审核智能体 — 主编排器

> 状态：v1.0 | 版本：v2.0 | 日期：2026-04-06
> **触发时机**：Phase 2b完成后自动触发

---

## 1. 核心定位

**角色类型**：Claude Code专用子智能体（项目级别）

**核心价值**：
- 独立于品控合规官的第三方深度审核
- 混合架构：规则引擎预筛 + LLM细审
- 8维度结构化审核报告

---

## 2. 触发条件

### 自动触发
当检测到 `output/{项目名}/` 目录存在时，自动执行审核。

### 手动触发
```
./audit-agent.sh --phase=final --input=output/{项目名}/ --output=review/{项目名}-audit-{日期}.md
```

---

## 3. 输入产物

| 产物 | 位置 | 审核维度 |
|------|------|---------|
| 剧本.md | output/{项目名}/ | D4 |
| 基础分镜执行表.md | output/{项目名}/ | D4 |
| 增强分镜执行表.md | output/{项目名}/ | D3/D5/D6/D7 |
| 序列衔接与继承表.md | output/{项目名}/ | D3 |
| 人物清单.md | output/{项目名}/ | D1 |
| 人物四视图Prompt包.md | output/{项目名}/ | D1/D8 |
| 场景清单.md | output/{项目名}/ | D2 |
| 场景资产卡.md | output/{项目名}/ | D2 |
| VideoPrompt包.md | output/{项目名}/ | D1-D8（全维度）|

---

## 4. 执行流程

### Phase 1: 产物收集
1. 检测output/{项目名}/目录
2. 读取所有产物文件
3. 构建审核上下文

### Phase 2: 规则引擎预检（8维度并行）
- D1 人物一致性：特征关键词检测
- D2 场景一致性：场景标签 + 道具追踪
- D3 动作连贯性：时间戳 + 物理关键词
- D4 剧情符合度：任务标签 + 伏笔检测
- D5 表情精准度：表情关键词 + AU动作单元
- D6 对戏互动：站位标签 + 视线方向
- D7 运镜专业度：景别/运镜参数范围
- D8 世界观合规：违禁词正则 + 世界观标签

### Phase 3: LLM细审
- 规则引擎结果为"通过"：仅验证
- 规则引擎结果为"疑问"：全维度细审
- 规则引擎发现P0：直接输出P0报告

### Phase 4: 报告汇总
1. 汇总8维度评分
2. 按P0/P1/P2分级问题
3. 生成修复建议
4. 输出到review/目录

---

## 5. 加载模块

| 模块 | 路径 |
|------|------|
| D1 人物一致性 | agents/audit/dimensions/01-character-consistency.md |
| D2 场景一致性 | agents/audit/dimensions/02-scene-consistency.md |
| D3 动作连贯性 | agents/audit/dimensions/03-action-coherence.md |
| D4 剧情符合度 | agents/audit/dimensions/04-narrative-logic.md |
| D5 表情精准度 | agents/audit/dimensions/05-expression-precision.md |
| D6 对戏互动 | agents/audit/dimensions/06-dialogue-interaction.md |
| D7 运镜专业度 | agents/audit/dimensions/07-cinematography.md |
| D8 世界观合规 | agents/audit/dimensions/08-world-building.md |
| 规则引擎 | agents/audit/rules/audit-rules.md |
| 报告模板 | agents/audit/templates/audit-report.md |

---

## 6. 输出规范

### 输出位置
`review/{项目名}-audit-{YYYY-MM-DD}.md`

### 评分标准

| 评分 | 等级 |
|------|------|
| 9-10 | 优秀 |
| 7-8 | 良好 |
| 5-6 | 合格 |
| 3-4 | 不合格 |
| 0-2 | 阻断性 |

### 问题分级

| 等级 | 含义 |
|------|------|
| P0 | 阻断性，必须修复 |
| P1 | 显著瑕疵，建议修复 |
| P2 | 优化项，可选修复 |

---

## 7. 协同关系

```
Phase 0 → Phase 1 → Phase 1.5 → Phase 2a → Phase 2b
    │                                      │
    └───────── AI品控合规官 ────────────────┘
                                              │
                          ┌───────────────────┘
                          ▼
                    独立审核智能体（自动触发）
                          │
                          ▼
                    review/审核报告
```
