from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .context import ProjectContext, ScanError

IGNORED_DIRECTORIES = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    ".gradle",
    "build",
    "dist",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


class ProjectScanner:
    def scan(self, root_path: Path) -> ProjectContext:
        root = root_path.resolve()
        errors: list[ScanError] = []

        all_files: list[Path] = []
        json_files: list[Path] = []
        java_files: list[Path] = []
        try:
            for current_root, dirs, files in os.walk(root, topdown=True, followlinks=False):
                dirs[:] = [directory for directory in dirs if directory not in IGNORED_DIRECTORIES]
                current_path = Path(current_root)
                for filename in files:
                    path = current_path / filename
                    all_files.append(path)
                    if path.suffix.lower() == ".json":
                        json_files.append(path)
                    if path.suffix.lower() == ".java":
                        java_files.append(path)
        except OSError as exc:
            errors.append(ScanError(f"Failed to scan project files: {exc}", root))

        manifest_path = self._find_manifest_path(root, all_files, errors)
        module_root = self._resolve_module_root(root, manifest_path)
        manifest_data: dict[str, Any] | None = None
        if manifest_path is not None:
            try:
                manifest_data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(ScanError(f"Failed to read manifest.json: {exc}", manifest_path))
                manifest_data = None

        asset_paths = [
            root,
            module_root,
            root / "resources",
            root / "resources" / "Common",
            root / "resources" / "Server",
            root / "src" / "main" / "resources",
            module_root / "resources",
            module_root / "resources" / "Common",
            module_root / "resources" / "Server",
            module_root / "src" / "main" / "resources",
        ]

        return ProjectContext(
            root_path=root,
            module_root=module_root,
            manifest_path=manifest_path,
            manifest_data=manifest_data,
            all_files=all_files,
            json_files=json_files,
            java_files=java_files,
            asset_paths=asset_paths,
            errors_during_scan=errors,
        )

    def _find_manifest_path(
        self,
        root: Path,
        all_files: list[Path],
        errors: list[ScanError],
    ) -> Path | None:
        file_set = set(all_files)
        for candidate in (
            root / "manifest.json",
            root / "src" / "main" / "resources" / "manifest.json",
        ):
            if candidate in file_set:
                return candidate

        nested_candidates = []
        for path in all_files:
            try:
                relative = path.relative_to(root)
            except ValueError:
                continue
            if len(relative.parts) == 5 and tuple(relative.parts[1:]) == (
                "src",
                "main",
                "resources",
                "manifest.json",
            ):
                nested_candidates.append(path)
        nested_candidates.sort()
        if len(nested_candidates) == 1:
            return nested_candidates[0]
        if len(nested_candidates) > 1:
            errors.append(
                ScanError(
                    "Multiple manifest.json files were found in nested project directories.",
                    root,
                )
            )
        return None

    def _resolve_module_root(self, root: Path, manifest_path: Path | None) -> Path:
        if manifest_path is None:
            return root
        resources_manifest = Path("src/main/resources/manifest.json")
        try:
            manifest_path.relative_to(root / resources_manifest)
            return root
        except ValueError:
            pass
        if len(manifest_path.parts) >= 4 and tuple(manifest_path.parts[-4:]) == (
            "src",
            "main",
            "resources",
            "manifest.json",
        ):
            return manifest_path.parents[3]
        return manifest_path.parent
