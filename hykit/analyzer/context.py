from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ScanError:
    message: str
    path: Path | None = None


@dataclass(frozen=True)
class ProjectContext:
    root_path: Path
    module_root: Path
    manifest_path: Path | None
    manifest_data: dict[str, Any] | None
    all_files: list[Path] = field(default_factory=list)
    json_files: list[Path] = field(default_factory=list)
    java_files: list[Path] = field(default_factory=list)
    asset_paths: list[Path] = field(default_factory=list)
    errors_during_scan: list[ScanError] = field(default_factory=list)
