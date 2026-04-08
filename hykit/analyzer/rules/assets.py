from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from ..context import ProjectContext
from ..issues import Issue


ASSET_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".blockymodel",
    ".ui",
    ".wav",
    ".ogg",
    ".mp3",
    ".txt",
    ".lang",
    ".json",
    ".xml",
}


def missing_referenced_assets_rule(context: ProjectContext) -> list[Issue]:
    issues: list[Issue] = []
    seen: set[tuple[Path, str]] = set()
    for json_path in context.json_files:
        data = _load_json(json_path)
        if data is None:
            continue
        for value in iter_string_values(data):
            if not _looks_like_asset_path(value):
                continue
            key = (json_path, value)
            if key in seen:
                continue
            seen.add(key)
            if not _asset_exists(value, context.asset_paths):
                issues.append(
                    Issue(
                        severity="warning",
                        code="ASSET_REFERENCE_MISSING",
                        message=f"Referenced asset was not found: {value}",
                        file=json_path,
                        hint="Check that the file exists in the resources paths.",
                    )
                )
    return issues


def _load_json(path: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return None


def iter_string_values(data: object) -> Iterable[str]:
    if isinstance(data, dict):
        for value in data.values():
            yield from iter_string_values(value)
    elif isinstance(data, list):
        for item in data:
            yield from iter_string_values(item)
    elif isinstance(data, str):
        yield data


def _looks_like_asset_path(value: str) -> bool:
    if "://" in value or value.startswith(("http://", "https://")):
        return False
    if value.startswith(("@", "$", "#")):
        return False
    if value.strip() != value:
        return False

    suffix = Path(value).suffix.lower()
    if suffix in ASSET_EXTENSIONS:
        return True
    if "/" in value or "\\" in value:
        return bool(suffix)
    return False


def _asset_exists(value: str, base_paths: list[Path]) -> bool:
    for base in base_paths:
        candidate = base / value
        if candidate.exists():
            return True
    return False
