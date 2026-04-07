from __future__ import annotations

from pathlib import Path

from .file_ops import copy_template, rename_paths, replace_in_text_files
from .placeholders import build_placeholders, build_project_name
from .template_loader import find_template_path


SUPPORTED_TEMPLATE_TYPES = {"Project"}


def create_project(
    name: str,
    template_type: str = "Project",
    destination_dir: Path | None = None,
    template_path: Path | None = None,
) -> Path:
    if template_type not in SUPPORTED_TEMPLATE_TYPES:
        raise ValueError(
            f"Unsupported template type '{template_type}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_TEMPLATE_TYPES))}."
        )

    project = build_project_name(name)
    destination_dir = destination_dir or Path.cwd()
    target_dir = destination_dir / project.raw

    if target_dir.exists():
        raise FileExistsError(f"Target directory already exists: {target_dir}")

    template_path = template_path or find_template_path()
    copy_template(template_path, target_dir)

    placeholders = build_placeholders(project.raw)
    rename_paths(target_dir, placeholders)
    replace_in_text_files(target_dir, placeholders)
    return target_dir
