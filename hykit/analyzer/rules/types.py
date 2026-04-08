from __future__ import annotations

from typing import Callable

from ..context import ProjectContext
from ..issues import Issue

Rule = Callable[[ProjectContext], list[Issue]]
