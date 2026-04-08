from __future__ import annotations

import os
import sys
from pathlib import Path

from .issues import Issue


class Reporter:
    RESET = "\033[0m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"

    def __init__(self, root_path: Path | None = None, enable_color: bool | None = None) -> None:
        self.root_path = root_path
        self.enable_color = self._supports_color() if enable_color is None else enable_color

    def render(self, issues: list[Issue]) -> str:
        if not issues:
            return self._colorize("Validation completed successfully.", self.GREEN)

        lines: list[str] = []
        for issue in issues:
            header = "[ERROR]" if issue.severity == "error" else "[WARNING]"
            color = self.RED if issue.severity == "error" else self.YELLOW
            lines.append(self._colorize(f"{header} {issue.code}", color))
            if issue.file:
                lines.append(f"  File: {self._format_path(issue.file)}")
            lines.append(f"  Message: {issue.message}")
            if issue.hint:
                lines.append(f"  Hint: {issue.hint}")
            lines.append("")

        errors = sum(1 for issue in issues if issue.severity == "error")
        warnings = sum(1 for issue in issues if issue.severity == "warning")
        summary = f"Validation completed: {errors} errors, {warnings} warnings."
        summary_color = self.RED if errors else self.YELLOW if warnings else self.GREEN
        lines.append(self._colorize(summary, summary_color))
        return "\n".join(lines).rstrip()

    def _format_path(self, path: Path) -> str:
        if self.root_path:
            try:
                relative = path.relative_to(self.root_path)
                return f".\\{relative.as_posix()}"
            except ValueError:
                return str(path)
        return str(path)

    def _colorize(self, text: str, color: str) -> str:
        if not self.enable_color:
            return text
        return f"{color}{text}{self.RESET}"

    def _supports_color(self) -> bool:
        if os.getenv("NO_COLOR"):
            return False
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False
        if os.name != "nt":
            return True
        return any(
            os.getenv(variable)
            for variable in ("WT_SESSION", "ANSICON", "ConEmuANSI", "TERM")
        )
