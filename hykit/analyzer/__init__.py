from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .context import ProjectContext
from .issues import Issue
from .scanner import ProjectScanner
from .rules import ALL_RULES


def build_context(root_path: Path) -> ProjectContext:
    scanner = ProjectScanner()
    return scanner.scan(root_path)


def run_rules(context: ProjectContext) -> list[Issue]:
    issues: list[Issue] = []
    for rule in ALL_RULES:
        issues.extend(rule(context))
    return issues


def validate_path(root_path: Path) -> list[Issue]:
    context = build_context(root_path)
    return run_rules(context)


def count_issues(issues: Iterable[Issue]) -> tuple[int, int]:
    errors = sum(1 for issue in issues if issue.severity == "error")
    warnings = sum(1 for issue in issues if issue.severity == "warning")
    return errors, warnings
