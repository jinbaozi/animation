from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import create_sqlite_engine, init_db
from app.routers.assets import router as assets_router
from app.routers.phases import router as phases_router
from app.routers.projects import router as projects_router
from app.routers.video_tasks import router as video_tasks_router


def create_app() -> FastAPI:
    get_settings.cache_clear()
    settings = get_settings()
    engine = create_sqlite_engine(settings.database_url)
    init_db(engine)

    app = FastAPI(title="animation-v3 local workbench")
    app.state.engine = engine

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    app.include_router(projects_router)
    app.include_router(phases_router)
    app.include_router(assets_router)
    app.include_router(video_tasks_router)

    return app


app = create_app()
