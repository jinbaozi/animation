from pathlib import Path
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import create_app
from app.routers import projects as projects_router


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


def test_create_and_list_project_with_in_memory_database(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ANIMATION_V3_OUTPUT_ROOT", str(tmp_path / "output"))
    monkeypatch.setenv("ANIMATION_V3_DATABASE_URL", "sqlite:///:memory:")

    client = TestClient(create_app())

    create_response = client.post(
        "/api/projects",
        files={"novel": ("novel.txt", "第一章\n少年醒来。", "text/plain")},
        data={"name": "Memory Project", "style": "", "target_platform": ""},
    )
    list_response = client.get("/api/projects")

    assert create_response.status_code == 201
    assert list_response.status_code == 200
    assert list_response.json()[0]["slug"] == "memory-project"


def test_create_project_rejects_invalid_utf8_upload(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ANIMATION_V3_OUTPUT_ROOT", str(tmp_path / "output"))
    monkeypatch.setenv("ANIMATION_V3_DATABASE_URL", f"sqlite:///{tmp_path / 'workbench.db'}")

    client = TestClient(create_app(), raise_server_exceptions=False)

    response = client.post(
        "/api/projects",
        files={"novel": ("novel.txt", b"\xff\xfe\x00", "text/plain")},
        data={"name": "Bad Encoding", "style": "", "target_platform": ""},
    )

    assert response.status_code == 400
    assert "UTF-8" in response.json()["detail"]
    assert not (tmp_path / "output" / "bad-encoding").exists()


def test_create_project_removes_output_dir_when_db_commit_fails(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.setenv("ANIMATION_V3_OUTPUT_ROOT", str(tmp_path / "output"))
    monkeypatch.setenv("ANIMATION_V3_DATABASE_URL", f"sqlite:///{tmp_path / 'workbench.db'}")

    original_session_scope = projects_router.session_scope
    call_count = 0

    @contextmanager
    def failing_second_session_scope(engine):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            with original_session_scope(engine) as session:
                yield session
            return

        session = Session(engine)
        try:
            yield session
            raise RuntimeError("simulated db commit failure")
        finally:
            session.rollback()
            session.close()

    monkeypatch.setattr(projects_router, "session_scope", failing_second_session_scope)
    client = TestClient(create_app(), raise_server_exceptions=False)

    response = client.post(
        "/api/projects",
        files={"novel": ("novel.txt", "第一章\n少年醒来。", "text/plain")},
        data={"name": "Cleanup Project", "style": "", "target_platform": ""},
    )

    assert response.status_code == 500
    assert not (tmp_path / "output" / "cleanup-project").exists()
