from fastapi import APIRouter


router = APIRouter(prefix="/api/projects/{project_id}/video-tasks", tags=["video-tasks"])


@router.get("/contract")
def video_task_contract() -> dict[str, list[str]]:
    return {"exports": ["video-tasks.json", "video-tasks.csv"], "provider_modes": ["task_package", "provider_adapter"]}
