from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .analyzer import count_issues, validate_path
from .analyzer.reporter import Reporter
from .placeholders import DEFAULT_PROJECT_AUTHOR
from .scaffold import create_project


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hykit",
        description="CLI tool for scaffolding Hytale project templates.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new project from template")
    create_parser.add_argument("template_type", help="Template type (use 'project')")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("author", nargs="?", help="Project author")

    validate_parser = subparsers.add_parser("validate", help="Validate an existing project")
    validate_parser.add_argument("path", nargs="?", default=".", help="Project path (default: current directory)")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "create":
        try:
            if args.author is None:
                print(
                    f"Warning: author name was not provided. Using '{DEFAULT_PROJECT_AUTHOR}'.",
                    file=sys.stderr,
                )
            target = create_project(args.name, args.author, template_type=args.template_type)
        except (ValueError, FileExistsError, FileNotFoundError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"Project created at {target}")
        issues = validate_path(target)
        reporter = Reporter(root_path=target.resolve())
        print(reporter.render(issues))
        errors, _warnings = count_issues(issues)
        return 1 if errors > 0 else 0
    if args.command == "validate":
        root = Path(args.path)
        issues = validate_path(root)
        reporter = Reporter(root_path=root.resolve())
        print(reporter.render(issues))
        errors, _warnings = count_issues(issues)
        return 1 if errors > 0 else 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
