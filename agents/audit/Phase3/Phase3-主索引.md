# Audit Gate: VideoPrompt 交付审核

> 状态：v2.0 | 日期：2026-05-31
> **执行时机**：Phase 2b完成后，最终交付前
> 路径兼容：当前仍位于 `agents/audit/Phase3/`，但流程定位是 Audit Gate，不属于成片 Phase 3。

---

## 概述

Audit Gate 负责对 IR、工具导出和三类核心交付物进行系统性质量审核，确保符合质量门禁标准后方可进入 `99-最终交付物/`。

## 执行前确认

- [ ] Phase 2b 已完成
- [ ] output/{项目名}/ 目录存在
- [ ] 包含 `VideoPrompt包`、`人物资产卡`、`场景资产卡`

### 必需产物清单

| 产物 | 位置 |
|------|------|
| project-manifest.md | `00-项目配置/` |
| StoryIR.md | `02-Phase1-剧本分镜/` |
| ShotIR.md | `03-Phase1.5-镜头序列/` |
| VisualAnchorIR.md | `04-Phase2a-四视图/` |
| 人物资产卡.md | `04-Phase2a-四视图/` |
| 场景资产卡.md | `04-Phase2a-四视图/` |
| PromptExportIR.md | `05-Phase2b-Prompt/` |
| VideoPrompt包-中文版.md | `05-Phase2b-Prompt/` |
| VideoPrompt包-英文版.md | `05-Phase2b-Prompt/` |

---

## 执行方式

### 手动触发
```bash
./scripts/audit-agent.sh --phase=final --input=output/{项目名}/ --output=review/{项目名}-audit-$(date +%Y-%m-%d).md
```

### 自动触发
当检测到 Phase 2b 完成标志文件存在时，自动执行审核。

---

## 子模块索引

| 模块 | 文件 | 说明 |
|------|------|------|
| Step1 | `Step1-产物收集.md` | 读取所有产物文件，构建审核上下文 |
| Step2 | `Step2-规则预检.md` | 8维度并行规则引擎预检 |
| Step3 | `Step3-LLM细审.md` | 对疑问项进行深度审核 |
| 报告 | `Phase3-报告生成.md` | 汇总评分、问题分级、生成修复建议 |

---

## 审核结果等级

| 等级 | 分数 | 说明 |
|------|------|------|
| 优秀 | 9-10 | 可直接使用 |
| 良好 | 7-8 | 微调后可用 |
| 合格 | 5-6 | 需修复P0/P1 |
| 不合格 | 3-4 | 需重大修改 |
| 阻断性 | 0-2 | 需重新生成 |

## 问题分级

- **P0**：必须修复，否则阻断
- **P1**：建议修复
- **P2**：可选修复
