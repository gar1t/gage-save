# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

from . import util

PROJECT_MARKERS = [
    # In order of precedence
    ("gage.json",),
    ("gage.yaml",),
    ("pyproject.toml",),
    (".vscode",),
    (".git",),
]


def find_project(dir: str, stop_dir: Optional[str] = None):
    last = None
    while True:
        if _has_project_marker(dir):
            return dir
        if stop_dir and util.compare_paths(stop_dir, dir):
            return None
        last = dir
        dir = os.path.dirname(dir)
        if dir == last:
            return None


def _has_project_marker(dir: str):
    return any(os.path.exists(os.path.join(dir, *marker)) for marker in PROJECT_MARKERS)
