from pathlib import Path

from app.core.database import create_sqlite_engine, init_db, session_scope
from app.models import Job, ModelConfig, Phase, Project


def test_project_phase_model_config_and_job_persist(tmp_path: Path):
    engine = create_sqlite_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)

    with session_scope(engine) as session:
        project = Project(name="demo", slug="demo", output_dir="output/demo")
        session.add(project)
        session.flush()

        phase = Phase(project_id=project.id, phase_id="phase1", status="pending")
        config = ModelConfig(
            name="local-compatible",
            provider_type="openai_compatible",
            modality="text",
            base_url="https://api.example.test/v1",
            model_name="demo-model",
            encrypted_key_id=None,
            default_params={"temperature": 0.4},
        )
        job = Job(project_id=project.id, phase_id="phase1", status="running", kind="phase")
        session.add_all([phase, config, job])

    with session_scope(engine) as session:
        saved = session.query(Project).filter_by(slug="demo").one()
        assert saved.phases[0].phase_id == "phase1"
        assert saved.phases[0].status == "pending"
        assert session.query(ModelConfig).one().default_params == {"temperature": 0.4}
        assert session.query(Job).one().kind == "phase"
