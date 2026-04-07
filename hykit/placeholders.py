from __future__ import annotations

import re
from dataclasses import dataclass


PLACEHOLDER_PATTERN = re.compile(r"\{[A-Z_]+\}")


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


def normalize_project_name(name: str) -> str:
    normalized = name.strip()
    if not normalized:
        raise ValueError("Project name cannot be empty.")
    if not any(ch.isalnum() for ch in normalized):
        raise ValueError("Project name must contain at least one letter or digit.")
    return normalized


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


def build_placeholders(name: str) -> dict[str, str]:
    project = build_project_name(name)
    return {
        "{PROJECT_NAME}": project.raw,
        "{PROJECT_NAME_LOWER}": project.lower,
        "{PROJECT_NAME_SNAKE}": project.snake,
        "{PROJECT_NAME_KEBAB}": project.kebab,
        "{PROJECT_NAME_PASCAL}": project.pascal,
        "{PROJECT_NAME_UPPER}": project.upper,
    }


def replace_placeholders(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text
