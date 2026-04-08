from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Iterable

from .placeholders import replace_placeholders


TEXT_EXTENSIONS = {
    ".py",
    ".json",
    ".toml",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
    ".ts",
    ".js",
    ".gradle",
    ".kts",
    ".properties",
    ".java",
    ".kt",
    ".xml",
}

TEXT_FILENAMES = {".gitignore"}


def copy_template(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination)


def iter_paths_depth_first(root: Path) -> Iterable[Path]:
    paths = list(root.rglob("*"))
    return sorted(paths, key=lambda p: len(p.parts), reverse=True)


def rename_paths(root: Path, mapping: dict[str, str]) -> None:
    for path in iter_paths_depth_first(root):
        new_name = replace_placeholders(path.name, mapping)
        if new_name == path.name:
            continue
        target = path.with_name(new_name)
        if target.exists():
            raise FileExistsError(f"Cannot rename {path} to {target}: target already exists.")
        path.rename(target)


def _is_text_file(path: Path) -> bool:
    if path.name in TEXT_FILENAMES:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def replace_in_text_files(root: Path, mapping: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if not _is_text_file(path):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Warning: skipped non-UTF-8 file {path}", file=sys.stderr)
            continue
        updated = replace_placeholders(original, mapping)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
