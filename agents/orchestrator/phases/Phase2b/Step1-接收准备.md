# Step 1: 接收与准备

> 执行角色：AI美术技术总监
> 所属阶段：Phase 2b
> 版本：v1.1
> **v1.1更新**：扩展输入材料清单，增加默会知识和示例

---

## 1. 接收清单

### Phase 2a 输出
- [ ] VisualAnchorIR.md
- [ ] 人物资产卡.md
- [ ] 人物四视图Prompt包.md
- [ ] 场景资产卡.md

### Phase 1.5 输出
- [ ] ShotIR.md
- [ ] 增强分镜执行表.md（shot数量以 project-manifest.md 为准）
- [ ] 序列衔接与继承表.md

### Phase 1 输出
- [ ] 人物清单.md
- [ ] 场景清单.md

---

## 2. 规则文件阅读（必须全部阅读）

### 核心规则
0. [ ] `rules/中间表示规范.md` — Prompt Export IR 与 Tool Export 契约
1. [ ] `rules/审美偏好.md`
2. [ ] `rules/风格一致性.md` — 禁用词、风格锚点
3. [ ] `rules/双轨生成.md` — 中英双轨生成规范
4. [ ] `rules/视频格式.md` — 时间分段规则

### 运镜与场景
5. [ ] `rules/运镜知识.md` — 运镜术语规范

### 工具技巧
6. [ ] `agents/orchestrator/phases/Phase2b/Seedance2提示词技巧.md` — Seedance2专有技巧
7. [ ] `agents/orchestrator/phases/Phase2b/VideoPrompt模板.md` — 优秀示例

### 默会知识（必须理解）
8. [ ] `.claude/skills/polanyi-tacit-knowledge/knowledge/镜头序列情绪落幅设计-默会知识.md`
9. [ ] `.claude/skills/polanyi-tacit-knowledge/knowledge/对话场景镜头语言-默会知识.md`
10. [ ] `.claude/skills/polanyi-tacit-knowledge/knowledge/角色情绪节奏把控-默会知识.md`

### 参考知识库
11. [ ] `templates/knowledge/13-好莱坞运镜库.md`
12. [ ] `templates/knowledge/13-好莱坞光影体系.md`

---

## 3. 准备检查

- [ ] Phase 2a 输出文件齐全（VisualAnchorIR + 人物资产卡 + 场景资产卡 + 人物四视图）
- [ ] ShotIR 与增强分镜执行表已阅读（shot数量与 project manifest 一致）
- [ ] 所有规则文件已阅读并理解
- [ ] 默会知识已理解（镜头语言、情绪节奏、落幅设计）
- [ ] 禁用词清单已确认
- [ ] 格式A模板已理解（带基本信息表的VideoPrompt格式）

---

## 4. 输出目录确认

确认 Phase 2b 输出目录结构：

```
output/{项目名}/05-Phase2b-Prompt/
├── PromptExportIR.md
├── VideoPrompt包-中文版.md    # 中文提示词
├── VideoPrompt包-英文版.md    # English prompts
└── ToolExport/               # 按目标工具可选拆分
```

**注意**：中英文分开存放，不混在同一文件。
