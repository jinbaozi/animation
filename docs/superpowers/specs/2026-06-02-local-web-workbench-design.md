# 本地 Web 工作台设计规格

> 日期：2026-06-02
> 项目：animation-v3
> 范围：长文小说转 AI 漫剧提示词生成器的本地 Web 化第一版

## 1. 目标

将当前文档、规则、模板和脚本型项目包装成一个本地半自动 Web 工作台。用户上传小说后，可以按 Phase 查看、生成、确认和返工，最终交付 `VideoPrompt`、`人物资产卡`、`场景资产卡`，并支持基于图片 prompt 自动生成参考图、基于视频 prompt 和参考图导出视频任务包。

第一版定位为本地个人工具，不做多人账号、计费、多租户或 SaaS 权限体系。

## 2. 非目标

- 不做商业化 SaaS 后台、用户注册、计费和用量结算。
- 不要求一键自动跑完整条链路到成片。
- 不强绑某一个视频模型 Provider。
- 不重写现有 `rules/`、`templates/`、`agents/` 和标准 `output/` 交付结构。
- 不把 API key 明文写入 SQLite、日志或产物文件。

## 3. 推荐方案

采用“工作台后端 + 双执行器”方案。

FastAPI 作为核心编排层，React/Vite 作为工作台前端。SQLite 记录项目、Phase 状态、模型配置、密钥引用、任务和生成记录；现有 `output/{项目名}/...` 目录继续保存 Markdown、IR、资产卡、VideoPrompt、图片和视频任务包。

文本生成支持两种执行器：

- `model_api_executor`：直接调用配置好的文本模型 API。
- `cli_executor`：调用本地 Codex/Claude CLI 或现有脚本，用于复用当前 agent/rules 流程。

两种执行器都必须写回相同标准目录和文件，Web 后续流程只依赖标准文件与 SQLite 状态。

## 4. 页面结构

第一版打开即进入工作台，不做营销首页。

### 4.1 项目页

展示所有小说项目，包括项目名、当前 Phase、最近更新时间、图片生成状态、视频任务包状态和审核状态。支持新建项目、上传小说、打开项目。

### 4.2 项目工作台

核心生产页面。左侧显示 Phase 导航：G0、Phase0、Phase1、Phase1.5、Phase2a、Phase2b、Audit Gate、最终交付。中间展示当前 Phase 输入、输出、日志和质量检查。右侧提供继续生成、重新生成、标记通过、返工到上游等操作。

### 4.3 资产页

按人物和场景查看资产。人物区展示人物资产卡、四视图 Prompt、已生成参考图；场景区展示场景资产卡、场景 Prompt、已生成场景图。支持单个资产重新生成图片。

### 4.4 VideoPrompt 页

按 sequence 和 shot 展示 PromptExportIR、中文 VideoPrompt、英文 VideoPrompt、工具导出版和参考图。支持导出视频任务包并标记外部视频生成状态。

### 4.5 模型配置页

配置文本模型、图片模型和视频任务包/Provider。文本与图片优先支持 OpenAI-Compatible 配置：`base_url`、`api_key`、`model` 和默认参数。视频第一版优先导出任务包，预留 Provider 适配层。

### 4.6 设置与密钥页

设置主密码、本地密钥解锁状态、输出目录、CLI 路径和默认项目参数。

## 5. 数据流与 Phase 执行

新建项目时，用户上传小说并填写项目名、风格、目标平台、交付范围和默认模型。后端创建 SQLite 项目记录，并按现有规范创建：

- `output/{项目名}/00-原始素材/`
- `output/{项目名}/00-项目配置/`
- 后续 Phase 目录

主流程保持当前链路：

```text
G0 project-manifest
-> Phase0 合规预审
-> Phase1 StoryIR
-> Phase1.5 ShotIR
-> Phase2a VisualAnchorIR + 人物资产卡 + 场景资产卡 + 四视图 Prompt
-> Phase2b PromptExportIR + VideoPrompt
-> Audit Gate
-> 99-最终交付物
```

每个 Phase 有五种状态：

- `pending`：尚未执行。
- `running`：正在执行。
- `needs_review`：生成完成，等待用户确认。
- `approved`：用户已确认，可以进入下游。
- `stale`：上游被修改或重跑，下游需要重新确认或重生成。

Phase 执行接口统一为：

```text
run_phase(project_id, phase_id, executor_type, model_config_id)
```

API 执行器读取对应规则、模板和上游 IR，组装 prompt，调用文本模型并写入目标文件。CLI 执行器调用本地脚本或 CLI prompt，并写回同一标准目录。

Phase 生成完成后不自动进入下一步，而是进入 `needs_review`。用户确认后才进入后续 Phase。

## 6. 模型配置与密钥

### 6.1 文本模型

文本模型优先支持 OpenAI-Compatible 配置：

- `base_url`
- `model`
- `api_key_ref`
- `temperature`
- `max_tokens`
- `timeout`

文本模型用于 G0 到 Phase2b 的文本生成。每个 Phase 可以选择 API 执行器或 CLI 执行器。

### 6.2 图片模型

图片模型优先支持 OpenAI-Compatible 图片接口，同时保留 Provider 扩展层。图片生成入口主要来自 Phase2a：

- 人物四视图 Prompt
- 人物资产卡标准图 Prompt
- 场景资产卡场景 Prompt

生成图片保存到：

- `output/{项目名}/04-Phase2a-四视图/四视图预览/`
- `output/{项目名}/04-Phase2a-四视图/场景预览/`

SQLite 记录 prompt、模型、参数、文件路径、生成状态和错误信息。

### 6.3 视频任务包

第一版视频不强依赖自动 API。系统从 PromptExportIR、VideoPrompt 和参考图生成标准视频任务包，包含：

- `shot_id`
- 中文视频提示词
- 英文视频提示词
- 参考图路径
- 时长
- 画幅比例
- 建议参数
- 目标工具字段

导出位置：

- `output/{项目名}/05-Phase2b-Prompt/ToolExport/video-tasks.json`
- `output/{项目名}/05-Phase2b-Prompt/ToolExport/video-tasks.csv`

后续接 Seedance 或其他视频 Provider 时，Provider 直接读取同一任务包并提交任务。

### 6.4 密钥

API key 使用本地主密码加密保存。加密后的 key 存 SQLite，后端只在用户解锁后把解密 key 放在内存中使用。未解锁时，模型配置可查看但不能执行模型调用。

## 7. 错误处理与可恢复性

每次 Phase 执行、图片生成和视频任务包导出都创建一条 `job` 记录，包含状态、开始时间、结束时间、执行器、模型、输入文件、输出文件、错误类型、错误信息和日志片段。

错误类型分为：

- `config_error`：模型配置、API key、CLI 路径或输出目录缺失。
- `generation_error`：模型调用失败、超时或返回格式不完整。
- `validation_error`：生成了文件，但 IR 字段缺失、禁用词命中或核心交付物不完整。

输出文件是事实来源，SQLite 是状态索引。服务重启后，系统可以扫描 `output/{项目名}/...` 恢复项目状态。用户可以从任意 Phase 重新运行；被影响的下游 Phase 标记为 `stale`。

## 8. 校验与验收

接入现有 `scripts/validate_project.py`。每个 Phase 结束后做轻量校验，最终交付前运行完整校验。

第一版验收标准：

- 可以上传小说并创建项目。
- 可以配置并加密保存文本和图片模型 key。
- 可以用 API 或 CLI 跑完 G0 到 Phase2b。
- 每个 Phase 都能进入 `needs_review`，并由用户确认。
- 可以从人物和场景 Prompt 自动生成图片并保存。
- 可以导出视频任务包。
- 最终交付物包含 VideoPrompt、人物资产卡、场景资产卡。
- 服务重启后项目状态可恢复。
- API key 不以明文出现在 SQLite、日志或产物文件中。

## 9. 第一版建议边界

第一版应优先实现完整生产闭环，而不是追求 Provider 数量。推荐实现顺序：

1. FastAPI + React/Vite 项目骨架。
2. SQLite schema 与输出目录扫描。
3. 模型配置与本地密钥加密。
4. 项目上传与 Phase 工作台。
5. API 执行器与 CLI 执行器。
6. 图片生成与资产页。
7. 视频任务包导出。
8. 最终交付与校验。
