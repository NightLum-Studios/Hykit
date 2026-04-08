from __future__ import annotations

from pathlib import Path

from ..context import ProjectContext
from ..issues import Issue


def build_files_missing_rule(context: ProjectContext) -> list[Issue]:
    module_root = context.module_root
    module_files = {
        path.relative_to(module_root).as_posix()
        for path in context.all_files
        if _is_direct_child(path, module_root)
    }
    has_groovy_pair = {"build.gradle", "settings.gradle"}.issubset(module_files)
    has_kts_pair = {"build.gradle.kts", "settings.gradle.kts"}.issubset(module_files)
    if has_groovy_pair or has_kts_pair:
        return []

    return [
        Issue(
            severity="warning",
            code="BUILD_FILES_MISSING",
            message="Gradle build files are missing or incomplete.",
            file=module_root,
            hint="Expected either build.gradle + settings.gradle or build.gradle.kts + settings.gradle.kts in the project root.",
        )
    ]


def gradle_wrapper_missing_rule(context: ProjectContext) -> list[Issue]:
    module_root = context.module_root
    required_paths = (
        module_root / "gradlew",
        module_root / "gradlew.bat",
        module_root / "gradle" / "wrapper",
    )
    if all(path.exists() for path in required_paths):
        return []

    return [
        Issue(
            severity="warning",
            code="GRADLE_WRAPPER_MISSING",
            message="Gradle wrapper files are missing.",
            file=module_root,
            hint="Include gradlew, gradlew.bat, and gradle/wrapper for portable builds.",
        )
    ]


def _is_direct_child(path: Path, module_root: Path) -> bool:
    try:
        relative = path.relative_to(module_root)
    except ValueError:
        return False
    return len(relative.parts) == 1
