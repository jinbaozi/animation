from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    name: str
    slug: str
    output_dir: str
    current_phase: str

    model_config = {"from_attributes": True}
