from __future__ import annotations

import tempfile
from pathlib import Path

from .file_ops import copy_template, rename_paths, replace_in_text_files
from .placeholders import build_placeholders, build_project_name, normalize_author_name
from .template_loader import find_template_path


SUPPORTED_TEMPLATE_TYPES = {"project"}


def create_project(
    name: str,
    author: str | None = None,
    template_type: str = "project",
    destination_dir: Path | None = None,
    template_path: Path | None = None,
) -> Path:
    normalized_template_type = template_type.strip().lower()
    if normalized_template_type not in SUPPORTED_TEMPLATE_TYPES:
        raise ValueError(
            f"Unsupported template type '{template_type}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_TEMPLATE_TYPES))}."
        )

    project = build_project_name(name)
    normalized_author = normalize_author_name(author)
    destination_dir = destination_dir or Path.cwd()
    if not destination_dir.exists() or not destination_dir.is_dir():
        raise FileNotFoundError(f"Destination directory does not exist: {destination_dir}")
    target_dir = destination_dir / project.raw

    if target_dir.exists():
        raise FileExistsError(f"Target directory already exists: {target_dir}")

    template_path = template_path or find_template_path()
    placeholders = build_placeholders(project.raw, normalized_author)

    with tempfile.TemporaryDirectory(prefix=".hykit-", dir=destination_dir) as temp_dir:
        staging_root = Path(temp_dir) / project.raw
        copy_template(template_path, staging_root)
        rename_paths(staging_root, placeholders)
        replace_in_text_files(staging_root, placeholders)
        staging_root.replace(target_dir)
    return target_dir
