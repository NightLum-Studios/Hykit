from __future__ import annotations

import re
from dataclasses import dataclass


PLACEHOLDER_PATTERN = re.compile(r"\{[A-Z_]+\}")
DEFAULT_PROJECT_AUTHOR = "hykit"
PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]*[A-Za-z0-9]$|^[A-Za-z0-9]$")
AUTHOR_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._-]*[A-Za-z0-9]$|^[A-Za-z0-9]$")
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


@dataclass(frozen=True)
class ProjectName:
    raw: str
    tokens: tuple[str, ...]

    @property
    def lower(self) -> str:
        return "".join(token.lower() for token in self.tokens)

    @property
    def upper(self) -> str:
        return "".join(token.upper() for token in self.tokens)

    @property
    def snake(self) -> str:
        return "_".join(token.lower() for token in self.tokens)

    @property
    def kebab(self) -> str:
        return "-".join(token.lower() for token in self.tokens)

    @property
    def pascal(self) -> str:
        return "".join(token.capitalize() for token in self.tokens)


def normalize_author_name(author: str | None) -> str:
    if author is None:
        return DEFAULT_PROJECT_AUTHOR
    if not author:
        return DEFAULT_PROJECT_AUTHOR
    _validate_no_edge_whitespace(author, "Author name")
    _validate_common_name(author, "Author name", AUTHOR_NAME_PATTERN)
    return author


def normalize_project_name(name: str) -> str:
    if not name:
        raise ValueError("Project name cannot be empty.")
    _validate_no_edge_whitespace(name, "Project name")
    _validate_common_name(name, "Project name", PROJECT_NAME_PATTERN)
    if ".." in name:
        raise ValueError("Project name cannot contain '..'.")
    if name.endswith((".", " ")):
        raise ValueError("Project name cannot end with a dot or space.")
    if name.upper() in WINDOWS_RESERVED_NAMES:
        raise ValueError(f"Project name '{name}' is reserved on Windows.")
    return name


def _tokenize(name: str) -> tuple[str, ...]:
    tokens: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            tokens.append("".join(buffer))
            buffer.clear()

    prev = ""
    for ch in name:
        if not ch.isalnum():
            flush()
            prev = ""
            continue

        if prev and prev.islower() and ch.isupper():
            flush()
        elif prev and prev.isalpha() and ch.isdigit():
            flush()
        elif prev and prev.isdigit() and ch.isalpha():
            flush()

        buffer.append(ch)
        prev = ch

    flush()
    if not tokens:
        raise ValueError("Project name must contain alphanumeric characters.")
    return tuple(tokens)


def build_project_name(name: str) -> ProjectName:
    normalized = normalize_project_name(name)
    tokens = _tokenize(normalized)
    return ProjectName(raw=normalized, tokens=tokens)


def build_placeholders(name: str, author: str | None) -> dict[str, str]:
    project = build_project_name(name)
    normalized_author = normalize_author_name(author)
    return {
        "{PROJECT_NAME}": project.raw,
        "{PROJECT_NAME_LOWER}": project.lower,
        "{PROJECT_NAME_SNAKE}": project.snake,
        "{PROJECT_NAME_KEBAB}": project.kebab,
        "{PROJECT_NAME_PASCAL}": project.pascal,
        "{PROJECT_NAME_UPPER}": project.upper,
        "{PROJECT_AUTHOR}": normalized_author,
    }


def replace_placeholders(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text


def _validate_no_edge_whitespace(value: str, field_name: str) -> None:
    if value != value.strip():
        raise ValueError(f"{field_name} cannot start or end with whitespace.")


def _validate_common_name(value: str, field_name: str, pattern: re.Pattern[str]) -> None:
    if not any(ch.isalnum() for ch in value):
        raise ValueError(f"{field_name} must contain at least one letter or digit.")
    if any(ch in {"/", "\\", ":"} or ord(ch) < 32 for ch in value):
        raise ValueError(
            f"{field_name} contains invalid characters. Avoid slashes, colons, and control characters."
        )
    if not pattern.fullmatch(value):
        raise ValueError(
            f"{field_name} contains unsupported characters. Use letters, digits, spaces, '_' and '-'."
            if field_name == "Project name"
            else f"{field_name} contains unsupported characters. Use letters, digits, spaces, '.', '_' and '-'."
        )
