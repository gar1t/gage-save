# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

from . import file_util
from . import sys_config

__all__ = [
    "find_project_dir",
]

PROJECT_MARKERS = [
    ("gage.json",),
    ("gage.toml",),
    ("gage.yaml",),
    ("pyproject.toml",),
    (".vscode",),
    (".git",),
]


def find_project_dir(dirname: str | None = None, stop_dir: str | None = None):
    dirname = dirname or sys_config.cwd()
    last = None
    while True:
        if _has_project_marker(dirname):
            return dirname
        if stop_dir and file_util.compare_paths(stop_dir, dirname):
            return None
        last = dirname
        dirname = os.path.dirname(dirname)
        if dirname == last:
            return None


def _has_project_marker(dir: str):
    return any(os.path.exists(os.path.join(dir, *marker)) for marker in PROJECT_MARKERS)
