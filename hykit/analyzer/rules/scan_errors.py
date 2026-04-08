from __future__ import annotations

from ..context import ProjectContext
from ..issues import Issue


def scan_errors_rule(context: ProjectContext) -> list[Issue]:
    issues: list[Issue] = []
    for error in context.errors_during_scan:
        issues.append(
            Issue(
                severity="warning",
                code="SCAN_ERROR",
                message=error.message,
                file=error.path,
            )
        )
    return issues
