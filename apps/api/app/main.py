from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="animation-v3 local workbench")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "animation-v3-api"}

    return app


app = create_app()
