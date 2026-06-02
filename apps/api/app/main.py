from fastapi import FastAPI

from app.core.config import get_settings
from app.routers.projects import router as projects_router


def create_app() -> FastAPI:
    get_settings.cache_clear()
    app = FastAPI(title="animation-v3 local workbench")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    app.include_router(projects_router)

    return app


app = create_app()
