# 输出目录结构规范

> 版本：v2.0.0
> 创建日期：2026-04-04
> 更新日期：2026-05-31

---

## 1. 项目输出根目录

每个AI动画项目应创建独立的输出目录，命名格式：

```
output/
└── {项目名}_{日期}/
```

示例：
```
output/
└── 三生三世十里桃花_20260404/
```

---

## 2. Phase 输出子目录结构

### 2.1 标准结构

```
{项目名}_{日期}/
├── 00-项目配置/
│   └── project-manifest.md
│
├── 00-原始素材/
│   ├── 原始小说.txt
│   └── 用户需求文档.md
│
├── 01-Phase0-合规预审/
│   └── 合规预审报告.md
│
├── 02-Phase1-剧本分镜/
│   ├── StoryIR.md
│   ├── 剧本.md
│   ├── 基础分镜执行表.md
│   ├── 人物清单.md
│   └── 场景清单.md
│
├── 03-Phase1.5-镜头序列/
│   ├── ShotIR.md
│   ├── 增强分镜执行表.md
│   └── 序列衔接与继承表.md
│
├── 04-Phase2a-四视图/
│   ├── VisualAnchorIR.md
│   ├── 人物资产卡.md
│   ├── 场景资产卡.md
│   ├── 人物四视图Prompt包.md
│   └── 四视图预览/ (如有生成的图片)
│
├── 05-Phase2b-Prompt/
│   ├── PromptExportIR.md
│   ├── VideoPrompt包-中文版.md    # 中文提示词
│   ├── VideoPrompt包-英文版.md    # English prompts
│   └── ToolExport/               # 可选：Seedance2/即梦/中文审阅版拆分
│
├── 06-Audit-Gate/
│   ├── 审核报告.md
│   └── 返工问题清单.md (如有)
│
└── 99-最终交付物/
    ├── 完整VideoPrompt包-中文版.md
    ├── 完整VideoPrompt包-英文版.md
    ├── 人物资产卡.md
    ├── 场景资产卡.md
    ├── 资产清单.md
    └── 交付检查清单.md
```

**Phase 2b 目录说明**：
- 目录名：`05-Phase2b-Prompt`（不是`05-Phase2b-视频提示词`）
- 中英文分开存放，不混在同一文件
- 每个文件的 shot 数必须来自 `project-manifest.md` 和 `ShotIR.md`，不得硬编码固定数量

---

## 3. 文件命名规范

### 3.1 Phase 输出文件

| Phase | 文件名 | 说明 |
|-------|--------|------|
| G0 | `project-manifest.md` | 项目配置与交付范围 |
| Phase 0 | `合规预审报告.md` | 固定名称 |
| Phase 1 | `StoryIR.md` | 叙事事实源 |
| Phase 1 | `剧本.md` | 固定名称 |
| Phase 1 | `基础分镜执行表.md` | 固定名称 |
| Phase 1 | `人物清单.md` | 固定名称 |
| Phase 1 | `场景清单.md` | 固定名称 |
| Phase 1.5 | `ShotIR.md` | 镜头事实源 |
| Phase 1.5 | `增强分镜执行表.md` | 固定名称 |
| Phase 1.5 | `序列衔接与继承表.md` | 固定名称 |
| Phase 2a | `VisualAnchorIR.md` | 视觉一致性事实源 |
| Phase 2a | `人物资产卡.md` | 最终交付物之一 |
| Phase 2a | `场景资产卡.md` | 最终交付物之一 |
| Phase 2a | `人物四视图Prompt包.md` | 固定名称 |
| Phase 2b | `PromptExportIR.md` | 多工具导出唯一来源 |
| Phase 2b | `VideoPrompt包-中文版.md` | 中文提示词 |
| Phase 2b | `VideoPrompt包-英文版.md` | English prompts |
| Audit Gate | `审核报告.md` | 8维度审核报告 |

### 3.2 资源文件

```
# 人物资源
{角色名}_四视图_{序号}.png

# 场景资源
{场景名}_{序号}.png

# 视频资源
{项目名}_{日期}_v{版本号}.mp4
```

---

## 4. 版本控制

### 4.1 文件版本

每次重大修改创建新版本：
```
VideoPrompt包-中文版_v1.md
VideoPrompt包-中文版_v2.md
VideoPrompt包-中文版_v3.md
```

### 4.2 交付版本

最终交付文件添加 `_final` 后缀：
```
VideoPrompt包-中文版_final.md
```

---

## 5. 完整性检查

在进入下一 Phase 前，检查：

- [ ] 当前 Phase 所有输出文件存在
- [ ] 文件命名符合规范
- [ ] 内容格式符合模板要求
- [ ] 无占位符（TODO、TBD）残留
- [ ] 审核通过（如适用）
- [ ] 最终交付物包含 VideoPrompt包、人物资产卡、场景资产卡
- [ ] 所有数量来自 project manifest，不使用示例固定数量

---

## 6. 版本历史

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v2.0.0 | 2026-05-31 | 新增 G0、IR、Audit Gate，并将人物资产卡/场景资产卡列为最终交付物 |
| v1.1.0 | 2026-04-10 | Phase 2b目录改为中英文分开存放 |
| v1.0.0 | 2026-04-04 | 初始版本 |
