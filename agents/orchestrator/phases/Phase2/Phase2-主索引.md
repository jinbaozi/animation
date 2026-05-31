# Phase 2 - 美术技术总监执行指令

> 版本：v1.0.0
> 创建日期：2026-04-04
> 执行角色：AI美术技术总监
> 细分：Phase 2a（人物+场景）→ Phase 2b（VideoPrompt）

---

## 1. 执行概述

| Phase | 执行角色 | 输入 | 输出 | 时长 |
|-------|---------|------|------|------|
| Phase 2a | AI美术技术总监 | Shot IR + 增强分镜执行表 + 序列衔接表 | VisualAnchorIR + 人物资产卡 + 场景资产卡 + 人物四视图Prompt包 | 约60分钟 |
| Phase 2b | AI美术技术总监 | VisualAnchorIR + ShotIR + 人物/场景资产卡 | PromptExportIR + VideoPrompt包 + Tool Export | 约60分钟 |

---

## 2. Phase 2a - 人物四视图 + 场景资产

### 目录结构

```
Phase2a/
├── Step1-人物分析.md      # 人物识别与视觉档案建立
├── Step2-四视图生成.md    # 四视图Prompt生成规则
├── Step3-场景资产卡.md    # 场景资产卡生成
├── 四视图模板.md          # 四视图Prompt模板
└── Phase2a-质量标准.md    # 质量检查清单
```

### 输入/输出映射

| 输入 | 输出 |
|------|------|
| 人物清单.md | 人物资产卡.md |
| 场景清单.md | 场景资产卡.md |
| ShotIR.md | VisualAnchorIR.md |
| 人物清单.md | 人物四视图Prompt包.md |

---

## 3. Phase 2b - VideoPrompt生成

### 目录结构

```
Phase2b/
├── Step1-接收准备.md          # 接收Phase 2a输出及规则文件
├── Step2-时间分段.md          # 5秒一段时间轴规范
├── Step3-VideoPrompt生成.md   # VideoPrompt生成流程
├── 双轨生成规则.md            # 中英双轨生成规范
├── VideoPrompt模板.md         # VideoPrompt完整模板
└── Phase2b-质量标准.md        # 质量检查清单
```

### 输入/输出映射

| 输入 | 输出 |
|------|------|
| VisualAnchorIR.md | PromptExportIR.md |
| ShotIR.md | VideoPrompt包-中文版.md |
| 人物资产卡.md | VideoPrompt包-英文版.md |
| 场景资产卡.md | ToolExport/ |
| rules/审美偏好.md | |
| rules/风格一致性.md | |
| rules/双轨生成.md | |
| rules/视频格式.md | |

---

## 4. 输出文件清单

| Phase | 文件 | 格式 | 必填 |
|-------|------|------|------|
| 2a | VisualAnchorIR.md | Markdown | 是 |
| 2a | 人物资产卡.md | Markdown | 是 |
| 2a | 人物四视图Prompt包.md | Markdown | 是 |
| 2a | 场景资产卡.md | Markdown表格 | 是 |
| 2b | PromptExportIR.md | Markdown | 是 |
| 2b | VideoPrompt包-中文版.md | Markdown | 是 |
| 2b | VideoPrompt包-英文版.md | Markdown | 是 |

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
