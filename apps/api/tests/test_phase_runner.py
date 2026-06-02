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
