from fastapi import APIRouter


router = APIRouter(prefix="/api/projects/{project_id}/assets", tags=["assets"])


@router.get("/contract")
def asset_contract() -> dict[str, list[str]]:
    return {"asset_types": ["character", "scene"], "image_statuses": ["pending", "running", "done", "failed"]}
