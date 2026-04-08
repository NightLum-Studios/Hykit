from __future__ import annotations

import json

from ..context import ProjectContext
from ..issues import Issue


def json_files_valid_rule(context: ProjectContext) -> list[Issue]:
    issues: list[Issue] = []
    for path in context.json_files:
        if context.manifest_path and path == context.manifest_path:
            if context.manifest_data is None:
                continue
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, OSError) as exc:
            issues.append(
                Issue(
                    severity="error",
                    code="JSON_INVALID",
                    message=f"Invalid JSON: {exc}",
                    file=path,
                    hint="Fix JSON syntax errors in this file.",
                )
            )
    return issues
