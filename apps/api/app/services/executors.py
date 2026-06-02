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
