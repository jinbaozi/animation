# 本地 Web 工作台运行指南

## 后端

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

默认地址：`http://127.0.0.1:8000`

## 前端

```bash
cd apps/web
npm install
npm run dev
```

默认地址：`http://127.0.0.1:5173`

## 数据与产物

- SQLite 默认文件：`apps/api/animation_workbench.db`
- 项目产物目录：`output/{项目slug}/`
- 最终交付物：VideoPrompt、人物资产卡、场景资产卡

## 第一版执行边界

文本链路支持模型 API 执行器和本地 CLI 执行器。图片生成走 OpenAI-Compatible 图片接口。视频第一版导出 `video-tasks.json` 与 `video-tasks.csv`，不要求自动生成视频。
