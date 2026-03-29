# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This is a **documentation-only** repository (pure Markdown, zero executable code). It contains the "长文小说转AI漫剧 — Prompt生成系统" knowledge base: structured templates, guides, and role definitions for converting Chinese novel text into AI image-generation prompts.

There are **no** package managers, build systems, services, or automated tests.

### Linting

Run `markdownlint-cli2 "**/*.md"` to lint all Markdown files. Expect many pre-existing style warnings (table formatting, blank-line rules, etc.) — these are **not** bugs.

### Documentation preview

Start a local preview server with `grip 0.0.0.0:6419` from the repo root. This serves rendered Markdown at `http://localhost:6419/`. Grip serves files by direct path (e.g. `/快速开始.md`); subdirectory paths with Chinese characters work (e.g. `/01-输入处理/小说输入模板.md`).

### Important caveats

- Grip uses the GitHub API for rendering; if you hit rate limits, pass `--pass <token>` with a GitHub token. For local-only rendering without GitHub API, consider `python3 -m http.server` as a fallback to browse raw files.
- All content is in Chinese (Simplified). File and directory names use Chinese characters — ensure your shell and tools handle UTF-8 correctly.
