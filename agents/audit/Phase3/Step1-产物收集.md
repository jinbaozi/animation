# Step1: Audit Gate 产物收集

> Audit Gate 第一步

---

## 目标

读取所有产物文件，构建审核上下文。

## 执行步骤

### 1.1 确认产物存在

检查 output/{项目名}/ 目录下是否存在以下文件：

| 产物 | 文件名 |
|------|--------|
| 项目配置 | 00-项目配置/project-manifest.md |
| Story IR | 02-Phase1-剧本分镜/StoryIR.md |
| Shot IR | 03-Phase1.5-镜头序列/ShotIR.md |
| Visual Anchor IR | 04-Phase2a-四视图/VisualAnchorIR.md |
| 人物资产 | 04-Phase2a-四视图/人物资产卡.md |
| 场景资产 | 04-Phase2a-四视图/场景资产卡.md |
| Prompt Export IR | 05-Phase2b-Prompt/PromptExportIR.md |
| 中文 VideoPrompt | 05-Phase2b-Prompt/VideoPrompt包-中文版.md |
| 英文 VideoPrompt | 05-Phase2b-Prompt/VideoPrompt包-英文版.md |

### 1.2 读取产物内容

逐个读取产物文件，将内容加载到审核上下文中。

### 1.3 构建审核上下文

汇总所有产物信息，为后续规则预检和LLM细审提供完整的素材基础。
