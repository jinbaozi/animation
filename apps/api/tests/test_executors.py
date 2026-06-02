from pathlib import Path
import os
import shutil
import subprocess

import httpx
import pytest

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
    calls = []

    def fake_run(command, cwd, capture_output, text, check, timeout):
        calls.append(
            {
                "command": command,
                "cwd": cwd,
                "capture_output": capture_output,
                "text": text,
                "check": check,
                "timeout": timeout,
            }
        )
        output = tmp_path / "02-Phase1-剧本分镜" / "StoryIR.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("# StoryIR\nCLI", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    executor = CliPhaseExecutor(repo_root=tmp_path, script_path="scripts/orchestrate.sh", project_name="demo")

    result = executor.run_phase(tmp_path, "phase1")

    assert result.log_excerpt == "ok"
    assert result.output_files["StoryIR"].endswith("StoryIR.md")
    assert calls == [
        {
            "command": [str(tmp_path / "scripts/orchestrate.sh"), "--project=demo", "--phase=phase1"],
            "cwd": tmp_path,
            "capture_output": True,
            "text": True,
            "check": True,
            "timeout": 300,
        }
    ]


def test_api_phase_executor_rejects_unsupported_phase_before_http(tmp_path: Path):
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("HTTP request should not be sent")

    executor = ApiPhaseExecutor(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://api.example.test/v1",
        api_key="sk-test",
        model_name="demo-model",
    )

    with pytest.raises(ValueError, match="unsupported phase output mapping: phase2a"):
        executor.run_phase(tmp_path, "phase2a")


def test_cli_phase_executor_rejects_unsupported_phase_before_subprocess(tmp_path: Path, monkeypatch):
    def fake_run(*args, **kwargs):
        raise AssertionError("subprocess should not be called")

    monkeypatch.setattr(subprocess, "run", fake_run)
    executor = CliPhaseExecutor(repo_root=tmp_path, script_path="scripts/orchestrate.sh", project_name="demo")

    with pytest.raises(ValueError, match="unsupported phase output mapping: phase2a"):
        executor.run_phase(tmp_path, "phase2a")


def test_orchestrate_script_dispatches_single_phase(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[3]
    script_path = tmp_path / "orchestrate.sh"
    shutil.copy(repo_root / "scripts/orchestrate.sh", script_path)
    script_path.chmod(0o755)

    project = "demo"
    input_dir = tmp_path / "input" / project
    output_dir = tmp_path / "output" / project / "01-Phase0-合规预审"
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)
    (input_dir / "novel.txt").write_text("story", encoding="utf-8")
    (output_dir / "合规预审报告.md").write_text("pass", encoding="utf-8")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    claude = bin_dir / "claude"
    claude.write_text("#!/bin/sh\necho stub-claude\n", encoding="utf-8")
    claude.chmod(0o755)

    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}
    completed = subprocess.run(
        [str(script_path), f"--project={project}", "--phase=phase1"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    assert "Phase 1" in completed.stdout
    assert "Phase 0" not in completed.stdout


def test_orchestrate_script_rejects_unknown_phase(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[3]
    script_path = tmp_path / "orchestrate.sh"
    shutil.copy(repo_root / "scripts/orchestrate.sh", script_path)
    script_path.chmod(0o755)

    completed = subprocess.run(
        [str(script_path), "--project=demo", "--phase=unknown"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "unsupported phase: unknown" in completed.stdout
