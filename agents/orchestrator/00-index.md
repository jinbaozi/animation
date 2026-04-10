# 编排智能体索引

> 版本：v1.0 | 日期：2026-04-06
> 作用：按 Phase 查找执行文档，确保工作流正确执行。

---

## Phase 执行顺序

```
Phase 0（品控合规官）→ Phase 1（内容总导演）→ Phase 1.5（镜头序列设计师）
                                                              │
                                                              ▼
                                              Phase 2a（美术技术总监）
                                                              │
                                                              ▼
                                              Phase 2b（美术技术总监）→ 完成
```

---

## 执行文档索引

### Phase 0：品控合规官

| 文档 | 位置 |
|------|------|
| 主索引 | `phases/Phase0/Phase0-主索引.md` |
| 质量标准 | `phases/Phase0/Phase0-质量标准.md` |
| Step1-接收解析 | `phases/Phase0/Step1-接收解析.md` |
| Step2-合规审核 | `phases/Phase0/Step2-合规审核.md` |
| Step3-评分标准 | `phases/Phase0/Step3-评分标准.md` |
| Step4-问题分类 | `phases/Phase0/Step4-问题分类.md` |
| Step5-生成报告 | `phases/Phase0/Step5-生成报告.md` |

### Phase 1：内容总导演

| 文档 | 位置 |
|------|------|
| 主索引 | `phases/Phase1/Phase1-主索引.md` |
| 质量标准 | `phases/Phase1/Phase1-质量标准.md` |
| Step1-接收准备 | `phases/Phase1/Step1-接收准备.md` |
| Step2-剧本改编 | `phases/Phase1/Step2-剧本改编.md` |
| Step3-分镜设计 | `phases/Phase1/Step3-分镜设计.md` |

### Phase 1.5：镜头序列设计师

| 文档 | 位置 |
|------|------|
| 主索引 | `phases/Phase1.5/Phase1.5-主索引.md` |
| 质量标准 | `phases/Phase1.5/Phase1.5-质量标准.md` |
| Step1-镜头序列设计 | `phases/Phase1.5/Step1-镜头序列设计.md` |
| Step2-序列衔接表 | `phases/Phase1.5/Step2-序列衔接表.md` |

### Phase 2a：美术技术总监（人物四视图）

| 文档 | 位置 |
|------|------|
| 主索引 | `phases/Phase2/Phase2-主索引.md` |
| 四视图模板 | `phases/Phase2a/四视图模板.md` |
| 质量标准 | `phases/Phase2a/Phase2a-质量标准.md` |
| Step1-人物分析 | `phases/Phase2a/Step1-人物分析.md` |
| Step2-四视图生成 | `phases/Phase2a/Step2-四视图生成.md` |
| Step3-场景资产卡 | `phases/Phase2a/Step3-场景资产卡.md` |

### Phase 2b：美术技术总监（VideoPrompt）

| 文档 | 位置 |
|------|------|
| 主索引 | `phases/Phase2/Phase2-主索引.md` |
| 双轨生成规则 | `phases/Phase2b/双轨生成规则.md` |
| 质量标准 | `phases/Phase2b/Phase2b-质量标准.md` |
| VideoPrompt模板 | `phases/Phase2b/VideoPrompt模板.md` |
| Step1-接收准备 | `phases/Phase2b/Step1-接收准备.md` |
| Step2-时间分段 | `phases/Phase2b/Step2-时间分段.md` |
| Step3-VideoPrompt生成 | `phases/Phase2b/Step3-VideoPrompt生成.md` |

---

## 技术指南

| 文档 | 位置 |
|------|------|
| Seedance2 基础理论 | `rules/Seedance2/Seedance2-基础理论.md` |
| Seedance2 禁止清单 | `rules/Seedance2/Seedance2-禁止清单.md` |
| Seedance2 模板示例 | `rules/Seedance2/Seedance2-模板示例.md` |
| Seedance2 NotebookLM补充 | `rules/Seedance2/Seedance2-NotebookLM补充.md` |
| Seedance2 提示词技巧大全 | `rules/Seedance2/Seedance2提示词技巧大全.md` |

---

## 入口文件

| 文件 | 位置 | 说明 |
|------|------|------|
| 编排师职责 | `orchestrator.md` | 编排智能体主入口 |
| 本索引 | `00-index.md` | 本文档 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-06 | 初始版本，从 docs/路径规范.md 提取 |
