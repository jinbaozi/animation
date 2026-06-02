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
