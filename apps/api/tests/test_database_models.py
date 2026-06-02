from pathlib import Path
from time import sleep

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.database import create_sqlite_engine, init_db, session_scope
from app.models import Generation, Job, ModelConfig, Phase, Project


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


def test_json_dict_columns_persist_in_place_updates(tmp_path: Path):
    engine = create_sqlite_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)

    with session_scope(engine) as session:
        project = Project(name="demo", slug="demo", output_dir="output/demo")
        session.add(project)
        session.flush()

        phase = Phase(
            project_id=project.id,
            phase_id="phase1",
            output_files={"draft": "phase1.md"},
            validation={"score": 0.5},
        )
        config = ModelConfig(
            name="local-compatible",
            provider_type="openai_compatible",
            modality="text",
            base_url="https://api.example.test/v1",
            model_name="demo-model",
            default_params={"temperature": 0.4},
        )
        generation = Generation(
            project_id=project.id,
            kind="storyboard",
            source_prompt="prompt",
            params={"seed": 7},
        )
        session.add_all([phase, config, generation])

    with session_scope(engine) as session:
        phase = session.query(Phase).one()
        config = session.query(ModelConfig).one()
        generation = session.query(Generation).one()

        phase.output_files["final"] = "phase1-final.md"
        phase.validation["approved"] = True
        config.default_params["top_p"] = 0.9
        generation.params["steps"] = 24

    with session_scope(engine) as session:
        phase = session.query(Phase).one()
        assert phase.output_files == {
            "draft": "phase1.md",
            "final": "phase1-final.md",
        }
        assert phase.validation == {"score": 0.5, "approved": True}
        assert session.query(ModelConfig).one().default_params == {
            "temperature": 0.4,
            "top_p": 0.9,
        }
        assert session.query(Generation).one().params == {"seed": 7, "steps": 24}


def test_updated_at_changes_when_project_or_phase_updates(tmp_path: Path):
    engine = create_sqlite_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)

    with session_scope(engine) as session:
        project = Project(name="demo", slug="demo", output_dir="output/demo")
        session.add(project)
        session.flush()
        phase = Phase(project_id=project.id, phase_id="phase1", status="pending")
        session.add(phase)

    with session_scope(engine) as session:
        project = session.query(Project).one()
        phase = session.query(Phase).one()
        original_project_updated_at = project.updated_at
        original_phase_updated_at = phase.updated_at

    sleep(0.01)

    with session_scope(engine) as session:
        session.query(Project).one().name = "demo updated"
        session.query(Phase).one().status = "complete"

    with session_scope(engine) as session:
        project = session.query(Project).one()
        phase = session.query(Phase).one()
        assert project.updated_at != original_project_updated_at
        assert phase.updated_at != original_phase_updated_at


def test_sqlite_foreign_keys_are_enforced(tmp_path: Path):
    engine = create_sqlite_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)

    with pytest.raises(IntegrityError):
        with session_scope(engine) as session:
            session.add(Phase(project_id=999, phase_id="phase1", status="pending"))
