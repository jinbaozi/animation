#!/usr/bin/env python3
"""Validate an animation-v3 project output package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN_PATTERN = re.compile(
    r"(?i)(影视|电影|摄像|胶片|摄影|古风写实|写实CG|游戏CG|影视质感|影视级|电影级)"
)


REQUIRED_FILES = [
    "00-项目配置/project-manifest.md",
    "01-Phase0-合规预审/合规预审报告.md",
    "02-Phase1-剧本分镜/StoryIR.md",
    "02-Phase1-剧本分镜/剧本.md",
    "02-Phase1-剧本分镜/基础分镜执行表.md",
    "02-Phase1-剧本分镜/人物清单.md",
    "02-Phase1-剧本分镜/场景清单.md",
    "03-Phase1.5-镜头序列/ShotIR.md",
    "03-Phase1.5-镜头序列/增强分镜执行表.md",
    "03-Phase1.5-镜头序列/序列衔接与继承表.md",
    "04-Phase2a-四视图/VisualAnchorIR.md",
    "04-Phase2a-四视图/人物资产卡.md",
    "04-Phase2a-四视图/场景资产卡.md",
    "04-Phase2a-四视图/人物四视图Prompt包.md",
    "05-Phase2b-Prompt/PromptExportIR.md",
    "05-Phase2b-Prompt/VideoPrompt包-中文版.md",
    "05-Phase2b-Prompt/VideoPrompt包-英文版.md",
]


FINAL_FILES = [
    "99-最终交付物/完整VideoPrompt包-中文版.md",
    "99-最终交付物/完整VideoPrompt包-英文版.md",
    "99-最终交付物/人物资产卡.md",
    "99-最终交付物/场景资产卡.md",
    "99-最终交付物/交付检查清单.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_exists(root: Path, files: list[str]) -> list[str]:
    missing = []
    for file_name in files:
        if not (root / file_name).is_file():
            missing.append(file_name)
    return missing


def check_forbidden(root: Path, files: list[str]) -> list[str]:
    violations = []
    for file_name in files:
        path = root / file_name
        if not path.is_file():
            continue
        match = FORBIDDEN_PATTERN.search(read_text(path))
        if match:
            violations.append(f"{file_name}: {match.group(0)}")
    return violations


def check_manifest_scope(root: Path) -> list[str]:
    path = root / "00-项目配置/project-manifest.md"
    if not path.is_file():
        return []
    text = read_text(path)
    required_terms = ["VideoPrompt", "人物资产卡", "场景资产卡"]
    return [term for term in required_terms if term not in text]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate required animation-v3 output files."
    )
    parser.add_argument("project_dir", help="Path to output/{project_name}")
    parser.add_argument(
        "--final",
        action="store_true",
        help="Also require files under 99-最终交付物/",
    )
    args = parser.parse_args()

    root = Path(args.project_dir).resolve()
    if not root.is_dir():
        print(f"ERROR: project directory does not exist: {root}")
        return 2

    required = REQUIRED_FILES + (FINAL_FILES if args.final else [])
    missing = check_exists(root, required)
    forbidden = check_forbidden(root, required)
    missing_scope = check_manifest_scope(root)

    if not missing and not forbidden and not missing_scope:
        print(f"PASS: {root}")
        return 0

    if missing:
        print("MISSING FILES:")
        for item in missing:
            print(f"- {item}")

    if missing_scope:
        print("MANIFEST DELIVERY SCOPE MISSING:")
        for item in missing_scope:
            print(f"- {item}")

    if forbidden:
        print("FORBIDDEN WORD VIOLATIONS:")
        for item in forbidden:
            print(f"- {item}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
