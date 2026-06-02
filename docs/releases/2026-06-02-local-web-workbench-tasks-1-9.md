# Release: Local Web Workbench Backend (Tasks 1–9)

> **Branch:** `codex/video-prompt-delivery-assets`
> **Base:** `main`
> **Commits ahead:** 24
> **Status:** Backend complete; frontend pending (Tasks 10–12)

## Summary

Adds a local FastAPI backend (`apps/api/`) that backs the animation-v3 pipeline: project upload, SQLite persistence, encrypted local key vault, phase runner with state machine, pluggable text executors (API + CLI), image generation, and video task export. The work is the first nine tasks of the [Local Web Workbench implementation plan](../superpowers/plans/2026-06-02-local-web-workbench-implementation.md); Tasks 10–12 (React/Vite frontend + run guide) are not in this branch.

## Highlights

- **FastAPI + SQLAlchemy 2 + Pydantic v2** backend under `apps/api/` with a clean `app/{routers,services,core,schemas,models}.py` layout.
- **Encrypted local key vault** (`cryptography.fernet`) — master-password-derived keys, no plaintext secrets on disk.
- **Phase runner state machine** with stale-downstream propagation and review gating.
- **Pluggable text executors** — same `PhaseExecutor` interface for HTTP API and CLI subprocess paths; CLI mode made explicit in 5ed43df.
- **Image generation** — OpenAI-compatible `httpx` client (DALL·E / 即梦 / others), base64 PNG output with auto-mkdir parent dirs.
- **Video task export** — reads `05-Phase2b-Prompt/PromptExportIR.md`, emits `ToolExport/video-tasks.{json,csv}`.

## Commits (24 ahead of main)

### New features
- `7b960d8` — define prompt delivery asset pipeline (IR family)
- `84f1f10` — api health skeleton
- `c6d884c` — workbench database models
- `d1e38b0` — harden workbench database models
- `625a20c` — project artifact storage
- `c4f6d4d` — encrypted api key vault
- `e1f2970` — project upload api
- `c23f884` — phase runner state machine
- `8708c6a` — api and cli phase executors
- `37957f9` — image generation service
- `6662fe9` — video task export

### Hardening / fixes
- `e33641b` — tighten project slug normalization
- `01926f2` — prevent project artifact overwrite
- `f9f2412` — atomically claim project artifact directory
- `3773c3c` — normalize key vault decode errors
- `56cfdf7` — harden project creation api
- `5ed43df` — make cli phase execution explicit

### Tooling / docs / cleanup
- `956b504` — design local web workbench
- `655aa6c` — plan local web workbench implementation
- `117fde3` — ignore local api database
- `6099d53` — mark Tasks 1-8 steps complete in workbench implementation plan
- `0a6329c` — add boundary and failure tests for image generation
- `6ad0821` — onboard Codex config and historical plan/spec docs; gitignore transient artifacts
- `2ea48a4` — stop tracking transient logs and intermediate artifacts

## Test Coverage

- **34 tests passing** across 8 test files (1 deprecation warning, no failures).
- Per-service test parity: every service/router has a matching `tests/test_*.py` file.
- Image generation suite covers happy path + parent-dir creation + trailing-slash normalization + HTTP error + empty-data `IndexError` (5 cases, all marked `@pytest.mark.unit`).

```
tests/test_database_models.py     4 tests
tests/test_executors.py          2 tests
tests/test_health.py             1 test
tests/test_image_generation.py   5 tests
tests/test_key_vault.py          2 tests
tests/test_phase_runner.py       1 test
tests/test_projects_api.py       3 tests
tests/test_storage.py            7 tests  (parametrized)
tests/test_video_tasks.py        1 test
```

## Plan Progress

`docs/superpowers/plans/2026-06-02-local-web-workbench-implementation.md` (68 checkboxes total):

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
| 10 | Frontend Skeleton & Project List | ⏳ |
| 11 | Frontend Workbench Pages | ⏳ |
| 12 | Local Run Guide & Full Verification | ⏳ |

**53/68 done · 15/68 pending (frontend only).**

## Risk & Compatibility Notes

- **No upstream breakage**: `rules/`, `templates/`, `agents/`, `scripts/`, and `output/` contracts are unchanged.
- **New dependency surface**: `apps/api/` is opt-in; legacy `scripts/{orchestrate,audit-agent}.sh` and `validate_project.py` are unaffected.
- **Encrypted vault is local-only**: keys never leave the SQLite file. There is no remote sync; if you move the workbench to a new machine the master password must come with you.
- **Image generation is best-effort**: provider errors surface as `httpx.HTTPStatusError`; UI consumers (Tasks 10–11) will need to handle retry/UI status propagation.
- **gitignore additions**: `.remember/logs/`, `graphify-out/`, `noval-tmp/`, `scripts/graphify-out/` are now ignored. Local files at those paths were removed from tracking in `2ea48a4` (no content lost — all were autosave/log outputs or sample fragments).

## Out of Scope (this branch)

- React/Vite frontend (`apps/web/`) — see Tasks 10–11.
- Production-grade deployment (uvicorn behind reverse proxy, TLS, multi-user auth, remote key sync).
- Provider-specific adapters beyond the OpenAI-compatible HTTP shape.

## Suggested PR Title

> `feat: local web workbench backend (Tasks 1–9 of workbench plan)`

## Test Plan (for PR review)

- [ ] `cd apps/api && python -m venv .venv && source .venv/bin/activate`
- [ ] `pip install -e ".[dev]"`
- [ ] `pytest -v` — expect 34 passed
- [ ] `uvicorn app.main:app --reload` and `curl http://127.0.0.1:8000/api/health` — expect `{"status":"ok","service":"animation-v3-api"}`
- [ ] `curl http://127.0.0.1:8000/api/projects/demo/assets/contract` — expect asset contract JSON
- [ ] `curl http://127.0.0.1:8000/api/projects/demo/video-tasks/contract` — expect video-task contract JSON
- [ ] `curl http://127.0.0.1:8000/api/projects/demo/phases/contract` — expect phase contract JSON
