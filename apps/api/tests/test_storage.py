from pathlib import Path

from app.services.storage import PHASE_DIRS, create_project_structure, project_slug


def test_project_slug_normalizes_ascii_and_keeps_chinese():
    assert project_slug("开局一张弓 装备就变强!") == "开局一张弓-装备就变强"
    assert project_slug("Demo Project") == "demo-project"


def test_create_project_structure_writes_expected_dirs_and_novel(tmp_path: Path):
    result = create_project_structure(
        output_root=tmp_path,
        project_name="Demo Project",
        novel_filename="novel.txt",
        novel_content="第一章\n少年醒来。",
    )

    assert result.project_dir == tmp_path / "demo-project"
    assert (
        result.project_dir / "00-原始素材" / "novel.txt"
    ).read_text(encoding="utf-8") == "第一章\n少年醒来。"
    for relative_dir in PHASE_DIRS:
        assert (result.project_dir / relative_dir).is_dir()
