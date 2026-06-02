from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Protocol

import httpx


PHASE_OUTPUTS = {
    "phase1": ("02-Phase1-剧本分镜", "StoryIR.md", "StoryIR"),
}


def _phase_output_mapping(phase_id: str) -> tuple[str, str, str]:
    if phase_id not in PHASE_OUTPUTS:
        raise ValueError(f"unsupported phase output mapping: {phase_id}")
    return PHASE_OUTPUTS[phase_id]


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
        directory, filename, label = _phase_output_mapping(phase_id)
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
    def __init__(self, repo_root: Path, script_path: str, project_name: str, timeout: int = 300):
        self.repo_root = repo_root
        self.script_path = script_path
        self.project_name = project_name
        self.timeout = timeout

    def run_phase(self, project_dir: Path, phase_id: str) -> ExecutionResult:
        directory, filename, label = _phase_output_mapping(phase_id)
        completed = subprocess.run(
            [str(self.repo_root / self.script_path), f"--project={self.project_name}", f"--phase={phase_id}"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=self.timeout,
        )
        output_path = project_dir / directory / filename
        return ExecutionResult(output_files={label: str(output_path)}, log_excerpt=completed.stdout[-2000:])
