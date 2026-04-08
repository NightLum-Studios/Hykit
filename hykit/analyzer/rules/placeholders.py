from __future__ import annotations

from pathlib import Path

from ...placeholders import PLACEHOLDER_PATTERN
from ..context import ProjectContext
from ..issues import Issue


TEXT_EXTENSIONS = {".java", ".gradle", ".kts", ".json", ".properties", ".md"}


def java_package_placeholder_leak_rule(context: ProjectContext) -> list[Issue]:
    issues: list[Issue] = []
    for path in context.all_files:
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue

        matches = sorted(set(PLACEHOLDER_PATTERN.findall(content)))
        for placeholder in matches:
            issues.append(
                Issue(
                    severity="error",
                    code="JAVA_PACKAGE_PLACEHOLDER_LEAK",
                    message=f"Unreplaced template placeholder found: {placeholder}",
                    file=path,
                    hint="Replace all template placeholders before building or validating the project.",
                )
            )
    return issues
