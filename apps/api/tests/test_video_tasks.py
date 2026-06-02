from pathlib import Path
import json

from app.services.video_tasks import export_video_tasks


def test_export_video_tasks_writes_json_and_csv(tmp_path: Path):
    project_dir = tmp_path / "demo"
    prompt_dir = project_dir / "05-Phase2b-Prompt"
    prompt_dir.mkdir(parents=True)
    (prompt_dir / "PromptExportIR.md").write_text(
        "shot_id: S001\nzh_prompt: 吴为拉开弓。\nen_prompt: Wu Wei draws the bow.\nreference_image: ../04-Phase2a-四视图/四视图预览/吴为.png\n",
        encoding="utf-8",
    )

    result = export_video_tasks(project_dir)

    data = json.loads(result.json_path.read_text(encoding="utf-8"))
    assert data[0]["shot_id"] == "S001"
    assert "Wu Wei draws the bow." in result.csv_path.read_text(encoding="utf-8")
