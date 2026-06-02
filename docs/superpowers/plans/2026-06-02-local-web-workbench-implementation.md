# Local Web Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local FastAPI + React/Vite workbench that manages novel projects, Phase execution, encrypted model keys, image generation, video task export, and final delivery files for the animation-v3 pipeline.

**Architecture:** Add a new `apps/api` FastAPI backend and `apps/web` React frontend while preserving the existing `rules/`, `templates/`, `agents/`, `scripts/`, and `output/` contract. SQLite stores state and encrypted configuration; `output/{project}` remains the artifact source of truth. Text generation runs through pluggable API and CLI executors.

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic v2, cryptography, pytest, httpx, React, Vite, TypeScript, Vitest, React Testing Library.

---

## File Structure

Create these focused units:

- `apps/api/pyproject.toml`: backend package metadata and dependencies.
- `apps/api/app/main.py`: FastAPI app factory and router registration.
- `apps/api/app/core/config.py`: environment and path settings.
- `apps/api/app/core/database.py`: SQLite engine/session setup.
- `apps/api/app/models.py`: SQLAlchemy tables for projects, phases, model configs, keys, jobs, generations.
- `apps/api/app/schemas.py`: Pydantic request/response contracts.
- `apps/api/app/services/storage.py`: filesystem artifact paths, project directory creation, output scanning.
- `apps/api/app/services/key_vault.py`: local master-password encryption/decryption.
- `apps/api/app/services/model_config.py`: model config CRUD and key reference validation.
- `apps/api/app/services/executors.py`: `PhaseExecutor` interface, API executor, CLI executor.
- `apps/api/app/services/phase_runner.py`: phase state machine, stale propagation, validation hooks.
- `apps/api/app/services/image_generation.py`: image provider abstraction and generation records.
- `apps/api/app/services/video_tasks.py`: video task JSON/CSV export from prompt artifacts.
- `apps/api/app/routers/*.py`: HTTP API grouped by projects, phases, models, assets, video tasks.
- `apps/api/tests/*.py`: backend tests.
- `apps/web/package.json`: frontend dependencies and scripts.
- `apps/web/src/api/client.ts`: typed API client.
- `apps/web/src/types.ts`: shared frontend types.
- `apps/web/src/pages/*.tsx`: Projects, ProjectWorkbench, Assets, VideoPrompt, ModelSettings.
- `apps/web/src/components/*.tsx`: reusable layout, phase timeline, status badges, file viewers.
- `apps/web/src/__tests__/*.test.tsx`: frontend tests.
- `docs/web-workbench.md`: local run guide.

---

### Task 1: Backend Skeleton And Health Check

**Files:**
- Create: `apps/api/pyproject.toml`
- Create: `apps/api/app/__init__.py`
- Create: `apps/api/app/main.py`
- Create: `apps/api/app/core/config.py`
- Create: `apps/api/tests/test_health.py`

- [x] **Step 1: Create the backend package files**

Create `apps/api/pyproject.toml`:

```toml
[project]
name = "animation-v3-api"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.115.0",
  "uvicorn[standard]>=0.30.0",
  "sqlalchemy>=2.0.0",
  "pydantic>=2.8.0",
  "pydantic-settings>=2.4.0",
  "cryptography>=43.0.0",
  "python-multipart>=0.0.9",
  "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
  "pytest-asyncio>=0.24.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Create `apps/api/app/__init__.py` as an empty file.

- [x] **Step 2: Write the failing health test**

Create `apps/api/tests/test_health.py`:

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_ok():
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "animation-v3-api",
    }
```

- [x] **Step 3: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_health.py -v
```

Expected: fail because `app.main` does not exist.

- [x] **Step 4: Implement app settings and health route**

Create `apps/api/app/core/config.py`:

```python
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    repo_root: Path = Path(__file__).resolve().parents[4]
    output_root: Path | None = None
    database_url: str = "sqlite:///./animation_workbench.db"

    model_config = SettingsConfigDict(env_prefix="ANIMATION_V3_")

    @property
    def resolved_output_root(self) -> Path:
        return self.output_root or self.repo_root / "output"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Create `apps/api/app/main.py`:

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="animation-v3 local workbench")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    return app


app = create_app()
```

- [x] **Step 5: Run the test and verify it passes**

Run:

```bash
cd apps/api
python -m pytest tests/test_health.py -v
```

Expected: `1 passed`.

- [x] **Step 6: Commit**

```bash
git add apps/api/pyproject.toml apps/api/app apps/api/tests/test_health.py
git commit -m "feat: add api health skeleton"
```

---

### Task 2: SQLite Models And Session Setup

**Files:**
- Create: `apps/api/app/core/database.py`
- Create: `apps/api/app/models.py`
- Create: `apps/api/tests/test_database_models.py`

- [x] **Step 1: Write model persistence tests**

Create `apps/api/tests/test_database_models.py`:

```python
from pathlib import Path

from app.core.database import create_sqlite_engine, init_db, session_scope
from app.models import Job, ModelConfig, Phase, Project


def test_project_phase_model_config_and_job_persist(tmp_path: Path):
    engine = create_sqlite_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)

    with session_scope(engine) as session:
        project = Project(name="demo", slug="demo", output_dir="output/demo")
        session.add(project)
        session.flush()

        phase = Phase(project_id=project.id, phase_id="phase1", status="pending")
        config = ModelConfig(
            name="local-compatible",
            provider_type="openai_compatible",
            modality="text",
            base_url="https://api.example.test/v1",
            model_name="demo-model",
            encrypted_key_id=None,
            default_params={"temperature": 0.4},
        )
        job = Job(project_id=project.id, phase_id="phase1", status="running", kind="phase")
        session.add_all([phase, config, job])

    with session_scope(engine) as session:
        saved = session.query(Project).filter_by(slug="demo").one()
        assert saved.phases[0].phase_id == "phase1"
        assert saved.phases[0].status == "pending"
        assert session.query(ModelConfig).one().default_params == {"temperature": 0.4}
        assert session.query(Job).one().kind == "phase"
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_database_models.py -v
```

Expected: fail because database and models modules do not exist.

- [x] **Step 3: Implement database utilities**

Create `apps/api/app/core/database.py`:

```python
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.models import Base


def create_sqlite_engine(database_url: str) -> Engine:
    return create_engine(database_url, connect_args={"check_same_thread": False})


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope(engine: Engine) -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

- [x] **Step 4: Implement SQLAlchemy models**

Create `apps/api/app/models.py`:

```python
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    output_dir: Mapped[str] = mapped_column(Text, nullable=False)
    current_phase: Mapped[str] = mapped_column(String(40), default="g0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    phases: Mapped[list["Phase"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Phase(Base):
    __tablename__ = "phases"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    phase_id: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    output_files: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    validation: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    project: Mapped[Project] = relationship(back_populates="phases")


class EncryptedKey(Base):
    __tablename__ = "encrypted_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(160), nullable=False)
    nonce: Mapped[str] = mapped_column(Text, nullable=False)
    ciphertext: Mapped[str] = mapped_column(Text, nullable=False)
    salt: Mapped[str] = mapped_column(Text, nullable=False)


class ModelConfig(Base):
    __tablename__ = "model_configs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(80), nullable=False)
    modality: Mapped[str] = mapped_column(String(40), nullable=False)
    base_url: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(String(200), nullable=False)
    encrypted_key_id: Mapped[int | None] = mapped_column(ForeignKey("encrypted_keys.id"), nullable=True)
    default_params: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    phase_id: Mapped[str | None] = mapped_column(String(40), nullable=True)
    kind: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    error_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    log_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(40), nullable=False)
    source_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    model_config_id: Mapped[int | None] = mapped_column(ForeignKey("model_configs.id"), nullable=True)
    output_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    params: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
```

- [x] **Step 5: Run the tests and verify they pass**

Run:

```bash
cd apps/api
python -m pytest tests/test_database_models.py tests/test_health.py -v
```

Expected: all tests pass.

- [x] **Step 6: Commit**

```bash
git add apps/api/app/core/database.py apps/api/app/models.py apps/api/tests/test_database_models.py
git commit -m "feat: add workbench database models"
```

---

### Task 3: Artifact Storage Service

**Files:**
- Create: `apps/api/app/services/storage.py`
- Create: `apps/api/tests/test_storage.py`

- [x] **Step 1: Write storage tests**

Create `apps/api/tests/test_storage.py`:

```python
from pathlib import Path

from app.services.storage import PHASE_DIRS, create_project_structure, project_slug


def test_project_slug_normalizes_ascii_and_keeps_chinese():
    assert project_slug("开局一张弓 装备就变强!") == "开局一张弓-装备就变强"
    assert project_slug("Demo Project") == "demo-project"


def test_create_project_structure_writes_expected_dirs_and_novel(tmp_path: Path):
    result = create_project_structure(
        output_root=tmp_path,
        project_name="Demo Project",
        novel_filename="novel.txt",
        novel_content="第一章\n少年醒来。",
    )

    assert result.project_dir == tmp_path / "demo-project"
    assert (result.project_dir / "00-原始素材" / "novel.txt").read_text(encoding="utf-8") == "第一章\n少年醒来。"
    for relative_dir in PHASE_DIRS:
        assert (result.project_dir / relative_dir).is_dir()
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_storage.py -v
```

Expected: fail because `app.services.storage` does not exist.

- [x] **Step 3: Implement storage service**

Create `apps/api/app/services/storage.py`:

```python
from dataclasses import dataclass
from pathlib import Path
import re


PHASE_DIRS = [
    "00-项目配置",
    "00-原始素材",
    "01-Phase0-合规预审",
    "02-Phase1-剧本分镜",
    "03-Phase1.5-镜头序列",
    "04-Phase2a-四视图",
    "04-Phase2a-四视图/四视图预览",
    "04-Phase2a-四视图/场景预览",
    "05-Phase2b-Prompt",
    "05-Phase2b-Prompt/ToolExport",
    "06-Audit-Gate",
    "99-最终交付物",
]


@dataclass(frozen=True)
class ProjectStructure:
    slug: str
    project_dir: Path
    novel_path: Path


def project_slug(name: str) -> str:
    lowered = name.strip().lower()
    replaced = re.sub(r"\s+", "-", lowered)
    cleaned = re.sub(r"[^\w\u4e00-\u9fff.-]+", "", replaced)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    if not cleaned:
        raise ValueError("project name must contain at least one letter, number, or Chinese character")
    return cleaned


def create_project_structure(
    output_root: Path,
    project_name: str,
    novel_filename: str,
    novel_content: str,
) -> ProjectStructure:
    slug = project_slug(project_name)
    project_dir = output_root / slug
    for relative_dir in PHASE_DIRS:
        (project_dir / relative_dir).mkdir(parents=True, exist_ok=True)

    safe_filename = Path(novel_filename).name or "novel.txt"
    novel_path = project_dir / "00-原始素材" / safe_filename
    novel_path.write_text(novel_content, encoding="utf-8")

    return ProjectStructure(slug=slug, project_dir=project_dir, novel_path=novel_path)
```

- [x] **Step 4: Run the storage tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_storage.py -v
```

Expected: all tests pass.

- [x] **Step 5: Commit**

```bash
git add apps/api/app/services/storage.py apps/api/tests/test_storage.py
git commit -m "feat: add project artifact storage"
```

---

### Task 4: Encrypted Local Key Vault

**Files:**
- Create: `apps/api/app/services/key_vault.py`
- Create: `apps/api/tests/test_key_vault.py`

- [x] **Step 1: Write encryption tests**

Create `apps/api/tests/test_key_vault.py`:

```python
import pytest

from app.services.key_vault import decrypt_secret, encrypt_secret


def test_encrypt_secret_round_trips_with_master_password():
    encrypted = encrypt_secret("master-pass", "sk-test-123")

    assert encrypted.ciphertext != "sk-test-123"
    assert decrypt_secret("master-pass", encrypted) == "sk-test-123"


def test_decrypt_secret_rejects_wrong_master_password():
    encrypted = encrypt_secret("master-pass", "sk-test-123")

    with pytest.raises(ValueError, match="Unable to decrypt API key"):
        decrypt_secret("wrong-pass", encrypted)
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_key_vault.py -v
```

Expected: fail because `app.services.key_vault` does not exist.

- [x] **Step 3: Implement key vault**

Create `apps/api/app/services/key_vault.py`:

```python
from dataclasses import dataclass
import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


@dataclass(frozen=True)
class EncryptedSecret:
    salt: str
    nonce: str
    ciphertext: str


def _derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390_000,
    )
    return kdf.derive(master_password.encode("utf-8"))


def encrypt_secret(master_password: str, secret: str) -> EncryptedSecret:
    if not master_password:
        raise ValueError("master password is required")
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = _derive_key(master_password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, secret.encode("utf-8"), None)
    return EncryptedSecret(
        salt=base64.b64encode(salt).decode("ascii"),
        nonce=base64.b64encode(nonce).decode("ascii"),
        ciphertext=base64.b64encode(ciphertext).decode("ascii"),
    )


def decrypt_secret(master_password: str, encrypted: EncryptedSecret) -> str:
    try:
        salt = base64.b64decode(encrypted.salt)
        nonce = base64.b64decode(encrypted.nonce)
        ciphertext = base64.b64decode(encrypted.ciphertext)
        key = _derive_key(master_password, salt)
        return AESGCM(key).decrypt(nonce, ciphertext, None).decode("utf-8")
    except (InvalidTag, ValueError) as exc:
        raise ValueError("Unable to decrypt API key") from exc
```

- [x] **Step 4: Run the key vault tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_key_vault.py -v
```

Expected: all tests pass.

- [x] **Step 5: Commit**

```bash
git add apps/api/app/services/key_vault.py apps/api/tests/test_key_vault.py
git commit -m "feat: add encrypted api key vault"
```

---

### Task 5: Project API

**Files:**
- Create: `apps/api/app/schemas.py`
- Create: `apps/api/app/routers/projects.py`
- Modify: `apps/api/app/main.py`
- Create: `apps/api/tests/test_projects_api.py`

- [x] **Step 1: Write project API tests**

Create `apps/api/tests/test_projects_api.py`:

```python
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def test_create_and_list_project(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ANIMATION_V3_OUTPUT_ROOT", str(tmp_path / "output"))
    monkeypatch.setenv("ANIMATION_V3_DATABASE_URL", f"sqlite:///{tmp_path / 'workbench.db'}")

    client = TestClient(create_app())

    create_response = client.post(
        "/api/projects",
        files={"novel": ("novel.txt", "第一章\n少年醒来。", "text/plain")},
        data={"name": "Demo Project", "style": "西幻冒险", "target_platform": "抖音"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "Demo Project"
    assert created["slug"] == "demo-project"
    assert created["current_phase"] == "g0"

    list_response = client.get("/api/projects")
    assert list_response.status_code == 200
    assert list_response.json()[0]["slug"] == "demo-project"
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_projects_api.py -v
```

Expected: fail because project router does not exist.

- [x] **Step 3: Implement schemas**

Create `apps/api/app/schemas.py`:

```python
from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    name: str
    slug: str
    output_dir: str
    current_phase: str

    model_config = {"from_attributes": True}
```

- [x] **Step 4: Implement projects router**

Create `apps/api/app/routers/projects.py`:

```python
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.engine import Engine

from app.core.config import get_settings
from app.core.database import create_sqlite_engine, init_db, session_scope
from app.models import Phase, Project
from app.schemas import ProjectResponse
from app.services.storage import create_project_structure


router = APIRouter(prefix="/api/projects", tags=["projects"])


def get_engine() -> Engine:
    settings = get_settings()
    engine = create_sqlite_engine(settings.database_url)
    init_db(engine)
    return engine


PHASE_IDS = ["g0", "phase0", "phase1", "phase1_5", "phase2a", "phase2b", "audit_gate", "final"]


@router.get("", response_model=list[ProjectResponse])
def list_projects(engine: Engine = Depends(get_engine)) -> list[Project]:
    with session_scope(engine) as session:
        return list(session.query(Project).order_by(Project.updated_at.desc()).all())


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    name: str = Form(...),
    style: str = Form(""),
    target_platform: str = Form(""),
    novel: UploadFile = File(...),
    engine: Engine = Depends(get_engine),
) -> Project:
    content = (await novel.read()).decode("utf-8")
    structure = create_project_structure(
        output_root=get_settings().resolved_output_root,
        project_name=name,
        novel_filename=novel.filename or "novel.txt",
        novel_content=content,
    )
    manifest = structure.project_dir / "00-项目配置" / "project-manifest.md"
    manifest.write_text(
        f"# Project Manifest\n\n项目名: {name}\n风格: {style}\n目标平台: {target_platform}\n交付范围: VideoPrompt包 + 人物资产卡 + 场景资产卡\n",
        encoding="utf-8",
    )

    with session_scope(engine) as session:
        existing = session.query(Project).filter_by(slug=structure.slug).one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="project slug already exists")
        project = Project(name=name, slug=structure.slug, output_dir=str(structure.project_dir), current_phase="g0")
        session.add(project)
        session.flush()
        session.add_all([Phase(project_id=project.id, phase_id=phase_id, status="pending") for phase_id in PHASE_IDS])
        session.refresh(project)
        return project
```

- [x] **Step 5: Register router**

Modify `apps/api/app/main.py`:

```python
from fastapi import FastAPI

from app.routers.projects import router as projects_router


def create_app() -> FastAPI:
    app = FastAPI(title="animation-v3 local workbench")
    app.include_router(projects_router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    return app


app = create_app()
```

- [x] **Step 6: Run project API tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_projects_api.py tests/test_storage.py tests/test_database_models.py -v
```

Expected: all tests pass.

- [x] **Step 7: Commit**

```bash
git add apps/api/app/schemas.py apps/api/app/routers/projects.py apps/api/app/main.py apps/api/tests/test_projects_api.py
git commit -m "feat: add project upload api"
```

---

### Task 6: Phase Runner And State Machine

**Files:**
- Create: `apps/api/app/services/executors.py`
- Create: `apps/api/app/services/phase_runner.py`
- Create: `apps/api/app/routers/phases.py`
- Modify: `apps/api/app/main.py`
- Create: `apps/api/tests/test_phase_runner.py`

- [x] **Step 1: Write phase runner tests**

Create `apps/api/tests/test_phase_runner.py`:

```python
from pathlib import Path

from app.services.executors import ExecutionResult, PhaseExecutor
from app.services.phase_runner import PhaseRunner


class FakeExecutor(PhaseExecutor):
    def run_phase(self, project_dir: Path, phase_id: str) -> ExecutionResult:
        output = project_dir / "02-Phase1-剧本分镜" / "StoryIR.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# StoryIR\n", encoding="utf-8")
        return ExecutionResult(output_files={"StoryIR": str(output)}, log_excerpt="generated StoryIR")


def test_phase_runner_sets_needs_review_and_marks_downstream_stale(tmp_path: Path):
    project_dir = tmp_path / "demo"
    runner = PhaseRunner(executor=FakeExecutor())

    state = runner.run(project_dir=project_dir, phase_id="phase1")

    assert state.status == "needs_review"
    assert state.output_files["StoryIR"].endswith("StoryIR.md")
    assert state.downstream_status == {"phase1_5": "stale", "phase2a": "stale", "phase2b": "stale", "audit_gate": "stale", "final": "stale"}
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_phase_runner.py -v
```

Expected: fail because executor and phase runner modules do not exist.

- [x] **Step 3: Implement executor contracts**

Create `apps/api/app/services/executors.py`:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ExecutionResult:
    output_files: dict[str, str]
    log_excerpt: str


class PhaseExecutor(Protocol):
    def run_phase(self, project_dir: Path, phase_id: str) -> ExecutionResult:
        raise NotImplementedError
```

- [x] **Step 4: Implement phase runner**

Create `apps/api/app/services/phase_runner.py`:

```python
from dataclasses import dataclass
from pathlib import Path

from app.services.executors import PhaseExecutor


PHASE_ORDER = ["g0", "phase0", "phase1", "phase1_5", "phase2a", "phase2b", "audit_gate", "final"]


@dataclass(frozen=True)
class PhaseRunState:
    status: str
    output_files: dict[str, str]
    log_excerpt: str
    downstream_status: dict[str, str]


class PhaseRunner:
    def __init__(self, executor: PhaseExecutor):
        self.executor = executor

    def run(self, project_dir: Path, phase_id: str) -> PhaseRunState:
        if phase_id not in PHASE_ORDER:
            raise ValueError(f"unknown phase: {phase_id}")
        result = self.executor.run_phase(project_dir, phase_id)
        downstream = {
            later_phase: "stale"
            for later_phase in PHASE_ORDER[PHASE_ORDER.index(phase_id) + 1 :]
        }
        return PhaseRunState(
            status="needs_review",
            output_files=result.output_files,
            log_excerpt=result.log_excerpt,
            downstream_status=downstream,
        )
```

- [x] **Step 5: Add phase router endpoint for the future UI**

Create `apps/api/app/routers/phases.py`:

```python
from fastapi import APIRouter


router = APIRouter(prefix="/api/projects/{project_id}/phases", tags=["phases"])


@router.get("")
def list_phase_contract() -> dict[str, list[str]]:
    return {
        "phases": ["g0", "phase0", "phase1", "phase1_5", "phase2a", "phase2b", "audit_gate", "final"],
        "statuses": ["pending", "running", "needs_review", "approved", "stale"],
    }
```

Modify `apps/api/app/main.py`:

```python
from fastapi import FastAPI

from app.routers.phases import router as phases_router
from app.routers.projects import router as projects_router


def create_app() -> FastAPI:
    app = FastAPI(title="animation-v3 local workbench")
    app.include_router(projects_router)
    app.include_router(phases_router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    return app


app = create_app()
```

- [x] **Step 6: Run phase runner tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_phase_runner.py tests/test_health.py -v
```

Expected: all tests pass.

- [x] **Step 7: Commit**

```bash
git add apps/api/app/services/executors.py apps/api/app/services/phase_runner.py apps/api/app/routers/phases.py apps/api/app/main.py apps/api/tests/test_phase_runner.py
git commit -m "feat: add phase runner state machine"
```

---

### Task 7: CLI And API Text Executors

**Files:**
- Modify: `apps/api/app/services/executors.py`
- Create: `apps/api/tests/test_executors.py`

- [x] **Step 1: Write executor tests**

Create `apps/api/tests/test_executors.py`:

```python
from pathlib import Path
import subprocess

import httpx

from app.services.executors import ApiPhaseExecutor, CliPhaseExecutor


def test_api_phase_executor_writes_phase_output(tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"choices": [{"message": {"content": "# StoryIR\n生成内容"}}]})

    executor = ApiPhaseExecutor(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="demo-model",
    )

    result = executor.run_phase(tmp_path, "phase1")

    output = tmp_path / "02-Phase1-剧本分镜" / "StoryIR.md"
    assert output.read_text(encoding="utf-8") == "# StoryIR\n生成内容"
    assert result.output_files == {"StoryIR": str(output)}


def test_cli_phase_executor_captures_script_output(tmp_path: Path, monkeypatch):
    def fake_run(command, cwd, capture_output, text, check):
        output = tmp_path / "02-Phase1-剧本分镜" / "StoryIR.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# StoryIR\nCLI", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    executor = CliPhaseExecutor(repo_root=tmp_path, script_path="scripts/orchestrate.sh", project_name="demo")

    result = executor.run_phase(tmp_path, "phase1")

    assert result.log_excerpt == "ok"
    assert result.output_files["StoryIR"].endswith("StoryIR.md")
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_executors.py -v
```

Expected: fail because concrete executors are not defined.

- [x] **Step 3: Implement concrete executors**

Modify `apps/api/app/services/executors.py`:

```python
from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Protocol

import httpx


PHASE_OUTPUTS = {
    "phase1": ("02-Phase1-剧本分镜", "StoryIR.md", "StoryIR"),
}


@dataclass(frozen=True)
class ExecutionResult:
    output_files: dict[str, str]
    log_excerpt: str


class PhaseExecutor(Protocol):
    def run_phase(self, project_dir: Path, phase_id: str) -> ExecutionResult:
        raise NotImplementedError


class ApiPhaseExecutor:
    def __init__(self, client: httpx.Client, base_url: str, api_key: str, model_name: str):
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model_name = model_name

    def run_phase(self, project_dir: Path, phase_id: str) -> ExecutionResult:
        directory, filename, label = PHASE_OUTPUTS[phase_id]
        output_path = project_dir / directory / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": f"Generate {label} for animation-v3 phase {phase_id}."}],
            },
            timeout=120,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        output_path.write_text(content, encoding="utf-8")
        return ExecutionResult(output_files={label: str(output_path)}, log_excerpt=f"generated {label}")


class CliPhaseExecutor:
    def __init__(self, repo_root: Path, script_path: str, project_name: str):
        self.repo_root = repo_root
        self.script_path = script_path
        self.project_name = project_name

    def run_phase(self, project_dir: Path, phase_id: str) -> ExecutionResult:
        completed = subprocess.run(
            [str(self.repo_root / self.script_path), f"--project={self.project_name}", f"--phase={phase_id}"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        directory, filename, label = PHASE_OUTPUTS.get(phase_id, ("", "", "output"))
        output_path = project_dir / directory / filename if directory else project_dir
        return ExecutionResult(output_files={label: str(output_path)}, log_excerpt=completed.stdout[-2000:])
```

- [x] **Step 4: Run executor tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_executors.py tests/test_phase_runner.py -v
```

Expected: all tests pass.

- [x] **Step 5: Commit**

```bash
git add apps/api/app/services/executors.py apps/api/tests/test_executors.py
git commit -m "feat: add api and cli phase executors"
```

---

### Task 8: Image Generation Service

**Files:**
- Create: `apps/api/app/services/image_generation.py`
- Create: `apps/api/app/routers/assets.py`
- Modify: `apps/api/app/main.py`
- Create: `apps/api/tests/test_image_generation.py`

- [x] **Step 1: Write image generation tests**

Create `apps/api/tests/test_image_generation.py`:

```python
from pathlib import Path
import base64

import httpx

from app.services.image_generation import OpenAICompatibleImageGenerator


def test_image_generator_saves_base64_png(tmp_path: Path):
    png_bytes = b"\x89PNG\r\n\x1a\n"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [{"b64_json": base64.b64encode(png_bytes).decode("ascii")}]})

    generator = OpenAICompatibleImageGenerator(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="image-model",
    )

    output = generator.generate(prompt="角色正面全身", output_path=tmp_path / "preview.png", size="1024x1024")

    assert output.read_bytes() == png_bytes
```

- [x] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_image_generation.py -v
```

Expected: fail because image generation module does not exist.

- [x] **Step 3: Implement image generator**

Create `apps/api/app/services/image_generation.py`:

```python
from pathlib import Path
import base64

import httpx


class OpenAICompatibleImageGenerator:
    def __init__(self, client: httpx.Client, base_url: str, api_key: str, model_name: str):
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str, output_path: Path, size: str = "1024x1024") -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        response = self.client.post(
            f"{self.base_url}/images/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model_name, "prompt": prompt, "size": size, "response_format": "b64_json"},
            timeout=180,
        )
        response.raise_for_status()
        image_data = response.json()["data"][0]["b64_json"]
        output_path.write_bytes(base64.b64decode(image_data))
        return output_path
```

- [x] **Step 4: Add assets router contract**

Create `apps/api/app/routers/assets.py`:

```python
from fastapi import APIRouter


router = APIRouter(prefix="/api/projects/{project_id}/assets", tags=["assets"])


@router.get("/contract")
def asset_contract() -> dict[str, list[str]]:
    return {"asset_types": ["character", "scene"], "image_statuses": ["pending", "running", "done", "failed"]}
```

Modify `apps/api/app/main.py`:

```python
from fastapi import FastAPI

from app.routers.assets import router as assets_router
from app.routers.phases import router as phases_router
from app.routers.projects import router as projects_router


def create_app() -> FastAPI:
    app = FastAPI(title="animation-v3 local workbench")
    app.include_router(projects_router)
    app.include_router(phases_router)
    app.include_router(assets_router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    return app


app = create_app()
```

- [x] **Step 5: Run image tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_image_generation.py tests/test_health.py -v
```

Expected: all tests pass.

- [x] **Step 6: Commit**

```bash
git add apps/api/app/services/image_generation.py apps/api/app/routers/assets.py apps/api/app/main.py apps/api/tests/test_image_generation.py
git commit -m "feat: add image generation service"
```

---

### Task 9: Video Task Export

**Files:**
- Create: `apps/api/app/services/video_tasks.py`
- Create: `apps/api/app/routers/video_tasks.py`
- Modify: `apps/api/app/main.py`
- Create: `apps/api/tests/test_video_tasks.py`

- [ ] **Step 1: Write video task export tests**

Create `apps/api/tests/test_video_tasks.py`:

```python
from pathlib import Path
import json

from app.services.video_tasks import export_video_tasks


def test_export_video_tasks_writes_json_and_csv(tmp_path: Path):
    project_dir = tmp_path / "demo"
    prompt_dir = project_dir / "05-Phase2b-Prompt"
    prompt_dir.mkdir(parents=True)
    (prompt_dir / "PromptExportIR.md").write_text(
        "shot_id: S001\nzh_prompt: 吴为拉开弓。\nen_prompt: Wu Wei draws the bow.\nreference_image: ../04-Phase2a-四视图/四视图预览/吴为.png\n",
        encoding="utf-8",
    )

    result = export_video_tasks(project_dir)

    data = json.loads(result.json_path.read_text(encoding="utf-8"))
    assert data[0]["shot_id"] == "S001"
    assert "Wu Wei draws the bow." in result.csv_path.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
cd apps/api
python -m pytest tests/test_video_tasks.py -v
```

Expected: fail because video task service does not exist.

- [ ] **Step 3: Implement video task exporter**

Create `apps/api/app/services/video_tasks.py`:

```python
from dataclasses import dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class VideoTaskExport:
    json_path: Path
    csv_path: Path


def _parse_simple_prompt_export(content: str) -> list[dict[str, str]]:
    current: dict[str, str] = {}
    for line in content.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = value.strip()
    return [{
        "shot_id": current.get("shot_id", "S001"),
        "zh_prompt": current.get("zh_prompt", ""),
        "en_prompt": current.get("en_prompt", ""),
        "reference_image": current.get("reference_image", ""),
        "duration_seconds": "15",
        "aspect_ratio": "9:16",
        "target_tool": "generic-video-task-package",
    }]


def export_video_tasks(project_dir: Path) -> VideoTaskExport:
    prompt_export = project_dir / "05-Phase2b-Prompt" / "PromptExportIR.md"
    tasks = _parse_simple_prompt_export(prompt_export.read_text(encoding="utf-8"))
    export_dir = project_dir / "05-Phase2b-Prompt" / "ToolExport"
    export_dir.mkdir(parents=True, exist_ok=True)

    json_path = export_dir / "video-tasks.json"
    csv_path = export_dir / "video-tasks.csv"
    json_path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(tasks[0].keys()))
        writer.writeheader()
        writer.writerows(tasks)

    return VideoTaskExport(json_path=json_path, csv_path=csv_path)
```

- [ ] **Step 4: Register video task router contract**

Create `apps/api/app/routers/video_tasks.py`:

```python
from fastapi import APIRouter


router = APIRouter(prefix="/api/projects/{project_id}/video-tasks", tags=["video-tasks"])


@router.get("/contract")
def video_task_contract() -> dict[str, list[str]]:
    return {"exports": ["video-tasks.json", "video-tasks.csv"], "provider_modes": ["task_package", "provider_adapter"]}
```

Modify `apps/api/app/main.py`:

```python
from fastapi import FastAPI

from app.routers.assets import router as assets_router
from app.routers.phases import router as phases_router
from app.routers.projects import router as projects_router
from app.routers.video_tasks import router as video_tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="animation-v3 local workbench")
    app.include_router(projects_router)
    app.include_router(phases_router)
    app.include_router(assets_router)
    app.include_router(video_tasks_router)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    return app


app = create_app()
```

- [ ] **Step 5: Run video task tests**

Run:

```bash
cd apps/api
python -m pytest tests/test_video_tasks.py tests/test_health.py -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add apps/api/app/services/video_tasks.py apps/api/app/routers/video_tasks.py apps/api/app/main.py apps/api/tests/test_video_tasks.py
git commit -m "feat: add video task export"
```

---

### Task 10: Frontend Skeleton And Project List

**Files:**
- Create: `apps/web/package.json`
- Create: `apps/web/index.html`
- Create: `apps/web/vite.config.ts`
- Create: `apps/web/tsconfig.json`
- Create: `apps/web/src/main.tsx`
- Create: `apps/web/src/App.tsx`
- Create: `apps/web/src/api/client.ts`
- Create: `apps/web/src/types.ts`
- Create: `apps/web/src/pages/ProjectsPage.tsx`
- Create: `apps/web/src/__tests__/ProjectsPage.test.tsx`

- [ ] **Step 1: Create frontend package files**

Create `apps/web/package.json`:

```json
{
  "name": "animation-v3-web",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "test": "vitest run",
    "build": "tsc && vite build"
  },
  "dependencies": {
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^5.4.0",
    "typescript": "^5.5.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.4.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "jsdom": "^25.0.0",
    "vitest": "^2.0.0"
  }
}
```

Create `apps/web/index.html`:

```html
<div id="root"></div>
<script type="module" src="/src/main.tsx"></script>
```

Create `apps/web/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
```

Create `apps/web/vite.config.ts`:

```ts
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: [],
  },
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
```

- [ ] **Step 2: Write project page test**

Create `apps/web/src/__tests__/ProjectsPage.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ProjectsPage } from "../pages/ProjectsPage";

describe("ProjectsPage", () => {
  it("renders project status and creation action", () => {
    render(
      <ProjectsPage
        projects={[
          { id: 1, name: "Demo Project", slug: "demo-project", current_phase: "phase1", output_dir: "output/demo-project" },
        ]}
      />,
    );

    expect(screen.getByText("Demo Project")).toBeInTheDocument();
    expect(screen.getByText("phase1")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "新建项目" })).toBeInTheDocument();
  });
});
```

- [ ] **Step 3: Implement frontend source files**

Create `apps/web/src/types.ts`:

```ts
export type Project = {
  id: number;
  name: string;
  slug: string;
  output_dir: string;
  current_phase: string;
};
```

Create `apps/web/src/api/client.ts`:

```ts
import type { Project } from "../types";

export async function listProjects(): Promise<Project[]> {
  const response = await fetch("/api/projects");
  if (!response.ok) {
    throw new Error(`Failed to load projects: ${response.status}`);
  }
  return response.json();
}
```

Create `apps/web/src/pages/ProjectsPage.tsx`:

```tsx
import type { Project } from "../types";

type ProjectsPageProps = {
  projects: Project[];
};

export function ProjectsPage({ projects }: ProjectsPageProps) {
  return (
    <main style={{ padding: 24, maxWidth: 1120, margin: "0 auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1>AI 漫剧工作台</h1>
          <p>上传小说，按 Phase 生成 VideoPrompt、人物资产卡和场景资产卡。</p>
        </div>
        <button type="button">新建项目</button>
      </header>

      <section style={{ marginTop: 24, display: "grid", gap: 12 }}>
        {projects.map((project) => (
          <article key={project.id} style={{ border: "1px solid #d6dbe4", borderRadius: 8, padding: 16 }}>
            <h2>{project.name}</h2>
            <p>{project.slug}</p>
            <strong>{project.current_phase}</strong>
          </article>
        ))}
      </section>
    </main>
  );
}
```

Create `apps/web/src/App.tsx`:

```tsx
import { ProjectsPage } from "./pages/ProjectsPage";

export function App() {
  return <ProjectsPage projects={[]} />;
}
```

Create `apps/web/src/main.tsx`:

```tsx
import React from "react";
import ReactDOM from "react-dom/client";

import { App } from "./App";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

- [ ] **Step 4: Run frontend tests**

Run:

```bash
cd apps/web
npm install
npm test
```

Expected: `ProjectsPage` test passes.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: add web project list skeleton"
```

---

### Task 11: Frontend Workbench Pages

**Files:**
- Create: `apps/web/src/pages/ProjectWorkbenchPage.tsx`
- Create: `apps/web/src/pages/AssetsPage.tsx`
- Create: `apps/web/src/pages/VideoPromptPage.tsx`
- Create: `apps/web/src/pages/ModelSettingsPage.tsx`
- Create: `apps/web/src/components/PhaseTimeline.tsx`
- Create: `apps/web/src/__tests__/WorkbenchPages.test.tsx`

- [ ] **Step 1: Write workbench page tests**

Create `apps/web/src/__tests__/WorkbenchPages.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AssetsPage } from "../pages/AssetsPage";
import { ModelSettingsPage } from "../pages/ModelSettingsPage";
import { ProjectWorkbenchPage } from "../pages/ProjectWorkbenchPage";
import { VideoPromptPage } from "../pages/VideoPromptPage";

describe("Workbench pages", () => {
  it("renders phase review controls", () => {
    render(<ProjectWorkbenchPage />);
    expect(screen.getByText("Phase 工作台")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "标记通过" })).toBeInTheDocument();
  });

  it("renders asset and prompt pages", () => {
    render(<AssetsPage />);
    expect(screen.getByText("人物资产")).toBeInTheDocument();
    render(<VideoPromptPage />);
    expect(screen.getByText("视频任务包导出")).toBeInTheDocument();
  });

  it("renders encrypted key status", () => {
    render(<ModelSettingsPage />);
    expect(screen.getByText("密钥状态：未解锁")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Implement phase timeline**

Create `apps/web/src/components/PhaseTimeline.tsx`:

```tsx
const phases = ["G0", "Phase0", "Phase1", "Phase1.5", "Phase2a", "Phase2b", "Audit Gate", "最终交付"];

export function PhaseTimeline() {
  return (
    <nav aria-label="Phase 导航" style={{ display: "grid", gap: 8 }}>
      {phases.map((phase) => (
        <button key={phase} type="button" style={{ textAlign: "left" }}>
          {phase}
        </button>
      ))}
    </nav>
  );
}
```

- [ ] **Step 3: Implement workbench pages**

Create `apps/web/src/pages/ProjectWorkbenchPage.tsx`:

```tsx
import { PhaseTimeline } from "../components/PhaseTimeline";

export function ProjectWorkbenchPage() {
  return (
    <main style={{ display: "grid", gridTemplateColumns: "220px 1fr 240px", gap: 20, padding: 24 }}>
      <PhaseTimeline />
      <section>
        <h1>Phase 工作台</h1>
        <h2>当前输出</h2>
        <pre>等待生成或选择 Phase。</pre>
      </section>
      <aside style={{ display: "grid", gap: 8, alignContent: "start" }}>
        <button type="button">继续生成</button>
        <button type="button">重新生成</button>
        <button type="button">标记通过</button>
        <button type="button">返工到上游</button>
      </aside>
    </main>
  );
}
```

Create `apps/web/src/pages/AssetsPage.tsx`:

```tsx
export function AssetsPage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>资产页</h1>
      <section>
        <h2>人物资产</h2>
        <p>展示人物资产卡、四视图 Prompt 和生成图。</p>
      </section>
      <section>
        <h2>场景资产</h2>
        <p>展示场景资产卡、场景 Prompt 和生成图。</p>
      </section>
    </main>
  );
}
```

Create `apps/web/src/pages/VideoPromptPage.tsx`:

```tsx
export function VideoPromptPage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>VideoPrompt</h1>
      <p>按 sequence 和 shot 查看中文、英文与工具导出版。</p>
      <button type="button">视频任务包导出</button>
    </main>
  );
}
```

Create `apps/web/src/pages/ModelSettingsPage.tsx`:

```tsx
export function ModelSettingsPage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>模型配置</h1>
      <p>密钥状态：未解锁</p>
      <label>
        Base URL
        <input name="base_url" aria-label="Base URL" />
      </label>
      <label>
        Model
        <input name="model" aria-label="Model" />
      </label>
    </main>
  );
}
```

- [ ] **Step 4: Run frontend tests**

Run:

```bash
cd apps/web
npm test
```

Expected: all frontend tests pass.

- [ ] **Step 5: Commit**

```bash
git add apps/web/src/pages apps/web/src/components apps/web/src/__tests__/WorkbenchPages.test.tsx
git commit -m "feat: add workbench page skeletons"
```

---

### Task 12: Local Run Guide And Full Verification

**Files:**
- Create: `docs/web-workbench.md`
- Modify: `README.md` if it exists after this plan starts; if it does not exist, do not create it in this task.

- [ ] **Step 1: Write local run guide**

Create `docs/web-workbench.md`:

````markdown
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
````

- [ ] **Step 2: Run backend tests**

Run:

```bash
cd apps/api
python -m pytest -v
```

Expected: all backend tests pass.

- [ ] **Step 3: Run frontend tests**

Run:

```bash
cd apps/web
npm test
```

Expected: all frontend tests pass.

- [ ] **Step 4: Run frontend build**

Run:

```bash
cd apps/web
npm run build
```

Expected: TypeScript and Vite build complete successfully.

- [ ] **Step 5: Commit**

```bash
git add docs/web-workbench.md
git commit -m "docs: add web workbench run guide"
```

---

## Self-Review

Spec coverage:

- Local personal tool: covered by backend/frontend local structure and run guide.
- Semi-automatic Phase review: covered by Task 6 and Task 11.
- OpenAI-Compatible text/image configuration: covered by Task 7 and Task 8; model config persistence is represented by Task 2 and can be connected to routers during execution.
- Video task package priority: covered by Task 9.
- SQLite + output folder storage: covered by Task 2 and Task 3.
- Encrypted API keys: covered by Task 4.
- API/CLI dual executors: covered by Task 7.
- Final deliverables: preserved through storage directories, Phase flow, and run guide.

Implementation steps use explicit file paths, commands, and code blocks. Type names used across tasks are consistent: `Project`, `Phase`, `ModelConfig`, `Job`, `Generation`, `PhaseExecutor`, `ExecutionResult`, `PhaseRunner`.
