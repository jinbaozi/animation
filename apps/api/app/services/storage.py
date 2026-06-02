from dataclasses import dataclass
from pathlib import Path
import re


PHASE_DIRS = [
    "00-项目配置",
    "00-原始素材",
    "01-Phase0-合规预审",
    "02-Phase1-剧本分镜",
    "03-Phase1.5-镜头序列",
    "04-Phase2a-四视图",
    "04-Phase2a-四视图/四视图预览",
    "04-Phase2a-四视图/场景预览",
    "05-Phase2b-Prompt",
    "05-Phase2b-Prompt/ToolExport",
    "06-Audit-Gate",
    "99-最终交付物",
]


@dataclass(frozen=True)
class ProjectStructure:
    slug: str
    project_dir: Path
    novel_path: Path


def project_slug(name: str) -> str:
    lowered = name.strip().lower()
    replaced = re.sub(r"\s+", "-", lowered)
    cleaned = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "", replaced)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    if not cleaned:
        raise ValueError(
            "project name must contain at least one letter, number, or Chinese character"
        )
    return cleaned


def create_project_structure(
    output_root: Path,
    project_name: str,
    novel_filename: str,
    novel_content: str,
) -> ProjectStructure:
    slug = project_slug(project_name)
    project_dir = output_root / slug
    if project_dir.exists():
        raise FileExistsError(f"project directory already exists: {project_dir}")

    for relative_dir in PHASE_DIRS:
        (project_dir / relative_dir).mkdir(parents=True, exist_ok=True)

    basename = Path(novel_filename).name
    safe_filename = "novel.txt" if basename in {"", ".", ".."} else basename
    novel_path = project_dir / "00-原始素材" / safe_filename
    novel_path.write_text(novel_content, encoding="utf-8")

    return ProjectStructure(slug=slug, project_dir=project_dir, novel_path=novel_path)
