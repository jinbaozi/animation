from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.core.database import create_sqlite_engine, init_db, session_scope
from app.models import Phase, Project
from app.schemas import ProjectResponse
from app.services.storage import create_project_structure, project_slug


router = APIRouter(prefix="/api/projects", tags=["projects"])

PHASE_IDS = [
    "g0",
    "phase0",
    "phase1",
    "phase1_5",
    "phase2a",
    "phase2b",
    "audit_gate",
    "final",
]


def get_engine():
    settings = get_settings()
    engine = create_sqlite_engine(settings.database_url)
    init_db(engine)
    return engine


@router.get("", response_model=list[ProjectResponse])
def list_projects() -> list[ProjectResponse]:
    engine = get_engine()
    with session_scope(engine) as session:
        projects = session.query(Project).order_by(Project.updated_at.desc()).all()
        return [ProjectResponse.model_validate(project) for project in projects]


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    name: str = Form(...),
    style: str = Form(""),
    target_platform: str = Form(""),
    novel: UploadFile = File(...),
) -> ProjectResponse:
    engine = get_engine()
    try:
        slug = project_slug(name)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    with session_scope(engine) as session:
        if session.query(Project).filter_by(slug=slug).first() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="project already exists",
            )

    settings = get_settings()
    content = (await novel.read()).decode("utf-8")
    try:
        structure = create_project_structure(
            output_root=settings.resolved_output_root,
            project_name=name,
            novel_filename=novel.filename or "novel.txt",
            novel_content=content,
        )
    except FileExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    manifest_path = structure.project_dir / "00-项目配置" / "project-manifest.md"
    manifest_path.write_text(
        "\n".join(
            [
                "# Project Manifest",
                "",
                f"- Project name: {name}",
                f"- Style: {style}",
                f"- Target platform: {target_platform}",
                "- Delivery scope: AI animation drama VideoPrompt workflow",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    try:
        with session_scope(engine) as session:
            project = Project(
                name=name,
                slug=structure.slug,
                output_dir=str(Path(structure.project_dir)),
                current_phase="g0",
            )
            session.add(project)
            session.flush()
            session.add_all(
                [
                    Phase(
                        project_id=project.id,
                        phase_id=phase_id,
                        status="pending",
                    )
                    for phase_id in PHASE_IDS
                ]
            )
            session.flush()
            session.refresh(project)
            return ProjectResponse.model_validate(project)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="project already exists",
        ) from exc
