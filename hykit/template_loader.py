from __future__ import annotations

import os
from pathlib import Path
import importlib.resources as resources

def _package_template_path() -> Path | None:
    try:
        templates_root = resources.files("hykit.templates")
    except ModuleNotFoundError:
        return None
    candidate = templates_root / "plugin-template-main"
    if candidate.is_dir():
        return Path(candidate)
    return None


def find_template_path() -> Path:
    packaged = _package_template_path()
    if packaged and packaged.exists():
        return packaged

    env_path = os.getenv("HYKIT_TEMPLATE_PATH")
    if env_path:
        path = Path(env_path)
        if path.is_dir():
            return path

    raise FileNotFoundError("Template not found. Provide HYKIT_TEMPLATE_PATH or include a packaged template.")
