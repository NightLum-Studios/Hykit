from __future__ import annotations

from ..context import ProjectContext
from ..issues import Issue

REQUIRED_MANIFEST_FIELDS = (
    "Group",
    "Name",
    "Version",
    "Description",
    "Authors",
    "Website",
    "DisabledByDefault",
    "IncludesAssetPack",
    "Dependencies",
    "OptionalDependencies",
    "ServerVersion",
    "Main",
)


def manifest_exists_rule(context: ProjectContext) -> list[Issue]:
    if context.manifest_path is None:
        return [
            Issue(
                severity="error",
                code="MANIFEST_MISSING",
                message="manifest.json was not found in the expected project locations.",
                file=context.root_path / "manifest.json",
                hint="Create a valid manifest.json in the project root or src/main/resources.",
            )
        ]
    return []


def manifest_valid_json_rule(context: ProjectContext) -> list[Issue]:
    if context.manifest_path is None:
        return []
    if context.manifest_data is None:
        return [
            Issue(
                severity="error",
                code="MANIFEST_INVALID_JSON",
                message="manifest.json could not be parsed as JSON.",
                file=context.manifest_path,
                hint="Fix JSON syntax errors in manifest.json.",
            )
        ]
    return []


def includes_asset_pack_rule(context: ProjectContext) -> list[Issue]:
    if context.manifest_path is None or context.manifest_data is None:
        return []

    if not isinstance(context.manifest_data, dict):
        return [
            Issue(
                severity="error",
                code="MANIFEST_INVALID_ASSET_PACK",
                message="manifest.json root must be a JSON object.",
                file=context.manifest_path,
            )
        ]

    if "IncludesAssetPack" not in context.manifest_data:
        return [
            Issue(
                severity="warning",
                code="MANIFEST_MISSING_ASSET_PACK",
                message="IncludesAssetPack is missing.",
                file=context.manifest_path,
                hint="Add IncludesAssetPack if this project uses asset packs.",
            )
        ]

    value = context.manifest_data.get("IncludesAssetPack")
    if not isinstance(value, bool):
        return [
            Issue(
                severity="error",
                code="MANIFEST_INVALID_ASSET_PACK",
                message="IncludesAssetPack must be a boolean.",
                file=context.manifest_path,
                hint="Set IncludesAssetPack to true or false.",
            )
        ]

    return []


def manifest_required_fields_rule(context: ProjectContext) -> list[Issue]:
    if context.manifest_path is None or context.manifest_data is None:
        return []

    if not isinstance(context.manifest_data, dict):
        return []

    issues: list[Issue] = []
    for field_name in REQUIRED_MANIFEST_FIELDS:
        if field_name not in context.manifest_data:
            issues.append(
                Issue(
                    severity="warning",
                    code="MANIFEST_MISSING_FIELD",
                    message=f"manifest.json is missing required field '{field_name}'.",
                    file=context.manifest_path,
                    hint=f"Add '{field_name}' to manifest.json.",
                )
            )

    authors = context.manifest_data.get("Authors")
    if "Authors" in context.manifest_data:
        if not isinstance(authors, list) or not authors:
            issues.append(
                Issue(
                    severity="warning",
                    code="MANIFEST_MISSING_FIELD",
                    message="manifest.json is missing required field 'Authors[0].Name'.",
                    file=context.manifest_path,
                    hint="Add at least one author entry with a 'Name' field.",
                )
            )
        else:
            first_author = authors[0]
            if not isinstance(first_author, dict) or "Name" not in first_author:
                issues.append(
                    Issue(
                        severity="warning",
                        code="MANIFEST_MISSING_FIELD",
                        message="manifest.json is missing required field 'Authors[0].Name'.",
                        file=context.manifest_path,
                        hint="Add a 'Name' field to the first author entry.",
                    )
                )

    return issues
