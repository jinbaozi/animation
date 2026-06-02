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
