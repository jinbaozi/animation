from fastapi import APIRouter


router = APIRouter(prefix="/api/projects/{project_id}/phases", tags=["phases"])


@router.get("")
def list_phase_contract() -> dict[str, list[str]]:
    return {
        "phases": ["g0", "phase0", "phase1", "phase1_5", "phase2a", "phase2b", "audit_gate", "final"],
        "statuses": ["pending", "running", "needs_review", "approved", "stale"],
    }
