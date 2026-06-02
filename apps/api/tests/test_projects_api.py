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
