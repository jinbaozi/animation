# Milestone: Local Web Workbench Tasks 1–10

> **Branch:** `codex/video-prompt-delivery-assets`
> **Base:** `main`
> **Commits ahead:** 27
> **Status:** Backend + frontend skeleton complete; 2 tasks remaining (workbench pages + run guide)

## Summary

Reached a demonstrable milestone on the [Local Web Workbench implementation plan](../superpowers/plans/2026-06-02-local-web-workbench-implementation.md). The FastAPI backend (Tasks 1–9) and the Vite/React/TypeScript frontend skeleton (Task 10) are in place with passing tests. Frontend workbench pages (Task 11) and the local-run guide (Task 12) are the only outstanding work.

## What's New in this Milestone (vs. prior release `tasks-1-9`)

- **Task 10** — Vite 5 + React 18 + TypeScript 5.5 + Vitest 2 frontend scaffold in `apps/web/`
  - Typed API client (`src/api/client.ts`) hitting `/api/projects`
  - `ProjectsPage` with project cards + new-project action
  - Vitest jsdom environment with `@testing-library/jest-dom` matchers
- **Test coverage expansion** — image generation suite grew from 1 → 5 cases (parent-dir, trailing-slash, HTTP error, empty data) and is now `@pytest.mark.unit`-tagged
- **Security hygiene** — pinned esbuild override (`apps/web/package.json`); `npm audit` findings down 5 → 4 (residual are Vite 5.x dev-server-only path traversal, see Risk section)
- **Plan fidelity** — backfilled 58/68 plan checkboxes; one documented plan deviation (`setupFiles` for jest-dom)

## Test Status

| Suite | Pass | Notes |
|-------|------|-------|
| Backend `apps/api/` | **34/34** ✅ | 1 deprecation warning (httpx + starlette TestClient); no failures |
| Frontend `apps/web/` | **1/1** ✅ | ProjectsPage render test |
| Plan checkboxes | **58/68** ✅ | 10 remaining (Task 11 + Task 12) |

## Commits added in this milestone (vs. `tasks-1-9` release)

- `0a6329c` — test: add boundary and failure tests for image generation
- `6ad0821` — chore: onboard Codex config and historical plan/spec docs; gitignore transient artifacts
- `2ea48a4` — chore: stop tracking transient logs and intermediate artifacts
- `d9d3d58` — docs: release notes for local web workbench backend (Tasks 1-9)
- `43c5310` — feat: add web project list skeleton
- `704bc4d` — chore(frontend): pin esbuild override to clear GHSA-67mh-4wv8-2f99

## Plan Progress (58/68)

| Task | Title | Status |
|------|-------|--------|
| 1 | Backend Skeleton & Health Check | ✅ |
| 2 | SQLite Models & Session Setup | ✅ |
| 3 | Artifact Storage Service | ✅ |
| 4 | Encrypted Local Key Vault | ✅ |
| 5 | Project API | ✅ |
| 6 | Phase Runner & State Machine | ✅ |
| 7 | CLI & API Text Executors | ✅ |
| 8 | Image Generation Service | ✅ |
| 9 | Video Task Export | ✅ |
| **10** | **Frontend Skeleton & Project List** | **✅ (this milestone)** |
| 11 | Frontend Workbench Pages | ⏳ |
| 12 | Local Run Guide & Full Verification | ⏳ |

## Risk & Open Items

- **Vite 5.x dev-server advisories (4)** — `GHSA-4w7w-66w2-5vf9` (Vite ≤6.4.1) is a dev-server path-traversal issue affecting the local Vite dev server only. Fix requires Vite 8 + Vitest 3+, which is out of scope for the current plan pin (Vite ^5.4.0). Acceptable for a local-only workbench; revisit when bumping Vite.
- **Plan deviation on Vite config** — `setupFiles: []` in the plan would have left `toBeInTheDocument()` un-registered. We added `src/test-setup.ts` importing `@testing-library/jest-dom/vitest` and updated `vite.config.ts` accordingly. Tracked in commit `43c5310`.
- **No remote configured** — local branch only. `gh auth status` shows the CLI is authenticated to `jinbaozi` but no `origin` is set on this clone.

## Reproducible Test Plan

```bash
# Backend
cd apps/api
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -v                                       # 34/34

# Frontend
cd ../web
npm install
npm test                                        # 1/1
npm run dev   # http://127.0.0.1:5173 (proxies /api → :8000)

# End-to-end (when Task 11 lands and Task 12 documents the full flow)
cd ../api && uvicorn app.main:app --reload      # :8000
```

## Next Milestone (Tasks 11 + 12)

1. **Task 11** — Frontend workbench pages: ProjectWorkbench, Assets, VideoPrompt, ModelSettings, plus shared layout / phase-timeline / file-viewer components.
2. **Task 12** — `docs/web-workbench.md` local-run guide + full verification harness (start API + start web + smoke-test endpoints).
