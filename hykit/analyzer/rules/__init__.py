from __future__ import annotations

from .assets import missing_referenced_assets_rule
from .build_files import build_files_missing_rule, gradle_wrapper_missing_rule
from .java_main import (
    main_class_missing_rule,
    main_class_package_mismatch_rule,
    manifest_main_missing_rule,
)
from .json_files import json_files_valid_rule
from .manifest import (
    includes_asset_pack_rule,
    manifest_exists_rule,
    manifest_required_fields_rule,
    manifest_valid_json_rule,
)
from .placeholders import java_package_placeholder_leak_rule
from .scan_errors import scan_errors_rule

ALL_RULES = [
    manifest_exists_rule,
    manifest_valid_json_rule,
    includes_asset_pack_rule,
    manifest_required_fields_rule,
    manifest_main_missing_rule,
    main_class_missing_rule,
    main_class_package_mismatch_rule,
    json_files_valid_rule,
    java_package_placeholder_leak_rule,
    build_files_missing_rule,
    gradle_wrapper_missing_rule,
    missing_referenced_assets_rule,
    scan_errors_rule,
]

__all__ = ["ALL_RULES"]
