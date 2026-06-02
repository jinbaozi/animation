from dataclasses import dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class VideoTaskExport:
    json_path: Path
    csv_path: Path


def _parse_simple_prompt_export(content: str) -> list[dict[str, str]]:
    current: dict[str, str] = {}
    for line in content.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current[key.strip()] = value.strip()
    return [{
        "shot_id": current.get("shot_id", "S001"),
        "zh_prompt": current.get("zh_prompt", ""),
        "en_prompt": current.get("en_prompt", ""),
        "reference_image": current.get("reference_image", ""),
        "duration_seconds": "15",
        "aspect_ratio": "9:16",
        "target_tool": "generic-video-task-package",
    }]


def export_video_tasks(project_dir: Path) -> VideoTaskExport:
    prompt_export = project_dir / "05-Phase2b-Prompt" / "PromptExportIR.md"
    tasks = _parse_simple_prompt_export(prompt_export.read_text(encoding="utf-8"))
    export_dir = project_dir / "05-Phase2b-Prompt" / "ToolExport"
    export_dir.mkdir(parents=True, exist_ok=True)

    json_path = export_dir / "video-tasks.json"
    csv_path = export_dir / "video-tasks.csv"
    json_path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(tasks[0].keys()))
        writer.writeheader()
        writer.writerows(tasks)

    return VideoTaskExport(json_path=json_path, csv_path=csv_path)
