# Step 0: 图谱查询 — VideoPrompt 规则获取

> 执行角色：AI美术技术总监
> 所属 Phase：Phase 2b
> **强制步骤**：执行任何 VideoPrompt 生成前，必须先通过图谱查询获取规则
> **v2.0更新**：新增覆盖率≥80%要求、镜头优先级排序

---

## 0.1 连接 MCP Server

通过 `mcp_config.json` 连接 graphify MCP server。

---

## 0.2 强制查询 — Phase 2b 核心规则

**Query 1: VideoPrompt 格式**
```
查询：VideoPrompt 的标准格式是什么？时间分段有哪些要求？
```
**预期返回**：VideoPrompt 格式规范：
- 时间分段：0-3s | 3-6s | 6-9s | 9-12s | 12-15s
- 每段格式：动作/内心活动/台词（根据场景类型选择）+ 镜头 + 光线

**Query 2: 覆盖率要求（v2.0新增）**
```
查询：Phase 2b VideoPrompt生成的覆盖率要求是多少？
```
**预期返回**：
- 核心镜头覆盖率 ≥80%
- 镜头优先级：P0核心叙事镜头→P0情绪高潮镜头→P1奇幻视觉奇观→P1动作戏关键帧

**Query 3: 双轨生成规则**
```
查询：中英双轨生成规则是什么？中文版和英文版有什么对应要求？
```
**预期返回**：双轨生成规则（来自 rules/双轨生成.md v3.0）

**Query 4: 禁止行为清单**
```
查询：Seedance2 VideoPrompt 生成中，有哪些禁止行为？
```
**预期返回**：禁止行为清单中的所有条目：
- 禁止使用人称代词
- 禁止模糊运镜描述
- 禁止手部精细动作
- 禁止同屏超过2个主要人物
- 禁止跳过动作三阶段
- 禁止词：cinematic, film, photorealistic 等

**Query 5: Negative Prompt 正确写法**
```
查询：VideoPrompt 中 Negative Prompt 的正确写法是什么？
```
**预期返回**：Negative Prompt 规范（来自 rules/Seedance2/Seedance2-NotebookLM补充.md）

---

## 0.3 图谱溯源记录

```markdown
## 图谱查询溯源记录

| 查询项 | 来源节点 | source_location |
|--------|---------|----------------|
| VideoPrompt格式 | 视频格式 | rules/视频格式.md |
| 覆盖率要求 | 覆盖率要求 | agents/orchestrator/phases/Phase2b/Step3-VideoPrompt生成.md |
| 双轨生成规则 | 双轨生成规则 | rules/双轨生成.md |
| 禁止行为清单 | 禁止行为清单 | rules/Seedance2/Seedance2-禁止清单.md |
| Negative Prompt写法 | Negative Prompt正确写法 | rules/Seedance2/Seedance2-NotebookLM补充.md |
```

---

## 0.4 进入 Step 1

完成图谱查询后，携带查询结果进入 Step 1: 接收准备。
