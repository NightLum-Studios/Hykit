from __future__ import annotations

import re
from pathlib import Path

from ..context import ProjectContext
from ..issues import Issue


PACKAGE_PATTERN = re.compile(r"^\s*package\s+([A-Za-z_][\w.]*)\s*;", re.MULTILINE)
CLASS_PATTERN = re.compile(
    r"^\s*(?:public\s+)?(?:final\s+|abstract\s+)?class\s+([A-Za-z_]\w*)\b",
    re.MULTILINE,
)


def manifest_main_missing_rule(context: ProjectContext) -> list[Issue]:
    if context.manifest_path is None or context.manifest_data is None:
        return []
    if not isinstance(context.manifest_data, dict):
        return []

    main_value = context.manifest_data.get("Main")
    if not isinstance(main_value, str) or not main_value.strip():
        return [
            Issue(
                severity="error",
                code="MANIFEST_MAIN_MISSING",
                message='manifest.json does not contain a valid "Main" entry.',
                file=context.manifest_path,
                hint='Add a non-empty "Main" field pointing to the plugin main class.',
            )
        ]
    return []


def main_class_missing_rule(context: ProjectContext) -> list[Issue]:
    main_entry = _get_main_entry(context)
    if main_entry is None:
        return []

    expected_path = _main_class_path(context.module_root, main_entry)
    if expected_path is None or expected_path.exists():
        return []

    return [
        Issue(
            severity="error",
            code="MAIN_CLASS_MISSING",
            message=f"Main class file was not found for '{main_entry}'.",
            file=expected_path,
            hint="Ensure that the main plugin class exists at the expected Java source path.",
        )
    ]


def main_class_package_mismatch_rule(context: ProjectContext) -> list[Issue]:
    main_entry = _get_main_entry(context)
    if main_entry is None:
        return []

    expected_path = _main_class_path(context.module_root, main_entry)
    if expected_path is None or not expected_path.exists():
        return []

    try:
        contents = expected_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [
            Issue(
                severity="error",
                code="MAIN_CLASS_PACKAGE_MISMATCH",
                message=f"Could not read main class file: {exc}",
                file=expected_path,
                hint="Make sure manifest.json Main matches the Java package and class declaration.",
            )
        ]

    package_match = PACKAGE_PATTERN.search(contents)
    class_match = CLASS_PATTERN.search(contents)
    if package_match is None or class_match is None:
        return [
            Issue(
                severity="error",
                code="MAIN_CLASS_PACKAGE_MISMATCH",
                message="Could not determine Java package or class declaration for the main class.",
                file=expected_path,
                hint="Make sure manifest.json Main matches the Java package and class declaration.",
            )
        ]

    declared_main = f"{package_match.group(1)}.{class_match.group(1)}"
    if declared_main == main_entry:
        return []

    return [
        Issue(
            severity="error",
            code="MAIN_CLASS_PACKAGE_MISMATCH",
            message=(
                f'manifest.json Main is "{main_entry}", but the Java file declares '
                f'"{declared_main}".'
            ),
            file=expected_path,
            hint="Make sure manifest.json Main matches the Java package and class declaration.",
        )
    ]


def _get_main_entry(context: ProjectContext) -> str | None:
    if context.manifest_data is None or not isinstance(context.manifest_data, dict):
        return None
    main_value = context.manifest_data.get("Main")
    if not isinstance(main_value, str):
        return None
    main_value = main_value.strip()
    if not main_value:
        return None
    return main_value


def _main_class_path(module_root: Path, main_entry: str) -> Path | None:
    parts = main_entry.split(".")
    if len(parts) < 2:
        return None
    return module_root / "src" / "main" / "java" / Path(*parts).with_suffix(".java")
