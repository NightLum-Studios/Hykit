from __future__ import annotations

import argparse
import sys

from .scaffold import create_project


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hykit",
        description="CLI tool for scaffolding Hytale project templates.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new project from template")
    create_parser.add_argument("template_type", help="Template type (only 'Project' is supported)")
    create_parser.add_argument("name", help="Project name")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "create":
        try:
            target = create_project(args.name, template_type=args.template_type)
        except (ValueError, FileExistsError, FileNotFoundError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"Project created at {target}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
